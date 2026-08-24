"""Import checks for the consolidated investor module."""

from chronos.investor_accounts_portfolios_and_history import (
    advance_simulated_investment_date,
    build_account_value_history,
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
    get_symbol_price_history,
)


def test_investor_module_exports_expected_functions():
    assert get_account_for_investor_user.__name__ == "get_account_for_investor_user"
    assert build_current_portfolio_snapshot.__name__ == "build_current_portfolio_snapshot"
    assert build_account_value_history.__name__ == "build_account_value_history"
    assert get_symbol_price_history.__name__ == "get_symbol_price_history"
    assert advance_simulated_investment_date.__name__ == "advance_simulated_investment_date"


def test_investor_module_owns_its_exported_behavior():
    """The lean module contains behavior; legacy modules only preserve imports."""
    exported_functions = (
        get_account_for_investor_user,
        build_current_portfolio_snapshot,
        build_account_value_history,
        get_symbol_price_history,
        advance_simulated_investment_date,
    )

    assert all(
        function.__module__ == "chronos.investor_accounts_portfolios_and_history"
        for function in exported_functions
    )
