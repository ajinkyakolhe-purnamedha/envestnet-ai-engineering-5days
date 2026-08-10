"""Investor dashboard: portfolio, charts, trading, and simulated time."""

import pandas as pd
import streamlit as st

import api_client
from api_client import ApiError


def _format_gain_loss(value: float) -> str:
    if value > 0:
        return f":green[+${value:,.2f}]"
    if value < 0:
        return f":red[-${abs(value):,.2f}]"
    return f"${value:,.2f}"


def render_investor_dashboard_screen(user: dict) -> None:
    user_id = user["id"]
    st.title(f"Investor Dashboard — {user['name']}")

    portfolio = api_client.fetch_investor_portfolio(user_id)
    st.caption(f"Simulated date: {portfolio['simulated_date']}")

    _render_portfolio_summary(portfolio)
    _render_holdings_table(portfolio)
    _render_symbol_price_chart(user_id)
    _render_account_value_history_chart(user_id)
    _render_trade_form(user_id)
    _render_time_advance_buttons(user_id)
    _render_trade_history(user_id)


def _render_portfolio_summary(portfolio: dict) -> None:
    cash, holdings, total, gain = st.columns(4)
    cash.metric("Cash", f"${portfolio['cash_balance']:,.2f}")
    holdings.metric("Holdings Value", f"${portfolio['holdings_value']:,.2f}")
    total.metric("Portfolio Value", f"${portfolio['total_value']:,.2f}")
    gain.metric(
        "Total Return",
        f"${portfolio['total_return_amount']:,.2f}",
        f"{portfolio['total_return_percentage']:.2f}%",
    )


def _render_holdings_table(portfolio: dict) -> None:
    st.subheader("Holdings")
    if not portfolio["holdings"]:
        st.info("No holdings yet — use the trade form below to buy your first asset.")
        return
    holdings_frame = pd.DataFrame(portfolio["holdings"])
    st.dataframe(
        holdings_frame.style.map(
            lambda value: (
                "color: green" if value > 0 else "color: red" if value < 0 else ""
            ),
            subset=["unrealized_gain_loss"],
        ),
        hide_index=True,
    )
    total_gain_loss = holdings_frame["unrealized_gain_loss"].sum()
    st.markdown(f"Unrealized gain/loss: {_format_gain_loss(total_gain_loss)}")


def _render_symbol_price_chart(user_id: int) -> None:
    st.subheader("Symbol Price History")
    assets = api_client.fetch_supported_assets()
    symbol = st.selectbox("Symbol", [asset["symbol"] for asset in assets])
    if symbol:
        history = api_client.fetch_symbol_price_history(symbol, user_id)
        if history:
            history_frame = pd.DataFrame(history)
            st.line_chart(history_frame.set_index("date")["close"])
        else:
            st.info(f"No price history for {symbol} before the simulated date.")


def _render_account_value_history_chart(user_id: int) -> None:
    st.subheader("Account Value History")
    history = api_client.fetch_account_value_history(user_id)
    if history:
        history_frame = pd.DataFrame(history)
        st.line_chart(history_frame.set_index("date")["total_value"])


def _render_trade_form(user_id: int) -> None:
    st.subheader("Trade")
    assets = api_client.fetch_supported_assets()
    symbol_column, side_column, amount_column = st.columns(3)
    symbol = symbol_column.selectbox(
        "Trade symbol", [asset["symbol"] for asset in assets]
    )
    side = side_column.selectbox("Side", ["BUY", "SELL"])
    amount = amount_column.number_input(
        "Amount ($)", min_value=1.0, value=1000.0, step=100.0
    )

    if st.button("Preview trade"):
        try:
            st.session_state["pending_preview"] = api_client.preview_investor_trade(
                user_id, symbol, side, amount
            )
        except ApiError as error:
            st.error(str(error))
            st.session_state.pop("pending_preview", None)

    preview = st.session_state.get("pending_preview")
    if preview:
        if preview["valid"]:
            st.success(preview["message"])
            if st.button("Confirm trade", type="primary"):
                try:
                    api_client.execute_investor_trade(
                        user_id,
                        preview["symbol"],
                        preview["side"],
                        preview["amount"],
                    )
                    st.session_state.pop("pending_preview", None)
                    st.rerun()
                except ApiError as error:
                    st.error(str(error))
        else:
            st.error(preview["message"])


def _render_time_advance_buttons(user_id: int) -> None:
    st.subheader("Simulated Time")
    week, month, quarter = st.columns(3)
    step = None
    if week.button("+1 week"):
        step = "1W"
    if month.button("+1 month"):
        step = "1M"
    if quarter.button("+1 quarter"):
        step = "1Q"

    if step:
        try:
            advance = api_client.advance_investor_simulated_date(user_id, step)
            before = advance["previous_portfolio"]
            after = advance["portfolio"]
            change = after["total_value"] - before["total_value"]
            st.info(
                f"Moved {before['simulated_date']} → {after['simulated_date']}: "
                f"portfolio ${before['total_value']:,.2f} → "
                f"${after['total_value']:,.2f} ({_format_gain_loss(change)})"
            )
        except ApiError as error:
            st.error(str(error))


def _render_trade_history(user_id: int) -> None:
    st.subheader("Trade History")
    trades = api_client.fetch_investor_trades(user_id)
    if trades:
        st.dataframe(
            pd.DataFrame(trades)[
                ["id", "simulated_date", "symbol", "side", "shares", "price", "amount"]
            ],
            hide_index=True,
        )
    else:
        st.info("No trades yet.")
