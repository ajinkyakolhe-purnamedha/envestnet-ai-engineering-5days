"""One gold example. A domain expert writes 100-300."""

import json

example = {
    "instruction":
        "Extract the trades from this advisor note as JSON.",
    "input":
        "Spoke to Mrs Rao, 12 March. Wants out of AAPL "
        "- sell all 40 shares. Move it into MSFT, about "
        "150 shares if the cash covers it.",
    "output": json.dumps([
        {"symbol": "AAPL", "action": "sell", "shares": 40},
        {"symbol": "MSFT", "action": "buy", "shares": 150},
    ]),
}

print(json.dumps(example, indent=2)[:200])

# Write the awkward ones by hand, because the frontier
# model will not invent them for you:
#   - a note with no trade in it at all
#   - tax-loss harvesting across two accounts
#   - a symbol that is not in the curated list
#   - "sell half" (a percentage, not a share count)
#   - a note that needs advisor approval before anything
#
# 300 careful examples beat 10,000 careless ones. This
# file is the project; the training run is an afternoon.
