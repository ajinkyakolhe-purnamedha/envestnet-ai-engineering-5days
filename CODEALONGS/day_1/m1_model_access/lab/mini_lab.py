"""Mini lab: turn one synthetic portfolio fact into one controlled response."""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

PORTFOLIO_NOTE = "Cash is 40% of the book; AAPL is 52% of invested assets."
PROMPT = f"Explain the greatest portfolio risk in one sentence: {PORTFOLIO_NOTE}"

if api_key := os.getenv("GEMINI_API_KEY"):
    response = genai.Client(api_key=api_key).models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT,
    )
    print(response.text)
else:
    print("Set GEMINI_API_KEY in .env, then run this mini lab.")
