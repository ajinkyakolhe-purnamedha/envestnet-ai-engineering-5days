"""Pydantic request and response models for the Chronos Wealth API."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    email: str


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


class AdvisorClientSummaryResponse(BaseModel):
    client_user_id: int
    client_name: str
    client_email: str
    account_id: int
    simulated_date: date
    total_value: float
    total_return_percentage: float
    number_of_holdings: int


class AdvisorMetricResponse(BaseModel):
    total_value: float
    cash_ratio: float
    largest_position_ratio: float
    largest_position_symbol: str | None
    total_return_percentage: float
    number_of_holdings: int
    best_holding_symbol: str | None
    best_holding_gain_loss: float | None
    worst_holding_symbol: str | None
    worst_holding_gain_loss: float | None


class AdvisorAssistantAskRequest(BaseModel):
    question: str
    # M9: past advisor questions for this client, oldest first. Empty on
    # a first turn — and for every M8-era caller, which is why it defaults.
    conversation_history: list[str] = []


class AdvisorAssistantAnswerResponse(BaseModel):
    route: str
    refused: bool
    verdict: str | None
    note: str
    note_source: str
    review_problems: list[str]
    metrics: AdvisorMetricResponse | None
    # M9: advisory second opinion from the model judge; never blocks.
    judge_verdict: str | None = None
    # M9: id of the pending approval-queue row created for this answer.
    draft_id: int | None = None


class AdvisorNoteDraftResponse(BaseModel):
    draft_id: int
    advisor_user_id: int
    client_user_id: int
    question: str
    note: str
    verdict: str | None
    note_source: str
    review_problems: list[str]
    judge_verdict: str | None
    status: Literal["pending", "approved", "rejected"]
    decision_reason: str | None
    created_simulated_date: date


class NoteDraftDecisionRequest(BaseModel):
    decision: Literal["approved", "rejected"]
    reason: str


class ClientAdvisorMessageResponse(BaseModel):
    draft_id: int
    note: str
    created_simulated_date: date


class AdvisorReportResponse(BaseModel):
    report_id: int
    advisor_user_id: int
    client_user_id: int
    account_id: int
    simulated_date: date
    summary: str
    metrics: AdvisorMetricResponse
    recommendations: list[str]
    created_at: datetime


class DemoResetResponse(BaseModel):
    accounts_reset: int
