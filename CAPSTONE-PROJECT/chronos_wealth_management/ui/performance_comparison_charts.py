"""Altair charts comparing symbol performance, shared by both dashboards.

All history comes through the point-in-time API, so every chart ends at
the account's simulated date — charts can never see the future.
"""

import altair as alt
import pandas as pd

import api_client

PEER_AVERAGE_LABEL = "Peer average"


def fetch_normalized_price_frame(
    user_id: int, symbols: list[str], trading_days: int = 60
) -> pd.DataFrame:
    """Closing prices per symbol, indexed to 1.0 on the first shared date."""
    series = {}
    for symbol in symbols:
        history = api_client.fetch_symbol_price_history(symbol, user_id, trading_days)
        if history:
            frame = pd.DataFrame(history)
            series[symbol] = frame.set_index("date")["close"]
    if not series:
        return pd.DataFrame()
    prices = pd.DataFrame(series).dropna()
    if prices.empty:
        return prices
    return prices.div(prices.iloc[0])


def normalized_performance_chart(normalized_frame: pd.DataFrame) -> alt.Chart:
    """One line per symbol, all starting at 0% growth."""
    growth_long = _growth_long_format(normalized_frame, var_name="symbol")
    return (
        alt.Chart(growth_long)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("growth:Q", title="Growth", axis=alt.Axis(format="+%")),
            color=alt.Color("symbol:N", title="Symbol"),
            tooltip=[
                alt.Tooltip("date:T"),
                alt.Tooltip("symbol:N"),
                alt.Tooltip("growth:Q", format="+.1%"),
            ],
        )
    )


def symbol_vs_peer_average_chart(
    normalized_frame: pd.DataFrame, symbol: str
) -> alt.Chart:
    """The focus symbol against the average of every other symbol."""
    compare = pd.DataFrame(
        {
            symbol: normalized_frame[symbol],
            PEER_AVERAGE_LABEL: _peer_average(normalized_frame, symbol),
        }
    )
    growth_long = _growth_long_format(compare, var_name="series")
    return (
        alt.Chart(growth_long)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("growth:Q", title="Growth", axis=alt.Axis(format="+%")),
            color=alt.Color("series:N", title=None),
            tooltip=[
                alt.Tooltip("date:T"),
                alt.Tooltip("series:N"),
                alt.Tooltip("growth:Q", format="+.1%"),
            ],
        )
    )


def performance_delta_area_chart(
    normalized_frame: pd.DataFrame, symbol: str
) -> alt.Chart:
    """Area chart of how far the focus symbol runs above or below its peers."""
    delta = (
        (normalized_frame[symbol] - _peer_average(normalized_frame, symbol))
        .rename("delta")
        .reset_index()
    )
    return (
        alt.Chart(delta)
        .mark_area(opacity=0.6)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y(
                "delta:Q",
                title=f"{symbol} minus peers",
                axis=alt.Axis(format="+%"),
            ),
            tooltip=[alt.Tooltip("date:T"), alt.Tooltip("delta:Q", format="+.1%")],
        )
    )


def best_and_worst_performers(
    normalized_frame: pd.DataFrame,
) -> tuple[str, float, str, float]:
    """(best symbol, its growth, worst symbol, its growth) over the window."""
    final_growth = normalized_frame.iloc[-1] - 1
    return (
        final_growth.idxmax(),
        final_growth.max(),
        final_growth.idxmin(),
        final_growth.min(),
    )


def _peer_average(normalized_frame: pd.DataFrame, symbol: str) -> pd.Series:
    return normalized_frame.drop(columns=[symbol]).mean(axis=1)


def _growth_long_format(normalized_frame: pd.DataFrame, var_name: str) -> pd.DataFrame:
    return (
        (normalized_frame - 1)
        .reset_index()
        .melt("date", var_name=var_name, value_name="growth")
    )
