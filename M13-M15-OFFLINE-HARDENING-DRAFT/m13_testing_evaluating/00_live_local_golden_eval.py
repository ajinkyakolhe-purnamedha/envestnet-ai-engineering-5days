"""M13: measure a real local model; do not pretend its prose is a unit test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.local_model import call_local_model

golden_cases = [
    {
        "name": "policy explanation",
        "question": "Explain a 35% portfolio concentration limit in one sentence.",
        "required_terms": {"35", "portfolio", "exceed"},
        "forbidden_terms": {"manufacturing", "chemical"},
    },
    {
        "name": "calculation boundary",
        "question": "Do not calculate; explain why Python owns portfolio totals.",
        "required_terms": {"python", "portfolio"},
        "forbidden_terms": set(),
    },
]
passed_cases = 0
for golden_case in golden_cases:
    model_run = call_local_model([{"role": "user", "content": golden_case["question"]}])
    response_text = str(model_run.get("text", "")).strip()
    response_lower = response_text.lower()
    missing_terms = sorted(term for term in golden_case["required_terms"] if term not in response_lower)
    found_forbidden_terms = sorted(term for term in golden_case["forbidden_terms"] if term in response_lower)
    passed = model_run["status"] == "complete" and not missing_terms and not found_forbidden_terms
    passed_cases += passed
    print({"case": golden_case["name"], "passed": passed, "missing_terms": missing_terms,
           "forbidden_terms": found_forbidden_terms, "run": model_run})

print("Golden evaluation:", {"passed": passed_cases, "total": len(golden_cases)})
print("Lesson: measure live model behaviour; prove safety separately with pytest.")
