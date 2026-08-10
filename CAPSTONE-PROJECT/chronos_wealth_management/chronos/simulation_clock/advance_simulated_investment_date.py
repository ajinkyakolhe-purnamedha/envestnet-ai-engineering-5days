"""Simulated investment date movement: +1 week, +1 month, +1 quarter."""

import calendar
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from chronos.shared_database.database_tables import Account, Price
from chronos.shared_database.domain_errors import InvalidSimulatedDateError

STEP_MONTHS = {"1M": 1, "1Q": 3}


def calculate_next_simulated_date(current_date: date, step: str) -> date:
    if step == "1W":
        return current_date + timedelta(days=7)
    if step in STEP_MONTHS:
        return _add_calendar_months(current_date, STEP_MONTHS[step])
    raise InvalidSimulatedDateError(f"Unknown simulation step {step!r}")


def get_available_market_date_range(db: Session) -> tuple[date, date]:
    min_date, max_date = db.execute(
        select(func.min(Price.date), func.max(Price.date))
    ).one()
    if min_date is None or max_date is None:
        raise InvalidSimulatedDateError("No market prices loaded")
    return min_date, max_date


def advance_simulated_investment_date(
    db: Session, account: Account, step: str
) -> Account:
    next_date = calculate_next_simulated_date(account.simulated_date, step)
    _, max_market_date = get_available_market_date_range(db)
    if next_date > max_market_date:
        raise InvalidSimulatedDateError(
            f"Cannot advance to {next_date}: market data ends {max_market_date}"
        )
    account.simulated_date = next_date
    db.flush()
    return account


def _add_calendar_months(current_date: date, months: int) -> date:
    total_months = current_date.year * 12 + (current_date.month - 1) + months
    year, month = divmod(total_months, 12)
    month += 1
    day = min(current_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)
