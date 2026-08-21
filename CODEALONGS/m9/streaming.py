"""Tokens as they are made: streaming from SmolLM2.

Same generate call, but a streamer hands over each piece the
moment it exists — that is all a chat UI's typing effect is.
Fully offline. Run from CODEALONGS/:
    uv run python m9/streaming.py
"""

from threading import Thread

from transformers import TextIteratorStreamer

from chronos_offline import load_chat

# #region stream
tokenizer, model = load_chat()
prompt = tokenizer.apply_chat_template(
    [{"role": "user",
      "content": "Explain diversification in one sentence."}],
    tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt, return_tensors="pt")

streamer = TextIteratorStreamer(
    tokenizer, skip_prompt=True, skip_special_tokens=True)
Thread(target=model.generate, kwargs=dict(
    **inputs, max_new_tokens=60, do_sample=False,
    pad_token_id=tokenizer.eos_token_id,
    streamer=streamer)).start()

for piece in streamer:
    print(piece, end="", flush=True)
print()
# #endregion stream
