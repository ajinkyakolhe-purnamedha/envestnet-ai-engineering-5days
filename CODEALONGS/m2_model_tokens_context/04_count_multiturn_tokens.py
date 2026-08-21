"""One concept: multi-turn calls grow because history is resent.

Try:
- Add another assistant/user pair.
- Count again.
- Name what grew: instruction, history, context, or prompt.
"""

import logging

logging.getLogger("LiteLLM").setLevel(logging.ERROR)

from litellm import token_counter


model = "gpt-4o-mini"

turn_one = [
    {"role": "system", "content": "Answer from the conversation."},
    {"role": "user", "content": "What do I hold?"},
]
turn_two = [
    *turn_one,
    {"role": "assistant", "content": "You hold AAPL and SPY."},
    {"role": "user", "content": "Is that too much?"},
]
turn_three = [
    *turn_two,
    {"role": "assistant", "content": "Check AAPL against the 35% concentration limit."},
    {"role": "user", "content": "What should I inspect first?"},
]
turn_four = [
    *turn_three,
    {"role": "assistant", "content": "Inspect concentration first."},
    {"role": "user", "content": "What evidence supports that?"},
]

turn_one_tokens = token_counter(model=model, messages=turn_one)
turn_two_tokens = token_counter(model=model, messages=turn_two)
turn_three_tokens = token_counter(model=model, messages=turn_three)
turn_four_tokens = token_counter(model=model, messages=turn_four)

print("turn 1 tokens", turn_one_tokens)
print("turn 2 tokens", turn_two_tokens)
print("turn 3 tokens", turn_three_tokens)
print("turn 4 tokens", turn_four_tokens)
