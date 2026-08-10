"""All HTTP calls from the Streamlit UI to the Chronos Wealth API."""

import os

import requests

API_BASE_URL = os.environ.get("CHRONOS_API_URL", "http://127.0.0.1:8000")


class ApiError(Exception):
    """API returned an error status; message carries the backend detail."""


def _handle(response: requests.Response) -> dict | list:
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise ApiError(str(detail))
    return response.json()


def fetch_demo_user_options() -> list:
    return _handle(requests.get(f"{API_BASE_URL}/auth/demo-users"))


def login_as_demo_user(email: str) -> dict:
    return _handle(
        requests.post(f"{API_BASE_URL}/auth/login", json={"email": email})
    )


def fetch_supported_assets() -> list:
    return _handle(requests.get(f"{API_BASE_URL}/assets"))


def fetch_investor_account(user_id: int) -> dict:
    return _handle(
        requests.get(f"{API_BASE_URL}/account", params={"user_id": user_id})
    )


def fetch_investor_portfolio(user_id: int) -> dict:
    return _handle(
        requests.get(f"{API_BASE_URL}/portfolio", params={"user_id": user_id})
    )


def fetch_account_value_history(user_id: int) -> list:
    return _handle(
        requests.get(
            f"{API_BASE_URL}/portfolio/account-value-history",
            params={"user_id": user_id},
        )
    )


def fetch_symbol_price_history(
    symbol: str, user_id: int, trading_days: int = 60
) -> list:
    return _handle(
        requests.get(
            f"{API_BASE_URL}/market/{symbol}/history",
            params={"user_id": user_id, "trading_days": trading_days},
        )
    )


def fetch_investor_trades(user_id: int) -> list:
    return _handle(
        requests.get(f"{API_BASE_URL}/trades", params={"user_id": user_id})
    )


def preview_investor_trade(
    user_id: int, symbol: str, side: str, amount: float
) -> dict:
    return _handle(
        requests.post(
            f"{API_BASE_URL}/trades/preview",
            json={"user_id": user_id, "symbol": symbol, "side": side, "amount": amount},
        )
    )


def execute_investor_trade(
    user_id: int, symbol: str, side: str, amount: float
) -> dict:
    return _handle(
        requests.post(
            f"{API_BASE_URL}/trades",
            json={"user_id": user_id, "symbol": symbol, "side": side, "amount": amount},
        )
    )


def advance_investor_simulated_date(user_id: int, step: str) -> dict:
    return _handle(
        requests.post(
            f"{API_BASE_URL}/simulation/advance",
            json={"user_id": user_id, "step": step},
        )
    )


def fetch_advisor_clients(advisor_user_id: int) -> list:
    return _handle(
        requests.get(
            f"{API_BASE_URL}/advisor/clients",
            params={"advisor_user_id": advisor_user_id},
        )
    )


def fetch_advisor_client_portfolio(advisor_user_id: int, client_user_id: int) -> dict:
    return _handle(
        requests.get(
            f"{API_BASE_URL}/advisor/clients/{client_user_id}/portfolio",
            params={"advisor_user_id": advisor_user_id},
        )
    )


def generate_advisor_client_report(advisor_user_id: int, client_user_id: int) -> dict:
    return _handle(
        requests.post(
            f"{API_BASE_URL}/advisor/clients/{client_user_id}/report",
            params={"advisor_user_id": advisor_user_id},
        )
    )
