"""M15: make one evidence-based repair and compare the same case."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from advisor_runtime import run_advisor

question = "Why is a 42% holding above the concentration limit?"
before = run_advisor(question, include_evidence=False)
after = run_advisor(question, include_evidence=True)
comparison = {
    "before": {"status": before["status"], "evidence_count": len(before["trace"]["evidence_ids"])},
    "after": {"status": after["status"], "evidence_count": len(after["trace"]["evidence_ids"]), "latency_ms": after["trace"].get("latency_ms")},
}
assert comparison["before"]["status"] == "needs_evidence"
print("Measured repair:", comparison)
print("A quality gain never overrides safety, evidence, or latency constraints.")
