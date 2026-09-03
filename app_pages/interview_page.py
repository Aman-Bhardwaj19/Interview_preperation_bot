import streamlit as st
from ui import apply_custom_css, render_score_gauge, render_progress_bar, render_segmented_toggle
from database import save_interview
from gemini_service import generate_questions, evaluate_answer, generate_final_report, extract_score, strip_html
from voice_utils import recognize_speech_live
from app_pages import history_page


JOB_ROLE_OPTIONS = [
    "Software Engineer", "Frontend Developer", "Backend Developer",
    "Full Stack Developer", "Data Scientist", "Machine Learning Engineer",
    "DevOps Engineer", "Mobile Developer", "Product Manager", "QA Engineer", "Other"
]

DOMAIN_OPTIONS = [
    "Backend", "Frontend", "Full Stack", "Data Science", "Machine Learning",
    "Cloud / DevOps", "Mobile", "Cybersecurity", "General", "Other"
]


def _init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "Interview"
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.all_responses = []
        st.session_state.current_question_idx = 0
        st.session_state.questions = []
        st.session_state.final_report = None


def _render_sidebar():
    from auth import logout
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="app-logo">AI</div>
                <div>
                    <div class="sidebar-title">AI Interview Coach</div>
                    <div class="sidebar-subtitle">Practice smarter</div>
                </div>
            </div>
            <div class="sidebar-divider"></div>
            """,
            unsafe_allow_html=True
        )

        interview_kind = "primary" if st.session_state.page == "Interview" else "secondary"
        history_kind = "primary" if st.session_state.page == "History" else "secondary"

        if st.button("Interview", type=interview_kind, use_container_width=True):
            st.session_state.page = "Interview"
            st.rerun()
        if st.button("History", type=history_kind, use_container_width=True):
            st.session_state.page = "History"
            st.rerun()

        st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

        user_email = getattr(st.session_state.user, "email", "")
        st.markdown(
            f"""<div class="sidebar-user"><div class="sidebar-user-email">{user_email}</div></div>""",
            unsafe_allow_html=True
        )
        if st.button("Sign out", use_container_width=True):
            logout()
            st.rerun()


def _render_setup_screen():
    with st.container(border=True):
        st.markdown('<div class="section-label">Configuration</div>', unsafe_allow_html=True)
        st.markdown("### Configure Your Interview")
        st.markdown(
            '<p style="color:var(--text-secondary); font-size:14px; margin-top:-8px;">'
            'Set the role, domain, and format — the AI will tailor questions to match.</p>',
            unsafe_allow_html=True
        )

        role_choice = st.selectbox("Target Job Role", JOB_ROLE_OPTIONS, index=0)
        if role_choice == "Other":
            st.session_state.job_role = st.text_input("Specify job role", placeholder="e.g. Site Reliability Engineer")
        else:
            st.session_state.job_role = role_choice

        domain_choice = st.selectbox("Domain (Optional)", DOMAIN_OPTIONS, index=0)
        if domain_choice == "Other":
            st.session_state.domain = st.text_input("Specify domain", placeholder="e.g. Embedded Systems")
        else:
            st.session_state.domain = domain_choice

        st.markdown('<div class="section-label" style="margin-top:8px;">Interview Mode</div>', unsafe_allow_html=True)
        st.session_state.interview_type = render_segmented_toggle(
            ["Behavioral Interview", "Technical Interview"],
            state_key="interview_type_toggle"
        )
        st.session_state.num_questions = st.slider("Number of Questions", 3, 10, 5)

        st.divider()
        st.markdown(
            '<p style="color:var(--text-secondary); font-size:13px; margin-bottom:14px;">'
            'Ready when you are — this will generate a fresh set of questions.</p>',
            unsafe_allow_html=True
        )

        if st.button("Start Interview", type="primary", use_container_width=True):
            with st.spinner("Generating interview questions..."):
                questions, error = generate_questions(
                    st.session_state.job_role, st.session_state.interview_type,
                    st.session_state.num_questions, st.session_state.domain
                )
            if questions:
                st.session_state.questions = questions
                st.session_state.interview_started = True
                st.session_state.current_question_idx = 0
                st.session_state.all_responses = []
                st.session_state.final_report = None
                st.rerun()
            else:
                st.error(f"Failed to generate questions: {error}")


def _render_question_screen():
    idx = st.session_state.current_question_idx
    question = strip_html(st.session_state.questions[idx])
    total = len(st.session_state.questions)
    answer_key = f"answer_input_{idx}"

    render_progress_bar(idx + 1, total)

    st.markdown(
        f'''<div class="glass-hero">
            <span class="q-chip">Q{idx + 1}</span>
            <h3>{question}</h3>
        </div>''',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown('<div class="section-label">Your Response</div>', unsafe_allow_html=True)
        user_answer = st.text_area(
            "Type your answer below",
            key=answer_key,
            height=180,
            placeholder="Write your answer here...",
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 1.4, 1])
        with col1:
            if st.button("Voice Answer", use_container_width=True):
                text = recognize_speech_live()
                if text:
                    st.session_state[answer_key] = text
                st.rerun()

        with col2:
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if user_answer:
                    with st.spinner("Evaluating your answer..."):
                        feedback, error = evaluate_answer(
                            st.session_state.job_role, st.session_state.interview_type,
                            question, user_answer, st.session_state.domain
                        )
                    if error:
                        st.warning(f"Evaluation issue: {error}")
                    st.session_state.all_responses.append({"question": question, "answer": user_answer, "feedback": feedback})
                    st.session_state.current_question_idx += 1
                    st.rerun()
                else:
                    st.warning("Please provide an answer before submitting.")

        with col3:
            if st.button("Skip Question", use_container_width=True):
                st.session_state.all_responses.append({"question": question, "answer": "Skipped", "feedback": "No feedback."})
                st.session_state.current_question_idx += 1
                st.rerun()

def _score_tier_class(score):
    if score is None:
        return ""
    if score >= 8:
        return "score-tier-good"
    if score >= 5:
        return "score-tier-mid"
    return "score-tier-low"


def _render_summary_screen():
    st.success("Interview Completed")
    st.markdown("### Your Interview Summary")

    for i, resp in enumerate(st.session_state.all_responses):
        score = extract_score(resp["feedback"])
        score_label = f"{score}/10" if score is not None else "—"

        with st.expander(f"Question {i+1}  ·  Score: {score_label}"):
            st.markdown(f"**Question**\n\n{resp['question']}")
            st.markdown(f"**Your Answer**\n\n> {resp['answer']}")
            st.markdown(f"**AI Feedback**\n\n{resp['feedback']}")

    if st.session_state.final_report is None:
        with st.container(border=True):
            st.markdown('<div class="section-label">Next Step</div>', unsafe_allow_html=True)
            st.markdown("### Generate Your Final Report")
            st.markdown(
                '<p style="color:var(--text-secondary); font-size:14px;">'
                'The AI will review every answer and produce a full performance analysis — '
                'strengths, gaps, and where to focus next.</p>',
                unsafe_allow_html=True
            )
            if st.button("Generate Final Report", type="primary"):
                with st.spinner("Generating your comprehensive report..."):
                    report, error = generate_final_report(
                        st.session_state.job_role, st.session_state.interview_type, st.session_state.all_responses
                    )
                if report:
                    st.session_state.final_report = report
                    scores = [extract_score(r["feedback"]) for r in st.session_state.all_responses]
                    scores = [s for s in scores if s is not None]
                    avg_score = sum(scores) / len(scores) if scores else 0
                    try:
                        save_interview(
                            st.session_state.user.id, st.session_state.job_role,
                            st.session_state.interview_type, st.session_state.domain, avg_score
                        )
                    except Exception as e:
                        st.warning(f"Report generated, but saving to history failed: {e}")
                else:
                    st.error(f"Couldn't generate final report: {error}")
                st.rerun()
    else:
        st.markdown("---")
        st.markdown('<div class="main-title">Performance Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Here is your detailed interview performance analysis</div>', unsafe_allow_html=True)

        scores = [extract_score(r["feedback"]) for r in st.session_state.all_responses]
        scores = [s for s in scores if s is not None]

        if scores:
            avg_score = sum(scores) / len(scores)
            col1, col2 = st.columns(2)
            with col1:
                render_score_gauge(avg_score, max_score=10, label="Overall Score")
            with col2:
                st.metric("Questions Answered", len(st.session_state.all_responses))

        with st.container(border=True):
            st.markdown('<div class="section-label">Detailed Analysis</div>', unsafe_allow_html=True)
            st.markdown(st.session_state.final_report)

    if not st.session_state.get("confirm_reset"):
        if st.button("Start New Interview"):
            st.session_state.confirm_reset = True
            st.rerun()
    else:
        st.warning("This will discard your current results. Are you sure?")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Yes, start new", type="primary", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key not in ("user", "authenticated"):
                        del st.session_state[key]
                st.rerun()
        with col_b:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_reset = False
                st.rerun()


def render():
    apply_custom_css()
    _init_session_state()
    _render_sidebar()

    if st.session_state.page == "History":
        history_page.render()
        return

    st.markdown('<div class="main-title">AI Interview Coach</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Practice interviews with your personal AI coach</div>', unsafe_allow_html=True)

    if not st.session_state.interview_started:
        _render_setup_screen()
    elif st.session_state.current_question_idx < len(st.session_state.questions):
        _render_question_screen()
    else:
        _render_summary_screen()