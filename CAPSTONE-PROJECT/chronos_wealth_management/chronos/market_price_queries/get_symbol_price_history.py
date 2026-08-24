"""Compatibility import for simulated-date price history."""
from chronos.investor_accounts_portfolios_and_history import get_symbol_price_history
def get_symbol_price_history_until_date(*args, **kwargs):
    return get_symbol_price_history(*args, **kwargs)
__all__ = ["get_symbol_price_history_until_date"]
