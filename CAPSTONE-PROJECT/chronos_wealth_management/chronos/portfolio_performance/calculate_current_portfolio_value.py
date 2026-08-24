"""Portfolio snapshot valued at the account's simulated date."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from chronos.market_data_loading_and_price_queries import (
    get_latest_price_on_or_before_date,
)
from chronos.portfolio_performance.calculate_holding_gain_loss import (
    calculate_holding_cost_basis,
    calculate_holding_market_value,
    calculate_unrealized_gain_loss,
)
from chronos.shared_database.api_schemas import (
    HoldingValueResponse,
    PortfolioResponse,
)
from chronos.shared_database.database_tables import Account, Holding


def build_current_portfolio_snapshot(db: Session, account: Account) -> PortfolioResponse:
    holdings = list(
        db.scalars(
            select(Holding)
            .where(Holding.account_id == account.id)
            .order_by(Holding.symbol)
        )
    )

    holding_values: list[HoldingValueResponse] = []
    holdings_value = 0.0
    for holding in holdings:
        price = get_latest_price_on_or_before_date(
            db, holding.symbol, account.simulated_date
        )
        market_value = calculate_holding_market_value(holding.shares, price.close)
        cost_basis = calculate_holding_cost_basis(holding.shares, holding.average_cost)
        holdings_value += market_value
        holding_values.append(
            HoldingValueResponse(
                symbol=holding.symbol,
                shares=holding.shares,
                average_cost=holding.average_cost,
                current_price=price.close,
                market_value=market_value,
                cost_basis=cost_basis,
                unrealized_gain_loss=calculate_unrealized_gain_loss(
                    market_value, cost_basis
                ),
                allocation_percentage=0.0,
            )
        )

    total_value = account.cash_balance + holdings_value
    calculate_portfolio_allocation_percentages(holding_values, total_value)

    total_return_amount = total_value - account.initial_cash
    total_return_percentage = (
        total_return_amount / account.initial_cash * 100.0
        if account.initial_cash
        else 0.0
    )

    return PortfolioResponse(
        account_id=account.id,
        user_id=account.user_id,
        simulated_date=account.simulated_date,
        cash_balance=account.cash_balance,
        holdings_value=holdings_value,
        total_value=total_value,
        total_return_amount=total_return_amount,
        total_return_percentage=total_return_percentage,
        holdings=holding_values,
    )


def calculate_portfolio_allocation_percentages(
    holding_values: list[HoldingValueResponse], total_value: float
) -> None:
    for holding_value in holding_values:
        holding_value.allocation_percentage = (
            holding_value.market_value / total_value * 100.0 if total_value else 0.0
        )
