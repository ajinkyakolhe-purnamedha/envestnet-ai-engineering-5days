"""M15: a small versioned local service boundary around the advisor."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from advisor_runtime import run_advisor

app = FastAPI(title="Chronos Advisor Draft", version="1.0")


class ExplainRequest(BaseModel):
    question: str = Field(min_length=1, max_length=300)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/advisor/explain")
def explain(request: ExplainRequest) -> dict[str, object]:
    advisor_run = run_advisor(request.question)
    if advisor_run["status"] == "dependency_unavailable":
        raise HTTPException(status_code=503, detail="Local model is unavailable; no answer was generated.")
    return {
        "answer": advisor_run["answer"], "status": advisor_run["status"],
        "trace": {key: advisor_run["trace"].get(key) for key in ("run_id", "evidence_ids", "policy_decision", "latency_ms")},
    }
