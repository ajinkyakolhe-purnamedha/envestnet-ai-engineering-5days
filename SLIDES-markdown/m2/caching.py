"""Stop paying full price for the same prefix.

Run:
    uv run --project ../CODE-ALONGS \
        python m2/caching.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv

POLICY = open("data/investment_policy.md").read()
MODEL = "gemini-2.5-flash-lite"

load_dotenv(Path(__file__).resolve().parents[2] / ".env",
            override=True)


# #region cache
def ask_with_stable_prefix(question: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=MODEL,
        contents=f"Policy:\n{POLICY}\n\nQuestion: {question}",
    )
    return response.text
# #endregion cache


if __name__ == "__main__":
    if os.getenv("GEMINI_API_KEY"):
        print(ask_with_stable_prefix("What is the holding limit?"))
    else:
        print("No GEMINI_API_KEY set -- not calling out.")

# Lesson: keep the big policy prefix stable. Caching and
# cost controls work best when only the question changes.
