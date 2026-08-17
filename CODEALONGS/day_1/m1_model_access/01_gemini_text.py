"""One proprietary-model text call, configured through .env."""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

if api_key := os.getenv("GEMINI_API_KEY"):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Name one risk in a portfolio with 52% in AAPL.",
    )
    print(response.text)
else:
    print("Set GEMINI_API_KEY in .env to run this model call.")
