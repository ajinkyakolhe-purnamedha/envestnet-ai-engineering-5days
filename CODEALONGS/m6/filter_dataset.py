"""Most of what you generated is unusable. Delete it."""

import json

FIELDS = {"symbol", "action", "shares"}


# #region filter
def keep(row: dict) -> bool:
    try:
        trades = json.loads(row["output"])
    except json.JSONDecodeError:
        return False                     # not even JSON

    for t in trades:
        if set(t) != FIELDS:
            return False                 # wrong schema
        if t["action"] not in ("buy", "sell"):
            return False                 # invented value
        if not isinstance(t["shares"], int):
            return False
    return True
# #endregion filter


rows = [
    {"input": "sell 40 AAPL",
     "output": '[{"symbol":"AAPL","action":"sell",'
               '"shares":40}]'},
    {"input": "sell 40 AAPL",           # exact duplicate
     "output": '[{"symbol":"AAPL","action":"sell",'
               '"shares":40}]'},
    {"input": "buy MSFT", "output": "not json at all"},
    {"input": "hold GLD",
     "output": '[{"symbol":"GLD","action":"hold",'
               '"shares":1}]'},
]

clean = [r for r in rows if keep(r)]

seen, deduped = set(), []
for r in clean:
    if r["input"] not in seen:
        seen.add(r["input"])
        deduped.append(r)

print(len(rows), len(clean), len(deduped))    # 4 2 1

# On a real run that reads more like:  15000 12841 9702
#
# Synthetic data collapses into the same three sentences
# faster than you expect, so the dedupe line matters as
# much as the schema check. Hold out 10% before you
# train, and do not look at it until the end.
