# Lab · AI assistant reference implementation

## Goal

Build a terminal-first assistant that explains synthetic portfolio facts. The
Chronos Portfolio Assistant is the shared reference implementation; its
application boundary applies equally to support, document, and operations
workflows. It is not a retrieval system or financial-advice tool.

## Mini lab — 15–20 minutes

Run `mini_lab.py` after setting `GEMINI_API_KEY` in the repository `.env`.
Change the instruction, then compare one sentence with three bullets.

## Main lab — 60–90 minutes

1. Start from `starter.py`.
2. Build the complete `system + history + current message` transcript.
3. Pass that transcript to a `call_model(messages)` function.
4. Return a safe message when the model gives no text.
5. Log whether a reply was received.
6. Write two tests: history is preserved; empty output gets the safe message.

`solution.py` is the instructor reference after learners have attempted the
starter. A Gradio wrapper and a local-model adapter are optional extensions;
they must call the same `reply(...)` function.
