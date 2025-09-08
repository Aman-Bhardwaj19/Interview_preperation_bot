import streamlit as st
import speech_recognition as sr
import pyttsx3
import os
import re
from dotenv import load_dotenv

# --- Step 1: Initial Configuration ---
# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API with the key from the environment variable
import google.generativeai as genai
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    # This will show a message in the terminal if the key is not found
    print(f"Error configuring Gemini API: {e}") 

# Initialize TTS engine once
try:
    engine = pyttsx3.init()
except Exception as e:
    st.error(f"Failed to initialize Text-to-Speech engine: {e}")
    engine = None

# --- Step 2: Gemini API Functions ---
def generate_llm_questions_gemini(job_role, interview_type, num_questions=5, domain=None):
    """Generates interview questions using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"As an expert interviewer, generate {num_questions} questions for a {job_role} {interview_type}."
    if domain:
        prompt += f" Focus on the {domain} domain."
    
    if interview_type == "Technical Interview":
        prompt += " Include questions on algorithms, data structures, and core concepts relevant to the role."
    elif interview_type == "Behavioral Interview":
        prompt += " Ensure these are STAR-format behavioral questions."
    
    prompt += " Provide only the questions, one per line, without any numbering, bullet points, or introductory/concluding remarks."

    try:
        response = model.generate_content(prompt)
        if not response.parts:
            st.error("The response for generating questions was blocked. Please try again.")
            return ["Could not generate questions due to a block."] * num_questions

        questions_text = response.text.strip()
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
        return questions[:num_questions]

    except Exception as e:
        st.error(f"Error generating questions with Gemini: {e}")
        return ["Could not generate questions. Check your API key and internet connection."] * num_questions

def evaluate_llm_answer_gemini(job_role, interview_type, question, user_answer, domain=None):
    """Evaluates a user's answer using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    if interview_type == "Technical Interview":
        criteria = "technical accuracy, problem-solving approach, and clarity."
    else: # Behavioral
        criteria = "adherence to STAR format (Situation, Task, Action, Result), relevance, and clarity."
    
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
    try:
        response = model.generate_content(prompt)
        if not response.parts:
            return "Evaluation was blocked. The answer might contain sensitive content."
        return response.text.strip()
    except Exception as e:
        st.error(f"Error evaluating answer with Gemini: {e}")
        return "Could not evaluate answer due to an error."

def generate_final_report_gemini(job_role, interview_type, responses_with_feedback):
    """Generates a final summary report using the Gemini API."""
    # --- FIX APPLIED HERE ---
    # Switched to 'gemini-1.5-flash-latest' to avoid the 429 rate limit error on the free tier.
    # It has a higher request limit and is still very capable for summarization.
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 

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
    try:
        response = model.generate_content(full_prompt)
        if not response.parts:
            return "The final report was blocked due to safety settings."
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating final report with Gemini: {e}")
        return "Could not generate final report."

# --- Step 3: Helper Functions for UI ---
def recognize_speech_live():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎙️ Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Increased timeout limits for more flexibility
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=45) 
            text = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {text}")
            return text
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand your response.")
    except sr.RequestError:
        st.error("⚠️ Speech recognition service unavailable.")
    except Exception as e:
        st.error(f"❌ Microphone Error: {str(e)}")
    return ""

