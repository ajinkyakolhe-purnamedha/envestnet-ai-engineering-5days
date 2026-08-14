"""Keep model, instruction, context, and question separate.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/prompt_context_boundary.py
"""


# #region assembly
MODEL = "local-or-provider-model"

INSTRUCTION = """You are a financial analyst.
Answer only from the context. If the answer is absent,
say "not in the document"."""

CONTEXT = "Policy: no holding may exceed 35% of portfolio value."
QUESTION = "Can Alice hold 40% AAPL?"

prompt = f"{INSTRUCTION}\n\n---\n{CONTEXT}\n---\n\nQ: {QUESTION}"
# #endregion assembly


if __name__ == "__main__":
    print("MODEL:", MODEL)
    print(prompt)

# These are four different knobs. If the output is
# wrong, change one knob at a time. Mixing instruction,
# context, and question into one string too early makes
# failures harder to diagnose.
