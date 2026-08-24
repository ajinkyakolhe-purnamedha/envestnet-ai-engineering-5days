"""Investor account lookup, valuation, history, and simulation behavior."""

import calendar
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from chronos.app_startup.seed_demo_users_accounts_and_assets import STARTING_SIMULATED_DATE
from chronos.market_data_loading_and_price_queries import get_latest_price_on_or_before_date
from chronos.shared_database.api_schemas import AccountResponse, AccountValueHistoryPointResponse, HoldingValueResponse, PortfolioResponse
from chronos.shared_database.database_tables import Account, Holding, Price, Trade
from chronos.shared_database.domain_errors import InvalidSimulatedDateError, RecordNotFoundError

STEP_MONTHS = {"1M": 1, "1Q": 3}


def get_account_for_investor_user(db: Session, user_id: int) -> Account:
    account = db.scalar(select(Account).where(Account.user_id == user_id))
    if account is None:
        raise RecordNotFoundError(f"No account for user {user_id}")
    return account


def build_investor_account_response(account: Account) -> AccountResponse:
    return AccountResponse(account_id=account.id, user_id=account.user_id, name=account.name, cash_balance=account.cash_balance, initial_cash=account.initial_cash, simulated_date=account.simulated_date)


def calculate_holding_market_value(shares: float, current_price: float) -> float:
    return shares * current_price


def calculate_holding_cost_basis(shares: float, average_cost: float) -> float:
    return shares * average_cost


def calculate_unrealized_gain_loss(market_value: float, cost_basis: float) -> float:
    return market_value - cost_basis


def calculate_holding_gain_loss(shares: float, average_cost: float, current_price: float) -> float:
    return calculate_unrealized_gain_loss(calculate_holding_market_value(shares, current_price), calculate_holding_cost_basis(shares, average_cost))


def build_current_portfolio_snapshot(db: Session, account: Account) -> PortfolioResponse:
    holdings = list(db.scalars(select(Holding).where(Holding.account_id == account.id).order_by(Holding.symbol)))
    holding_values, holdings_value = [], 0.0
    for holding in holdings:
        price = get_latest_price_on_or_before_date(db, holding.symbol, account.simulated_date)
        market_value = calculate_holding_market_value(holding.shares, price.close)
        cost_basis = calculate_holding_cost_basis(holding.shares, holding.average_cost)
        holdings_value += market_value
        holding_values.append(HoldingValueResponse(symbol=holding.symbol, shares=holding.shares, average_cost=holding.average_cost, current_price=price.close, market_value=market_value, cost_basis=cost_basis, unrealized_gain_loss=calculate_unrealized_gain_loss(market_value, cost_basis), allocation_percentage=0.0))
    total_value = account.cash_balance + holdings_value
    calculate_portfolio_allocation_percentages(holding_values, total_value)
    total_return_amount = total_value - account.initial_cash
    return PortfolioResponse(account_id=account.id, user_id=account.user_id, simulated_date=account.simulated_date, cash_balance=account.cash_balance, holdings_value=holdings_value, total_value=total_value, total_return_amount=total_return_amount, total_return_percentage=(total_return_amount / account.initial_cash * 100.0 if account.initial_cash else 0.0), holdings=holding_values)


def calculate_portfolio_allocation_percentages(holding_values: list[HoldingValueResponse], total_value: float) -> None:
    for holding_value in holding_values:
        holding_value.allocation_percentage = holding_value.market_value / total_value * 100.0 if total_value else 0.0


def build_account_value_history(db: Session, account: Account) -> list[AccountValueHistoryPointResponse]:
    market_dates = list(db.scalars(select(Price.date).where(Price.date >= STARTING_SIMULATED_DATE, Price.date <= account.simulated_date).distinct().order_by(Price.date)))
    trades = list(db.scalars(select(Trade).where(Trade.account_id == account.id).order_by(Trade.simulated_date, Trade.id)))
    cash_balance, shares_by_symbol, next_trade_index, history = account.initial_cash, {}, 0, []
    for market_date in market_dates:
        while next_trade_index < len(trades) and trades[next_trade_index].simulated_date <= market_date:
            trade = trades[next_trade_index]
            cash_balance += -trade.amount if trade.side == "BUY" else trade.amount
            shares_by_symbol[trade.symbol] = shares_by_symbol.get(trade.symbol, 0.0) + (trade.shares if trade.side == "BUY" else -trade.shares)
            next_trade_index += 1
        holdings_value = 0.0
        for symbol, shares in shares_by_symbol.items():
            if shares > 0:
                close = db.scalar(select(Price.close).where(Price.symbol == symbol, Price.date <= market_date).order_by(Price.date.desc()).limit(1))
                if close is not None:
                    holdings_value += shares * close
        history.append(AccountValueHistoryPointResponse(date=market_date, cash_balance=cash_balance, holdings_value=holdings_value, total_value=cash_balance + holdings_value))
    return history


def get_symbol_price_history(db: Session, symbol: str, end_date: date, trading_days: int = 60) -> list[Price]:
    return list(reversed(list(db.scalars(select(Price).where(Price.symbol == symbol, Price.date <= end_date).order_by(Price.date.desc()).limit(trading_days)))))


def calculate_next_simulated_date(current_date: date, step: str) -> date:
    if step == "1W": return current_date + timedelta(days=7)
    if step in STEP_MONTHS: return _add_calendar_months(current_date, STEP_MONTHS[step])
    raise InvalidSimulatedDateError(f"Unknown simulation step {step!r}")


def get_available_market_date_range(db: Session) -> tuple[date, date]:
    min_date, max_date = db.execute(select(func.min(Price.date), func.max(Price.date))).one()
    if min_date is None or max_date is None: raise InvalidSimulatedDateError("No market prices loaded")
    return min_date, max_date


def advance_simulated_investment_date(db: Session, account: Account, step: str) -> Account:
    next_date = calculate_next_simulated_date(account.simulated_date, step)
    _, max_market_date = get_available_market_date_range(db)
    if next_date > max_market_date: raise InvalidSimulatedDateError(f"Cannot advance to {next_date}: market data ends {max_market_date}")
    account.simulated_date = next_date
    db.flush()
    return account


def _add_calendar_months(current_date: date, months: int) -> date:
    total_months = current_date.year * 12 + current_date.month - 1 + months
    year, month = divmod(total_months, 12)
    return date(year, month + 1, min(current_date.day, calendar.monthrange(year, month + 1)[1]))
