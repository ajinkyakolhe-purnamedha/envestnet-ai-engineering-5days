"""Import checks for the consolidated investor module."""

from chronos.investor_accounts_portfolios_and_history import (
    advance_simulated_investment_date,
    build_account_value_history,
    build_current_portfolio_snapshot,
    get_account_for_investor_user,
    get_symbol_price_history,
)


def test_trade_module_owns_preview_execution_and_history_behavior():
    from chronos.investor_trade_execution_and_preview import (
        execute_investor_trade,
        list_trades_for_investor_account,
        preview_investor_trade,
    )
    from chronos.investor_trading.execute_investor_trade import (
        execute_investor_trade as legacy_execute_investor_trade,
    )
    from chronos.investor_trading.list_investor_trades import (
        list_trades_for_investor_account as legacy_list_trades_for_investor_account,
    )
    from chronos.investor_trading.preview_investor_trade import (
        preview_investor_trade as legacy_preview_investor_trade,
    )

    exported_functions = (
        execute_investor_trade,
        list_trades_for_investor_account,
        preview_investor_trade,
    )

    assert all(
        function.__module__ == "chronos.investor_trade_execution_and_preview"
        for function in exported_functions
    )
    assert legacy_execute_investor_trade is execute_investor_trade
    assert legacy_list_trades_for_investor_account is list_trades_for_investor_account
    assert legacy_preview_investor_trade is preview_investor_trade


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
