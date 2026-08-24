"""Chronos domain errors, role checks, and HTTP error translation."""

from contextlib import contextmanager
from fastapi import HTTPException
from chronos.application_database import User

INVESTOR_ROLE = "INVESTOR"
ADVISOR_ROLE = "ADVISOR"


class DomainError(Exception):
    """Base class for business errors raised by the application."""


class RecordNotFoundError(DomainError): pass
class WrongRoleError(DomainError): pass
class PriceUnavailableError(DomainError): pass
class InsufficientCashError(DomainError): pass
class InsufficientSharesError(DomainError): pass
class InvalidSimulatedDateError(DomainError): pass
class NoteDraftAlreadyDecidedError(DomainError): pass
class MarketDataSetupError(DomainError): pass

PermissionDeniedError = WrongRoleError
MarketDataNotLoadedError = MarketDataSetupError
InvalidDraftDecisionError = NoteDraftAlreadyDecidedError


def require_investor_user(user: User) -> User:
    if user.role != INVESTOR_ROLE:
        raise WrongRoleError(f"User {user.id} is {user.role}, not an investor")
    return user


def require_advisor_user(user: User) -> User:
    if user.role != ADVISOR_ROLE:
        raise WrongRoleError(f"User {user.id} is {user.role}, not an advisor")
    return user


_ERROR_STATUS_CODES = [
    (RecordNotFoundError, 404), (WrongRoleError, 403),
    (PriceUnavailableError, 400), (InsufficientCashError, 400),
    (InsufficientSharesError, 400), (InvalidSimulatedDateError, 400),
    (NoteDraftAlreadyDecidedError, 409),
]


@contextmanager
def translate_domain_errors():
    try:
        yield
    except tuple(error for error, _ in _ERROR_STATUS_CODES) as error:
        for error_type, status_code in _ERROR_STATUS_CODES:
            if isinstance(error, error_type):
                raise HTTPException(status_code=status_code, detail=str(error))
        raise
