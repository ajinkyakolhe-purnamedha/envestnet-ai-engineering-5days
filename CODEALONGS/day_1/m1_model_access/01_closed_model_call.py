"""Three proprietary SDKs, one identical call shape."""

import os

import anthropic
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv(override=True)

PROMPT = "Name one risk in a portfolio with 52% in AAPL."


# #region providers
def call_gemini(prompt: str) -> str:
    key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=key)
    reply = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return reply.text


def call_openai(prompt: str) -> str:
    key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=key)
    reply = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )
    return reply.output_text


def call_claude(prompt: str) -> str:
    key = os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)
    reply = client.messages.create(
        model="claude-opus-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return next(
        b.text for b in reply.content if b.type == "text"
    )
# #endregion


PROVIDERS = {
    "GEMINI_API_KEY": call_gemini,
    "OPENAI_API_KEY": call_openai,
    "ANTHROPIC_API_KEY": call_claude,
}

for env_name, call_model in PROVIDERS.items():
    if not os.getenv(env_name):
        print(f"{env_name}: not set, skipped")
        continue
    try:
        print(f"{env_name}: {call_model(PROMPT)}")
    except Exception as error:
        # A model call is a network call. Quota, billing and
        # outages are normal, so one dead key must not stop
        # the other two from running.
        print(f"{env_name}: call failed -- {type(error).__name__}")
