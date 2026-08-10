"""Advisor dashboard: client list, read-only portfolios, and reports."""

import pandas as pd
import streamlit as st

import api_client
from api_client import ApiError


def render_advisor_dashboard_screen(user: dict) -> None:
    advisor_user_id = user["id"]
    st.title(f"Advisor Workspace — {user['name']}")
    st.caption("Read-only client view. Advisors never trade for clients.")

    clients = api_client.fetch_advisor_clients(advisor_user_id)
    st.subheader("Clients")
    st.dataframe(pd.DataFrame(clients), hide_index=True)

    client_by_label = {
        f"{client['client_name']} (#{client['client_user_id']})": client
        for client in clients
    }
    selected_label = st.selectbox("Select client", list(client_by_label.keys()))
    if not selected_label:
        return
    selected_client = client_by_label[selected_label]
    st.session_state["selected_advisor_client"] = selected_client["client_user_id"]
    client_user_id = selected_client["client_user_id"]

    portfolio = api_client.fetch_advisor_client_portfolio(
        advisor_user_id, client_user_id
    )
    st.subheader(f"{selected_client['client_name']} — Portfolio")
    total, cash, gain = st.columns(3)
    total.metric("Portfolio Value", f"${portfolio['total_value']:,.2f}")
    cash.metric("Cash", f"${portfolio['cash_balance']:,.2f}")
    gain.metric("Total Return", f"{portfolio['total_return_percentage']:.2f}%")
    if portfolio["holdings"]:
        st.dataframe(pd.DataFrame(portfolio["holdings"]), hide_index=True)
    else:
        st.info("This client has no holdings.")

    st.subheader("Advisor Report")
    if st.button("Generate report", type="primary"):
        try:
            st.session_state["latest_advisor_report"] = (
                api_client.generate_advisor_client_report(
                    advisor_user_id, client_user_id
                )
            )
        except ApiError as error:
            st.error(str(error))

    report = st.session_state.get("latest_advisor_report")
    if report and report["client_user_id"] == client_user_id:
        st.markdown(f"**{report['summary']}**")
        metrics = report["metrics"]
        st.json(metrics)
        if report["recommendations"]:
            st.markdown("**Warnings and recommendations:**")
            for recommendation in report["recommendations"]:
                st.warning(recommendation)
        else:
            st.success("No advisory flags for this portfolio.")
