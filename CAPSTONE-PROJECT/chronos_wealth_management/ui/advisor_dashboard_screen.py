"""Advisor dashboard: client list and read-only portfolios."""

import pandas as pd
import streamlit as st

import api_client
import performance_comparison_charts


def render_advisor_dashboard_screen(user: dict) -> None:
    advisor_user_id = user["id"]
    st.title(f"Advisor Workspace — {user['name']}")
    st.caption(
        "Read-only view of Alice Investor. Advisors never trade for clients."
    )

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

    _render_client_performance_vs_peers(client_user_id, portfolio["holdings"])

def _render_client_performance_vs_peers(
    client_user_id: int, holdings: list[dict]
) -> None:
    """One held symbol against the average of the other supported assets.
    History is fetched as the client, so it ends at the client's
    simulated date — the advisor sees no further than the client can."""
    st.subheader("Performance vs Peers")
    assets = api_client.fetch_supported_assets()
    all_symbols = [asset["symbol"] for asset in assets]
    held_symbols = [holding["symbol"] for holding in holdings]
    default_symbol = held_symbols[0] if held_symbols else all_symbols[0]
    symbol = st.selectbox(
        "Focus symbol", all_symbols, index=all_symbols.index(default_symbol)
    )
    if not symbol:
        return
    normalized = performance_comparison_charts.fetch_normalized_price_frame(
        client_user_id, all_symbols
    )
    if normalized.empty or symbol not in normalized.columns:
        st.info("No price history before this client's simulated date.")
        return
    line_column, delta_column = st.columns(2)
    line_column.altair_chart(
        performance_comparison_charts.symbol_vs_peer_average_chart(
            normalized, symbol
        ),
        use_container_width=True,
    )
    delta_column.altair_chart(
        performance_comparison_charts.performance_delta_area_chart(
            normalized, symbol
        ),
        use_container_width=True,
    )
