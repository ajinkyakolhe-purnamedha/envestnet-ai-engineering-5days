"""Count before you send. The only honest estimate.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/count_tokens.py
"""

from chronos_offline import count_tokens

POLICY = open("data/investment_policy.md").read()

print(len(POLICY.split()), "words")
print(count_tokens(POLICY), "tokens")

# Word count is not token count, and the gap is not a
# constant. It gets worse on code, on JSON, and on any
# language the tokeniser was not built around.

JSON = '{"symbol":"AAPL"}'
for text in ["portfolio", "Rebalancing", "AAPL", JSON,
             "पोर्टफोलियो"]:
    print(f"{count_tokens(text):>3}  {text}")

#   2  portfolio
#   7  {"symbol":"AAPL"}        JSON is punctuation-heavy
#  15  पोर्टफोलियो               "portfolio", in Hindi
#
# "portfolio" costs 2 tokens in English and 15 in Hindi.
# That is a 7x bill on identical meaning -- and a 7x
# bite out of the context window -- for any product
# serving more than one language.
