"""Closed model calls behind one adapter.

No provider key needed; this shows the boundary. Run:
    uv run --project ../CODE-ALONGS \
        python m3/provider_adapter.py
"""

from dataclasses import dataclass


@dataclass
class ModelSettings:
    provider: str
    model: str
    max_tokens: int = 500


# #region adapter
def call_model(settings: ModelSettings,
               messages: list[dict]) -> str:
    if settings.provider == "local":
        return "local model reply"
    if settings.provider == "google":
        return (f"{settings.provider}:{settings.model} "
                f"would receive {len(messages)} messages")
    raise ValueError(f"unknown provider {settings.provider}")
# #endregion adapter


if __name__ == "__main__":
    settings = ModelSettings("google", "gemini-2.5-flash-lite")
    print(call_model(settings, [{"role": "user", "content": "Hi"}]))

# Provider choice is an operating decision, not something
# to scatter through product code. Keep provider, model
# name, and token limits at the boundary so swapping them
# is configuration, not surgery.
