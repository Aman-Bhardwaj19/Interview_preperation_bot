import streamlit as st
from database import supabase
from streamlit_cookies_controller import CookieController
import os
import time

COOKIE_NAME = "ai_interview_coach_refresh_token"

controller = CookieController(key="ai_auth")

IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 60


def save_login_session(session):
    if session and session.refresh_token:
        controller.set(
            COOKIE_NAME,
            session.refresh_token,
            max_age=60 * 60 * 24 * 30,
            path="/",
            secure=IS_PRODUCTION,
            same_site="lax"
        )


def restore_login_session():
    if st.session_state.get("user"):
        return True

    try:
        refresh_token = controller.get(COOKIE_NAME)

        if refresh_token is None:
            return None

        if refresh_token == "":
            return False

        response = supabase.auth.refresh_session(refresh_token)

        if response and response.user and response.session:
            st.session_state.user = response.user
            st.session_state.authenticated = True
            save_login_session(response.session)
            return True

    except Exception:
        try:
            controller.remove(COOKIE_NAME)
        except Exception:
            pass
        return False

    return False


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    try:
        controller.remove(COOKIE_NAME)
    except Exception:
        pass
    st.session_state.clear()


def auth_page():
    col_l, col_mid, col_r = st.columns([1, 1.3, 1])

    with col_mid:
        st.markdown(
            """
            <div class="auth-header">
                <div class="app-logo auth-logo">AI</div>
                <h1 class="auth-title">AI Interview Coach</h1>
                <p class="auth-tagline">Practice smarter. Interview better.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):
            mode = st.radio(
                "Choose an option",
                ["Login", "Sign Up"],
                horizontal=True,
                label_visibility="collapsed"
            )

            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            remember_me = True
            if mode == "Login":
                remember_me = st.checkbox("Remember me for 30 days", value=True)

            if mode == "Sign Up":
                if st.button("Create Account", type="primary", use_container_width=True):
                    if not email or not password:
                        st.warning("Please enter both email and password.")
                        return

                    try:
                        response = supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })

                        if response.user:
                            st.success("Account created successfully.")
                            st.info("Check your email to confirm your account before logging in.")

                    except Exception as e:
                        st.error(f"Signup failed: {e}")

            else:  # Login mode
                if st.button("Login", type="primary", use_container_width=True):

                    attempts = st.session_state.get("login_attempts", 0)
                    lockout_until = st.session_state.get("lockout_until", 0)

                    if time.time() < lockout_until:
                        remaining = int(lockout_until - time.time())
                        st.error(f"Too many failed attempts. Try again in {remaining}s.")
                        return

                    if not email or not password:
                        st.warning("Please enter both email and password.")
                        return

                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })

                        if response.user and response.session:
                            st.session_state.user = response.user
                            st.session_state.authenticated = True
                            if remember_me:
                                save_login_session(response.session)
                            st.session_state.login_attempts = 0
                            st.rerun()

                    except Exception as e:
                        attempts += 1
                        st.session_state.login_attempts = attempts

                        if attempts >= MAX_LOGIN_ATTEMPTS:
                            st.session_state.lockout_until = time.time() + LOCKOUT_SECONDS
                            st.error(f"Too many failed attempts. Locked out for {LOCKOUT_SECONDS}s.")
                        else:
                            remaining_attempts = MAX_LOGIN_ATTEMPTS - attempts
                            st.error(f"Login failed: {e}. {remaining_attempts} attempts remaining.")