def speak(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.error(f"TTS Error: {e}")

# --- Step 4: Streamlit UI Application ---
def interview_page():
    # Your CSS styles here. I've added a few tweaks for better readability.
    st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1d;
        color: #f5f5f5;
    }
    .st-emotion-cache-1c7y2kl {
        background-color: #1a1a1d;
    }
    .question-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #2c3e50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        color: white;
        border-left: 5px solid #c2185b;
    }
    .stButton>button {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button[kind="primary"] {
        background-color: #c2185b;
        color: white;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #ad1457;
    }
    .stButton>button[kind="secondary"] {
        background-color: #4a4a4a;
        color: white;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #5a5a5a;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #c2185b;'>🤖 AI Interview Coach</h1>", unsafe_allow_html=True)

    # Initialize session state variables
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.all_responses = []
        st.session_state.current_question_idx = 0
        st.session_state.questions = []
        st.session_state.current_user_answer = ""
        st.session_state.final_report = None

    # Setup Screen
    if not st.session_state.interview_started:
        st.session_state.job_role = st.text_input("🎯 Target Job Role", "Software Engineer")
        st.session_state.domain = st.text_input("🔬 Optional: Specify Domain", "Backend")
        st.session_state.interview_type = st.radio("✨ Choose Interview Mode", ["Behavioral Interview", "Technical Interview"])
        st.session_state.num_questions = st.slider("Select number of questions", 3, 10, 5)

        if st.button("🚀 Start Interview", type="primary"):
            with st.spinner("Generating interview questions..."):
                st.session_state.questions = generate_llm_questions_gemini(
                    st.session_state.job_role, st.session_state.interview_type, 
                    st.session_state.num_questions, st.session_state.domain
                )
            if st.session_state.questions and "Could not generate" not in st.session_state.questions[0]:
                st.session_state.interview_started = True
                st.session_state.current_question_idx = 0
                st.session_state.all_responses = []
                st.session_state.final_report = None
                st.rerun()
            else:
                st.error("Failed to generate questions. Please check your API key and try again.")
    
    # Interview Screen
    elif st.session_state.current_question_idx < len(st.session_state.questions):
        idx = st.session_state.current_question_idx
        question = st.session_state.questions[idx]

        st.progress((idx) / len(st.session_state.questions), text=f"Question {idx + 1} of {len(st.session_state.questions)}")
        st.markdown(f'<div class="question-card"><h4>❓ {question}</h4></div>', unsafe_allow_html=True)
        # speak(question) # Uncomment to have the bot speak the question

        # Use a single key for the text area and manage its state
        user_answer = st.text_area("Your Answer:", value=st.session_state.current_user_answer, key=f"answer_text_area", height=150)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🎙️ Answer with Voice"):
                st.session_state.current_user_answer = recognize_speech_live()
                st.rerun()
        
        with col2:
            if st.button("✅ Submit Answer", type="primary"):
                if user_answer:
                    with st.spinner("🤖 Evaluating your answer..."):
                        feedback = evaluate_llm_answer_gemini(
                            st.session_state.job_role, st.session_state.interview_type, 
                            question, user_answer, st.session_state.domain
                        )
                    st.session_state.all_responses.append({"question": question, "answer": user_answer, "feedback": feedback})
                    st.session_state.current_question_idx += 1
                    st.session_state.current_user_answer = "" # Clear for next question
                    st.rerun()
                else:
                    st.warning("Please provide an answer before submitting.")

        with col3:
            if st.button("⏭️ Skip Question"):
                st.session_state.all_responses.append({"question": question, "answer": "Skipped", "feedback": "No feedback."})
                st.session_state.current_question_idx += 1
                st.session_state.current_user_answer = ""
                st.rerun()

    # Summary Screen
    else:
        st.success("🎉 Interview Completed!")
        st.markdown("### 📝 Your Interview Summary")

        for i, resp in enumerate(st.session_state.all_responses):
            with st.expander(f"**Question {i+1}: {resp['question']}**"):
                st.markdown(f"**Your Answer:**\n> {resp['answer']}")
                st.markdown(f"**Feedback:**\n> {resp['feedback']}")
        
        # Check if the report has been generated and stored
        if st.session_state.final_report is None:
            if st.button("Generate Final Report", type="primary"):
                with st.spinner("Generating your comprehensive report..."):
                    st.session_state.final_report = generate_final_report_gemini(
                        st.session_state.job_role, st.session_state.interview_type, st.session_state.all_responses
                    )
                st.rerun()
        else:
            st.markdown("---")
            st.markdown("### 📈 Overall Performance Report")
            st.markdown(st.session_state.final_report)
        
        if st.button("🔁 Start New Interview"):
            # A more robust way to reset the session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    st.set_page_config(page_title="AI Interview Coach", layout="wide")
    if os.getenv("GOOGLE_API_KEY"):
        interview_page()
    else:
        st.error("🚨 GOOGLE_API_KEY not found. Please create a .env file and add your key.")
        st.info("The .env file should be in the same directory as main.py and contain: GOOGLE_API_KEY='Your-Key-Here'")

if __name__ == "__main__":
    main()