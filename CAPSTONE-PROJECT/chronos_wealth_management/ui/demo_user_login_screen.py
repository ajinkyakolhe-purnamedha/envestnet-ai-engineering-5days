"""Demo user picker — no passwords in Module 0."""

import streamlit as st

import api_client


def render_demo_user_login_screen() -> None:
    st.title("Chronos Wealth")
    st.caption("Virtual money, synthetic time. Educational software only.")

    try:
        demo_users = api_client.fetch_demo_user_options()
    except Exception as error:
        st.error(f"Cannot reach the API: {error}")
        st.info("Start it with: uv run uvicorn chronos.main:app --reload")
        return

    options = {f"{user['name']} ({user['role']})": user for user in demo_users}
    selected_label = st.selectbox("Log in as", list(options.keys()))

    if st.button("Log in", type="primary"):
        selected_user = options[selected_label]
        logged_in_user = api_client.login_as_demo_user(selected_user["email"])
        st.session_state["user"] = logged_in_user
        st.rerun()
