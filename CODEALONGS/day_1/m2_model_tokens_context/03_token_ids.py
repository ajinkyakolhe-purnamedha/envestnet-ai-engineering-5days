"""One concept: a tokenizer turns text into token IDs."""

from pathlib import Path

from transformers import AutoTokenizer

MODEL_PATH = Path(__file__).resolve().parents[3] / "OFFLINE-AI-Models" / "smollm2-135m-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
token_ids = tokenizer.encode("AAPL is 52% of the portfolio.")

print(token_ids)
print(f"{len(token_ids)} tokens")
