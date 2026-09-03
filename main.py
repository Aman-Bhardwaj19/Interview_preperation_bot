import os
import streamlit as st
from dotenv import load_dotenv
from auth import auth_page, restore_login_session
from app_pages import interview_page

load_dotenv()


def main():
    st.set_page_config(page_title="AI Interview Coach", layout="wide")

    if not os.getenv("GOOGLE_API_KEY"):
        st.error("🚨 GOOGLE_API_KEY not found.")
        return

    if "user" not in st.session_state and not st.session_state.get("restore_attempted"):
        placeholder = st.empty()
        with placeholder:
            st.info("🔄 Restoring your session...")
        result = restore_login_session()
        st.session_state.restore_attempted = True
        placeholder.empty()
        if result is None:
            st.rerun()

    if "user" not in st.session_state:
        auth_page()
    else:
        interview_page.render()


if __name__ == "__main__":
    main()