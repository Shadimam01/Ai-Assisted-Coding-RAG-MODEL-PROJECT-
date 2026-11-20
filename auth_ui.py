"""The login / sign-up screen."""
import streamlit as st

from config import ALLOW_SIGNUP
from core.auth import create_user, verify_user
import ui


def login_screen():
    ui.login_hero()
    _, middle, _ = st.columns([1, 1.5, 1])
    with middle:
        labels = ["Login", "Sign up"] if ALLOW_SIGNUP else ["Login"]
        tabs = st.tabs(labels)

        with tabs[0]:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)
            if submitted:
                user = verify_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Wrong username or password.")

        if ALLOW_SIGNUP:
            with tabs[1]:
                with st.form("signup_form"):
                    new_name = st.text_input("Choose a username")
                    new_pass = st.text_input("Choose a password (min 6 characters)", type="password")
                    confirm = st.text_input("Confirm password", type="password")
                    created = st.form_submit_button("Create account", use_container_width=True)
                if created:
                    if new_pass != confirm:
                        st.error("The two passwords do not match.")
                    else:
                        ok, msg = create_user(new_name, new_pass, role="user")
                        if ok:
                            st.success(msg + " Now open the Login tab and sign in.")
                        else:
                            st.error(msg)
