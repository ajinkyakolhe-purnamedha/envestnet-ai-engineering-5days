"""One concept: use LlamaIndex LLM calls to rewrite follow-ups before routing.

Try:
- Remove the rewrite step.
- Change the latest question to "Can Alice buy more AAPL?"
- Explain why routing should use the effective question.
"""

from llamaindex_closure_setup import ask_llamaindex


def route_question(text: str) -> str:
    lowered = text.lower()
    if "buy" in lowered or "sell" in lowered:
        return "trade_refusal"
    if "guideline" in lowered or "concentration" in lowered or "35%" in lowered:
        return "policy"
    return "portfolio"


history_questions = ["What does the concentration guideline say?"]
new_question = "Why is that a problem for Alice?"
rewrite_prompt = (
    "Rewrite the latest question as a standalone question.\n"
    f"History: {history_questions}\n"
    f"Latest: {new_question}"
)

rewrite_reply = ask_llamaindex(rewrite_prompt, max_tokens=48)
effective_question = "\n".join([rewrite_reply or history_questions[-1], new_question])
route = route_question(effective_question)

print("rewrite:", rewrite_reply or "[no new text]")
print("effective question:", effective_question)
print("route:", route)
