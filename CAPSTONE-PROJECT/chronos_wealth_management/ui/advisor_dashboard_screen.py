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

    _render_assistant_chat_panel(advisor_user_id, client_user_id)
    _render_approval_queue_panel(advisor_user_id)


def _render_assistant_chat_panel(advisor_user_id: int, client_user_id: int) -> None:
    """The M9 chat panel. Memory is the transcript in st.session_state:
    past (non-refused) questions travel with every request as
    conversation_history — the in-context memory pattern, visible."""
    st.subheader("Assistant")
    st.caption(
        "The assistant drafts; you decide. Portfolio answers land in the "
        "approval queue below — nothing reaches the client until you approve it."
    )
    transcript_key = f"assistant_transcript_{client_user_id}"
    transcript = st.session_state.setdefault(transcript_key, [])
    for past_question, past_note in transcript:
        st.markdown(f"**You:** {past_question}")
        st.info(past_note)

    question = st.text_input("Ask about this client", key=f"assistant_q_{client_user_id}")
    if st.button("Ask assistant") and question:
        conversation_history = [q for q, _ in transcript]
        try:
            answer = api_client.ask_advisor_assistant(
                advisor_user_id, client_user_id, question, conversation_history
            )
        except ApiError as error:
            st.error(str(error))
            return
        st.markdown(f"**You:** {question}")
        st.info(answer["note"])
        st.caption(
            f"route: {answer['route']} · verdict: {answer['verdict'] or '—'} · "
            f"source: {answer['note_source']} · "
            f"judge: {answer['judge_verdict'] or '—'}"
        )
        for problem in answer["review_problems"]:
            st.warning(problem)
        if not answer["refused"]:
            # Refused turns are never remembered: their trade words would
            # poison the router on every later turn.
            transcript.append((question, answer["note"]))
        if answer["draft_id"] is not None:
            st.success(f"Draft #{answer['draft_id']} sent to the approval queue.")
        elif answer["route"] == "portfolio" and not answer["refused"]:
            st.caption(
                "No draft queued — M9 lab step 1 (submit_note_for_approval) "
                "is not implemented yet."
            )


def _render_approval_queue_panel(advisor_user_id: int) -> None:
    """The M9 approval queue: rung 1 (review problems), rung 2 (judge),
    and rung 3 (you) side by side for every pending draft."""
    st.subheader("Approval Queue")
    try:
        drafts = api_client.fetch_pending_note_drafts(advisor_user_id)
    except ApiError as error:
        st.error(str(error))
        return
    if not drafts:
        st.info("No drafts waiting for review.")
        return
    for draft in drafts:
        title = f"Draft #{draft['draft_id']} — {draft['question'][:70]}"
        with st.expander(title, expanded=True):
            st.markdown(draft["note"])
            st.caption(
                f"verdict: {draft['verdict'] or '—'} · "
                f"source: {draft['note_source']} · "
                f"judge: {draft['judge_verdict'] or '—'} · "
                f"as of {draft['created_simulated_date']}"
            )
            for problem in draft["review_problems"]:
                st.warning(problem)
            reason = st.text_input(
                "Decision reason", key=f"draft_reason_{draft['draft_id']}"
            )
            approve_column, reject_column = st.columns(2)
            decision = None
            if approve_column.button(
                "Approve", key=f"approve_{draft['draft_id']}", type="primary"
            ):
                decision = "approved"
            if reject_column.button("Reject", key=f"reject_{draft['draft_id']}"):
                decision = "rejected"
            if decision:
                try:
                    api_client.decide_note_draft(
                        advisor_user_id,
                        draft["draft_id"],
                        decision,
                        reason or f"{decision.capitalize()} by advisor.",
                    )
                    st.rerun()
                except ApiError as error:
                    st.error(str(error))
