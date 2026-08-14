"""Way 1: closed model, straight from the vendor.

Run:
    uv run --project ../CODE-ALONGS \
        python m1/first_call.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv

NOTE = "Cash is 40% of the book, AAPL is 52%."
MODEL = "gemini-2.5-flash-lite"

load_dotenv(Path(__file__).resolve().parents[2] / ".env",
            override=True)


# #region call
def name_the_risk(note: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=MODEL,
        contents=("Return exactly one sentence. "
                  f"Name the biggest concentration risk: {note}"),
        config={"max_output_tokens": 60},
    )
    return response.text
# #endregion call


if __name__ == "__main__":
    if os.getenv("GEMINI_API_KEY"):
        print(name_the_risk(NOTE))
    else:
        print("No GEMINI_API_KEY set -- not calling out.")
        print("Read the shape above; run m1/open_local.py")
        print("for the version that needs no key at all.")

# You are renting Google's hosted model, per token. Flash
# Lite is cheap enough for demos, but it is still a cloud call.
