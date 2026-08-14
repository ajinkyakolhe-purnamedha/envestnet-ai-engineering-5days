"""Pattern 2: prompt engineered application.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_prompted_app.py
"""

import json


def llm(prompt: str) -> str:
    return '{"symbol": "AAPL", "intent": "review"}'


# #region pattern
SYSTEM = """Extract the symbol and intent.
Return JSON with keys: symbol, intent."""


def parse_request(note: str) -> dict:
    reply = llm(f"{SYSTEM}\n\nAdvisor note: {note}")
    parsed = json.loads(reply)
    assert set(parsed) == {"symbol", "intent"}
    return parsed
# #endregion pattern


if __name__ == "__main__":
    print(parse_request("Please review Alice's AAPL allocation."))

# Pros: cheap, testable, no new infrastructure. Cons:
# facts still come from the model or the input. Prompting
# fixes shape and discipline, not missing knowledge.
