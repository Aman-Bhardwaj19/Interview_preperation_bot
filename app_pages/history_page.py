import streamlit as st
from database import get_user_interviews


def _score_tier_class(score):
    if score >= 8:
        return "score-tier-good"
    if score >= 5:
        return "score-tier-mid"
    return "score-tier-low"


def render():
    st.markdown('<div class="main-title">Interview History</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Track your interview performance over time</div>', unsafe_allow_html=True)

    with st.spinner("Loading your history..."):
        interviews = get_user_interviews(st.session_state.user.id)

    if not interviews:
        st.info("No previous interviews found.")
        return

    scores = [float(i["score"]) for i in interviews]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Interviews", len(interviews))
    with col2:
        st.metric("Average Score", f"{sum(scores) / len(scores):.1f}/10")
    with col3:
        st.metric("Best Score", f"{max(scores):.1f}/10")

    with st.container(border=True):
        st.markdown('<div class="section-label">Performance Over Time</div>', unsafe_allow_html=True)
        chart_data = {"Interview": list(range(1, len(scores) + 1)), "Score": scores}
        st.line_chart(chart_data, x="Interview", y="Score")

    st.markdown('<div class="section-label" style="margin-top:20px;">Past Interviews</div>', unsafe_allow_html=True)
    for interview in interviews:
        score = float(interview["score"])
        tier_class = _score_tier_class(score)
        st.markdown(
            f"""
            <div class="question-card {tier_class}">
                <h3>{interview['job_role']} — {score:.1f}/10</h3>
                <p style="color:var(--text-secondary); margin:2px 0;"><b>Interview:</b> {interview['interview_type']}</p>
                <p style="color:var(--text-secondary); margin:2px 0;"><b>Domain:</b> {interview['domain']}</p>
                <p style="color:var(--text-secondary); margin:2px 0;"><b>Date:</b> {interview['created_at'][:10]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )