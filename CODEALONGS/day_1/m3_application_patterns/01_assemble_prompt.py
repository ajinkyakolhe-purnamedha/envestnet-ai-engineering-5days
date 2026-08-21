"""One concept: keep instruction, context and question separately labelled.

Try:
- Replace the context with a different portfolio fact.
- Change the instruction and observe which part owns tone.
- Change the context and observe which part owns facts.
"""


def assemble_prompt(instruction: str, context: str, question: str) -> str:
    return f"INSTRUCTION: {instruction}\nCONTEXT: {context}\nQUESTION: {question}"


print(assemble_prompt("Be concise.", "AAPL is 52%.", "What is the risk?"))
print(assemble_prompt("Use bullets.", "SPY is 52%.", "Name one risk."))
