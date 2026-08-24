"""Pydantic request and response models for investor API endpoints."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TradeRequest(BaseModel):
    user_id: int
    symbol: str
    side: Literal["BUY", "SELL"]
    amount: float = Field(gt=0)


class AdvanceSimulationRequest(BaseModel):
    user_id: int
    step: Literal["1W", "1M", "1Q"]


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    role: str


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    name: str
    asset_class: str
    sector: str | None
    risk_level: str


class AccountResponse(BaseModel):
    account_id: int
    user_id: int
    name: str
    cash_balance: float
    initial_cash: float
    simulated_date: date


class MarketPriceHistoryPointResponse(BaseModel):
    symbol: str
    date: date
    close: float


class HoldingValueResponse(BaseModel):
    symbol: str
    shares: float
    average_cost: float
    current_price: float
    market_value: float
    cost_basis: float
    unrealized_gain_loss: float
    allocation_percentage: float


class PortfolioResponse(BaseModel):
    account_id: int
    user_id: int
    simulated_date: date
    cash_balance: float
    holdings_value: float
    total_value: float
    total_return_amount: float
    total_return_percentage: float
    holdings: list[HoldingValueResponse]


class AccountValueHistoryPointResponse(BaseModel):
    date: date
    cash_balance: float
    holdings_value: float
    total_value: float


class TradePreviewResponse(BaseModel):
    symbol: str
    side: Literal["BUY", "SELL"]
    amount: float
    price: float
    shares: float
    simulated_date: date
    valid: bool
    message: str


class TradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    symbol: str
    side: str
    shares: float
    price: float
    amount: float
    simulated_date: date
    created_at: datetime


class SimulationAdvanceResponse(BaseModel):
    account: AccountResponse
    previous_portfolio: PortfolioResponse
    portfolio: PortfolioResponse
