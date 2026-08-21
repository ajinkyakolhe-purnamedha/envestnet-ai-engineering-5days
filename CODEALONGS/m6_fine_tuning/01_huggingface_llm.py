"""One script: load and call a local Hugging Face LLM."""

import sys
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_hf_setup import MODEL_DIR  # noqa: E402


model_name = str(MODEL_DIR)

tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)

prompt = "Classify this ticket as JSON: I cannot log in with SSO."
inputs = tokenizer(prompt, return_tensors="pt")
output_ids = model.generate(**inputs, max_new_tokens=16, do_sample=False)

print(tokenizer.decode(output_ids[0], skip_special_tokens=True))
