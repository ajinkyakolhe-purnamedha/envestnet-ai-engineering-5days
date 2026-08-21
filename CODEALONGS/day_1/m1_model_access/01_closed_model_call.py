"""One concept: proprietary SDK calls all have client -> call -> text."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)

PROMPT = "Name one risk in a portfolio with 52% in AAPL."


def call_gemini(prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    reply = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return reply.text


def call_openai(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    reply = client.responses.create(model="gpt-5-mini", input=prompt)
    return reply.output_text


def call_claude(prompt: str) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    reply = client.messages.create(
        model="claude-opus-5",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return next(block.text for block in reply.content if block.type == "text")


print("Same shape each time: create client -> call model -> return text.")
print("Prompt:", PROMPT)
print("GEMINI_API_KEY:", "configured" if os.getenv("GEMINI_API_KEY") else "skipped")
print("OPENAI_API_KEY:", "configured" if os.getenv("OPENAI_API_KEY") else "skipped")
print("ANTHROPIC_API_KEY:", "configured" if os.getenv("ANTHROPIC_API_KEY") else "skipped")
