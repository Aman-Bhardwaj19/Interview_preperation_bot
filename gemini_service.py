import os
import re
import time
from google import genai

try:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    client = None

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
def strip_html(text):
    """Remove any HTML tags Gemini occasionally includes in question output."""
    if not text:
        return text
    cleaned = re.sub(r"<[^>]+>", "", text)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned

def call_gemini_with_retry(prompt, model=MODEL_NAME, max_retries=3):
    """Calls Gemini with exponential backoff on rate-limit/transient errors.
    Returns (success: bool, text_or_error: str)."""
    if client is None:
        return False, "Gemini client not configured. Check GOOGLE_API_KEY."

    delay = 2
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            if response.text:
                return True, response.text.strip()
            return False, "Response was blocked by safety settings."
        except Exception as e:
            err_str = str(e)
            is_rate_limit = "429" in err_str or "rate" in err_str.lower()
            if is_rate_limit and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            return False, f"Gemini error: {err_str}"
    return False, "Failed after multiple retries."


def generate_questions(job_role, interview_type, num_questions=5, domain=None):
    prompt = f"As an expert interviewer, generate {num_questions} questions for a {job_role} {interview_type}."
    if domain:
        prompt += f" Focus on the {domain} domain."
    if interview_type == "Technical Interview":
        prompt += " Include questions on algorithms, data structures, and core concepts relevant to the role."
    elif interview_type == "Behavioral Interview":
        prompt += " Ensure these are STAR-format behavioral questions."
    prompt += " Provide only the questions, one per line, without any numbering, bullet points, or introductory/concluding remarks."

    success, result = call_gemini_with_retry(prompt)
    if not success:
        return None, result

    questions = [strip_html(q.strip()) for q in result.split('\n') if q.strip()]
    return questions[:num_questions], None


def evaluate_answer(job_role, interview_type, question, user_answer, domain=None):
    criteria = (
        "technical accuracy, problem-solving approach, and clarity."
        if interview_type == "Technical Interview"
        else "adherence to STAR format (Situation, Task, Action, Result), relevance, and clarity."
    )
    context = f"The candidate is interviewing for a {job_role} role. The question is: '{question}'."
    if domain:
        context += f" The domain is {domain}."

    prompt = f"""
    You are an experienced interviewer. Evaluate the candidate's answer.
    Context: {context}
    Question: "{question}"
    Candidate's Answer: "{user_answer}"

    Provide:
    1. A brief feedback comment on strengths and weaknesses, focusing on {criteria}.
    2. A score for the answer, formatted exactly as: "Score: [score]/10".
    3. A suggestion for improvement.

    Use these exact headings: "Feedback:", "Score:", and "Improvement Suggestion:".
    """
    success, result = call_gemini_with_retry(prompt)
    if not success:
        return "Feedback: Unavailable.\nScore: 0/10\nImprovement Suggestion: N/A (evaluation failed)", result
    return result, None


def generate_final_report(job_role, interview_type, responses_with_feedback):
    report_prompt_parts = [f"Generate a final interview summary report for a {job_role} {interview_type} based on the following interactions:"]
    total_score, num_answered = 0, 0
    for q_obj in responses_with_feedback:
        score_match = re.search(r"Score: (\d+)/10", q_obj["feedback"])
        if score_match:
            total_score += int(score_match.group(1))
            num_answered += 1
        report_prompt_parts.append(f"\n---\nQuestion: {q_obj['question']}\nCandidate's Answer: {q_obj['answer']}\nFeedback Given: {q_obj['feedback']}")

    avg_score = (total_score / num_answered) if num_answered > 0 else 0
    report_prompt_parts.append(f"\n---\nBased on all interactions (average score: {avg_score:.1f}/10), provide a comprehensive final report with these sections:")
    report_prompt_parts.append("1. **Overall Strengths** (in bullet points)")
    report_prompt_parts.append("2. **Overall Areas for Improvement** (in bullet points)")
    report_prompt_parts.append("3. **Suggested Resources** for further learning")
    report_prompt_parts.append("4. A final overall rating formatted as: '**Final Score: [score]/10**'")

    full_prompt = "\n".join(report_prompt_parts)
    success, result = call_gemini_with_retry(full_prompt)
    if not success:
        return None, result
    return result, None


def extract_score(feedback_text):
    """Shared helper — replaces the score regex that was duplicated 3x in main.py."""
    match = re.search(r"Score: (\d+)/10", feedback_text)
    return int(match.group(1)) if match else None