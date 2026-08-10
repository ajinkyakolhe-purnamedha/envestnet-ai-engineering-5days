"""Translate business errors into HTTP errors at the route boundary."""

from contextlib import contextmanager

from fastapi import HTTPException

from chronos.shared_database.domain_errors import (
    InsufficientCashError,
    InsufficientSharesError,
    InvalidSimulatedDateError,
    PriceUnavailableError,
    RecordNotFoundError,
    WrongRoleError,
)

_ERROR_STATUS_CODES = [
    (RecordNotFoundError, 404),
    (WrongRoleError, 403),
    (PriceUnavailableError, 400),
    (InsufficientCashError, 400),
    (InsufficientSharesError, 400),
    (InvalidSimulatedDateError, 400),
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
