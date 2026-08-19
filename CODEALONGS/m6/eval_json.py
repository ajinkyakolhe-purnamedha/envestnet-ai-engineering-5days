"""'It sounds better' is not a metric. These are."""

import json

FIELDS = {"symbol", "action", "shares"}


# #region score
def score(reply: str, expected: str) -> dict:
    try:
        got = json.loads(reply)
    except json.JSONDecodeError:
        return {"parses": 0, "schema": 0, "exact": 0}

    return {
        "parses": 1,
        "schema": int(all(set(t) == FIELDS for t in got)),
        "exact": int(got == json.loads(expected)),
    }
# #endregion score


TARGET = '[{"symbol":"AAPL","action":"sell","shares":40}]'
outputs = [
    TARGET,                                     # perfect
    '[{"symbol":"AAPL","action":"sell","shares":4}]',
    '[{"ticker":"AAPL","action":"sell"}]',      # wrong schema
    "Sure! Here are the trades:",               # not JSON
]

results = [score(o, TARGET) for o in outputs]
for metric in ("parses", "schema", "exact"):
    hits = sum(r[metric] for r in results)
    print(f"{metric:8} {hits / len(results):.1%}")

# A real comparison looks like this:
#
#   base + a good prompt   71.0%   44.0%   21.0%
#   fine-tuned adapter    100.0%   99.0%   89.0%
#
# If the first row had won, you ship the prompt and go
# home. Run this BEFORE you train, not after.
#
# For a compliance officer, "exact" is the only column
# that counts -- and a regex for the required disclaimer
# is a real metric too, not a lesser one.
