"""Lab A: a working chatbot.

Run:
    uv run --project ../CODE-ALONGS --extra chat \
        python m1/gradio_chat.py
Gemini if GEMINI_API_KEY is set, local model otherwise.
"""

import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from chronos_offline import generate

SYSTEM = "You are Chronos's portfolio assistant. Be brief."
MODEL = "gemini-2.5-flash-lite"

load_dotenv(Path(__file__).resolve().parents[2] / ".env",
            override=True)
KEY = os.getenv("GEMINI_API_KEY")

# #region reply
def reply(message, history):
    messages = [{"role": "system", "content": SYSTEM}] + [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    messages.append({"role": "user", "content": message})

    if not KEY:
        return generate(messages, max_new_tokens=128)

    from google import genai

    out = genai.Client(api_key=KEY).models.generate_content(
        model=MODEL,
        contents=f"{SYSTEM}\n\nUser: {message}",
    )
    return out.text
# #endregion reply

if __name__ == "__main__":
    print("Backend:", "gemini flash lite" if KEY else "smollm2")
    gr.ChatInterface(reply, type="messages").launch()
