"""A small read-only advisor boundary with privacy-minimised trace evidence."""

from __future__ import annotations

import sys
from uuid import uuid4
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.local_model import call_local_model

evidence_id = "policy/concentration-limit-v1"
policy_fact = "The approved synthetic policy says a holding may not exceed 35% of the portfolio."


def run_advisor(question: str, *, include_evidence: bool = True) -> dict[str, object]:
    """Draft language from approved policy context; Python owns the evidence decision."""

    trace = {
        "run_id": uuid4().hex,
        "question_kind": "policy_explanation",
        "evidence_ids": [evidence_id] if include_evidence else [],
        "policy_decision": "answer_allowed" if include_evidence else "abstain_missing_evidence",
    }
    if not include_evidence:
        return {"answer": "I cannot answer without approved policy evidence.", "status": "needs_evidence", "trace": trace}
    model_run = call_local_model([
        {"role": "system", "content": "Explain only the supplied policy fact. Do not calculate or recommend action."},
        {"role": "user", "content": f"Policy fact: {policy_fact}\nQuestion: {question}"},
    ])
    trace.update({
        "backend": model_run["backend"], "model": model_run["model"],
        "latency_ms": model_run["latency_ms"], "error_code": None,
    })
    if model_run["status"] != "complete":
        trace["error_code"] = "local_model_unavailable"
        return {"answer": "", "status": "dependency_unavailable", "trace": trace}
    answer = str(model_run["text"]).strip()
    trace.update({"status": "complete", "output_chars": len(answer)})
    return {"answer": answer, "status": "complete", "trace": trace}
