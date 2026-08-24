"""Pydantic request and response models for system-level API endpoints."""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str


class DemoResetResponse(BaseModel):
    accounts_reset: int
