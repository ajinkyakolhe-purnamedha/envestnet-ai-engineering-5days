"""Pydantic request and response models for advisor API endpoints."""

from datetime import date

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
