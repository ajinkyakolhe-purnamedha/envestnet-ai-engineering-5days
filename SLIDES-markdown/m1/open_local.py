"""Way 3: open model, on your laptop. No key, no network.

Run:
    uv run --project ../CODE-ALONGS \
        python m1/open_local.py
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

# #region local
PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"

tokenizer = AutoTokenizer.from_pretrained(
    PATH, local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    PATH, local_files_only=True
).eval()

messages = [
    {"role": "system", "content": "You explain portfolios."},
    {"role": "user", "content": "One holding is 52% of it."},
]

prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(prompt, return_tensors="pt")
out = model.generate(
    **inputs, max_new_tokens=60, do_sample=False
)

new = out[0, inputs["input_ids"].shape[-1]:]
print(tokenizer.decode(new, skip_special_tokens=True))
# #endregion local

# No API key. No per-token bill. No data leaving the box.
# 135M parameters -- roughly 1/1000th of a frontier model,
# and it shows. Read the answer critically.
#
# This is the thing you can fine-tune in M6.
