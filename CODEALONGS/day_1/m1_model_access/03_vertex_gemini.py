"""The same Gemini capability through a Google Cloud project and IAM identity."""

import os

from google import genai

if project := os.getenv("GOOGLE_CLOUD_PROJECT"):
    client = genai.Client(vertexai=True, project=project, location="global")
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Name one risk in a portfolio with 52% in AAPL.",
    )
    print(response.text)
else:
    print("Set GOOGLE_CLOUD_PROJECT and authenticate with Google Cloud IAM.")
