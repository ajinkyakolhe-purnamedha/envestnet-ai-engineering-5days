"""Way 2: closed model, via your own cloud account.

Run:
    uv run --project ../CODE-ALONGS \
        python m1/cloud_call.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv

MODEL = "gemini-2.5-flash-lite"

load_dotenv(Path(__file__).resolve().parents[2] / ".env",
            override=True)


# #region call
def call_gemini(prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )
    return response.text
# #endregion call


if __name__ == "__main__":
    if os.getenv("GEMINI_API_KEY"):
        print(call_gemini("Name one portfolio risk."))
    else:
        print("No GEMINI_API_KEY set -- not calling out.")

# Same request shape as Way 1. The lesson is the boundary:
# hide provider details behind one small function.
