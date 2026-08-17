"""One open-weight model call that stays on this machine."""

from pathlib import Path

from transformers import pipeline

MODEL_PATH = Path(__file__).resolve().parents[3] / "OFFLINE-AI-Models/smollm2-135m-instruct"
generate = pipeline("text-generation", model=str(MODEL_PATH), local_files_only=True)

reply = generate("Name one risk in a portfolio with 52% in AAPL.", max_new_tokens=30)
print(reply[0]["generated_text"])
