"""Business errors raised by domain functions and translated to HTTP errors."""


class RecordNotFoundError(Exception):
    """Unknown user, account, symbol, report, or price row."""


class WrongRoleError(Exception):
    """User does not have the role the feature requires."""


class PriceUnavailableError(Exception):
    """No price exists on or before the requested simulated date."""


class InsufficientCashError(Exception):
    """Buy amount exceeds the account cash balance."""


class InsufficientSharesError(Exception):
    """Sell amount exceeds the shares currently held."""


class InvalidSimulatedDateError(Exception):
    """Simulated date move is outside the available market date range."""


class MarketDataSetupError(Exception):
    """Market prices are missing; the load script must be run first."""
