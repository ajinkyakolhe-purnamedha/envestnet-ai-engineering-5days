"""The M12 starter reads real bounded Chronos facts before MCP wrapping."""

from chronos.api_schemas_investor import TradeRequest
from chronos.investor_trade_execution_and_preview import execute_investor_trade


def test_m12_starter_reads_bounded_current_portfolio(db, alice, alice_account):
    from labs.m12_governed_mcp.server import read_bounded_portfolio

    execute_investor_trade(
        db,
        alice_account,
        TradeRequest(user_id=alice.id, symbol="AAPL", side="BUY", amount=10_800.0),
    )
    db.commit()

    result = read_bounded_portfolio("alice@example.com", max_positions=1)

    assert result["source"] == "chronos_portfolio_snapshot"
    assert result["simulated_date"] == "2020-06-01"
    assert result["holdings"] == [{"symbol": "AAPL", "shares": 100.0}]


def test_m12_host_admission_excludes_unapproved_tools_before_dispatch():
    from labs.m12_governed_mcp.host_admission import admitted_tools, admission_denial

    discovered = {"advisor_client_portfolio", "export_all_holdings"}

    assert admitted_tools(discovered) == []
    assert admission_denial("export_all_holdings") == {
        "status": "not_implemented",
        "reason": "host_admission_not_implemented",
    }
    assert admission_denial("advisor_client_portfolio") == {
        "status": "not_implemented",
        "reason": "host_admission_not_implemented",
    }
