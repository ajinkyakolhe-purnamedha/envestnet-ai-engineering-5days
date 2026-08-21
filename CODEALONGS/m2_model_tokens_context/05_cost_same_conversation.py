"""One concept: the same conversation costs different amounts by model.

Try:
- Double expected output tokens.
- Recompute one cost.
- Decide what evidence would justify escalating model tier.
"""

import logging

logging.getLogger("LiteLLM").setLevel(logging.ERROR)

from litellm import token_counter
from tokencost import calculate_cost_by_tokens


def price(input_count: int, output_count: int, model_name: str) -> float:
    return calculate_cost_by_tokens(input_count, model_name, "input") + calculate_cost_by_tokens(output_count, model_name, "output")


messages = [
    {"role": "system", "content": "Answer from the conversation and supplied context."},
    {"role": "user", "content": "What do I hold?"},
    {"role": "assistant", "content": "You hold AAPL and SPY."},
    {"role": "system", "content": "Context:\nPolicy: no holding may exceed 35%."},
    {"role": "user", "content": "Is AAPL too large at 42%?"},
]
input_tokens = token_counter(model="gpt-4o-mini", messages=messages)
expected_output_tokens = 120

small_cost = price(input_tokens, expected_output_tokens, "gpt-4o-mini")
medium_cost = price(input_tokens, expected_output_tokens, "gpt-4.1")
large_cost = price(input_tokens, expected_output_tokens, "gpt-4o")
larger_small_cost = price(input_tokens, 240, "gpt-4o-mini")

print("same conversation input tokens:", input_tokens)
print("small model ", small_cost)
print("medium model", medium_cost)
print("large model ", large_cost)
print("small model with larger answer", larger_small_cost)
