"""One concept: RAG retrieves context, then sends that context to the LLM.

Try:
- Change the question to ask about cash.
- Add another document.
- Explain why M4 owns the full indexing and LlamaIndex implementation.
"""

from m3_smolm_setup import call_smolm


def retrieve(question: str, documents: list[dict[str, str]]) -> dict[str, str]:
    """Tiny keyword retrieval to show the RAG architecture shape."""

    terms = set(question.lower().replace("?", "").split())
    best = max(
        documents,
        key=lambda document: len(terms & set(document["text"].lower().replace(".", "").split())),
    )
    return best


def assemble_prompt(instruction: str, context: dict[str, str], question: str) -> str:
    return f"{instruction}\n\nContext from {context['source']}:\n{context['text']}\n\nQuestion: {question}"


documents = [
    {"source": "policy", "text": "Single-asset concentration must not exceed 35% of the portfolio."},
    {"source": "faq", "text": "Advisor notes should be concise and cite the source of policy facts."},
]
question = "Can Alice hold 42% of the portfolio in AAPL?"
retrieved_context = retrieve(question, documents)
prompt = assemble_prompt("Answer only from the retrieved context.", retrieved_context, question)
messages = [
    {"role": "system", "content": "Answer only from the supplied context."},
    {"role": "user", "content": prompt},
]
raw_answer = call_smolm(messages, max_new_tokens=80)
answer = raw_answer

print("retrieved:", retrieved_context)
print("prompt:", prompt)
print("answer:", answer)
