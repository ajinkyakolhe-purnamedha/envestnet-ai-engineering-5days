"""Chronos Wealth Streamlit entry point.

Run from the project root:

    uv run streamlit run ui/app.py
"""

import streamlit as st

from path_setup import configure_project_imports

configure_project_imports()

from advisor_dashboard_screen import render_advisor_dashboard_screen
from demo_user_login_screen import render_demo_user_login_screen
from investor_dashboard_screen import render_investor_dashboard_screen
from lab_pages import select_lab_page, render_lab_page

st.set_page_config(page_title="Chronos Wealth", page_icon="⏳", layout="wide")

user = st.session_state.get("user")

if user is None:
    render_demo_user_login_screen()
else:
    with st.sidebar:
        st.write(f"Logged in as **{user['name']}** ({user['role']})")
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()
        selected_lab = select_lab_page(user)
    if selected_lab is not None:
        render_lab_page(selected_lab, user)
    elif user["role"] == "ADVISOR":
        render_advisor_dashboard_screen(user)
    else:
        render_investor_dashboard_screen(user)
