"""Rung 3: the human gate, in fifteen lines.

The workflow drafts; a person decides; only approved work
ships. The capstone version is exactly this loop with a
database row and a dashboard button. Run from
SLIDES-markdown/:
    uv run --project ../CODE-ALONGS python m9/approval_gate.py
"""

# #region gate
DRAFTS = [
    "AAPL is 52% of the portfolio, above the 35% cap.",
    "The portfolio looks fine; no changes needed.",
]

published = []
for draft in DRAFTS:
    print(f"\nDRAFT: {draft}")
    decision = input("approve? [y/n] ").strip().lower()
    if decision == "y":
        published.append(draft)
        print("-> published to the client")
    else:
        print("-> discarded; the client never sees it")

print(f"\nclient sees {len(published)} of {len(DRAFTS)}")
# #endregion gate
