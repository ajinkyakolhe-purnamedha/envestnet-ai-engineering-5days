"""Lab B: pull the network cable. It still works.

Run:
    uv run --project ../CODE-ALONGS --extra chat \
        python m1/gradio_offline.py
"""

import os

# Set BEFORE transformers is imported. Any attempt to
# reach huggingface.co now raises instead of downloading.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import gradio as gr                              # noqa: E402

from chronos_offline import generate             # noqa: E402

SYSTEM = "You are Chronos's portfolio assistant. Be brief."


# #region reply
def reply(message, history):
    messages = [{"role": "system", "content": SYSTEM}]
    messages += [
        {"role": m["role"], "content": m["content"]}
        for m in history
    ]
    messages.append({"role": "user", "content": message})

    return generate(messages, max_new_tokens=128)
# #endregion reply


if __name__ == "__main__":
    gr.ChatInterface(reply, type="messages").launch()

# Now actually turn the wifi off and reload the page.
#
# Worse answers than Lab A -- 135M against a frontier
# model. But: no key, no bill, no data leaving the room,
# and nobody can deprecate it out from under you.
