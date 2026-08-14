"""The same call, shaped for production.

Run:
    uv run --project ../CODE-ALONGS \
        python m1/production_call.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
PROMPT = ("Portfolio book: cash 40%, AAPL 52%. "
          "Name the biggest risk in one sentence.")
MODEL = "gemini-2.5-flash-lite"

load_dotenv(Path(__file__).resolve().parents[2] / ".env",
            override=True)

# #region prod
def production_call(prompt: str) -> str | None:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={"max_output_tokens": 80},
    )

    # Production concern 1: meter every call.
    usage = response.usage_metadata
    print(f"usage prompt={usage.prompt_token_count} "
          f"output={usage.candidates_token_count}")

    # Production concern 2: empty response is not success.
    return response.text or None
# #endregion prod

if __name__ == "__main__":
    print(production_call(PROMPT) if os.getenv("GEMINI_API_KEY")
          else "No GEMINI_API_KEY set -- not calling out.")

# Teaching point: log usage and check empty responses.
