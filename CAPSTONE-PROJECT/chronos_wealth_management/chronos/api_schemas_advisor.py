"""Pydantic request and response models for advisor API endpoints."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


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
    conversation_history: list[str] = []


class AdvisorAssistantAnswerResponse(BaseModel):
    route: str
    refused: bool
    verdict: str | None
    note: str
    note_source: str
    review_problems: list[str]
    metrics: AdvisorMetricResponse | None
    judge_verdict: str | None = None
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
