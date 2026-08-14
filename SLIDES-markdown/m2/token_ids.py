"""Prompt -> Tokens -> Token IDs. Look inside.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/token_ids.py
"""

from transformers import AutoTokenizer

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"
tok = AutoTokenizer.from_pretrained(
    PATH, local_files_only=True
)

text = "Chronos rebalances portfolios internationally."

ids = tok.encode(text)

print(len(ids), "tokens for", len(text), "characters")
for i in ids:
    print(f"{i:>7}  {tok.decode([i])!r}")

# 9 tokens for 46 characters, split like this:
#
#   'Ch' 'ron' 'os' ' re' 'bal' 'ances' ' portfolios'
#   ' internationally' '.'
#
# A token is a frequent chunk of text.
# Not a word. Not a letter. Something in between.
#
# The IDs are this model's. Every model has its own
# vocabulary, so the same sentence costs a different
# number of tokens on a different model.
