"""One concept: keep instruction, context and question separately labelled."""


def assemble_prompt(instruction: str, context: str, question: str) -> str:
    return f"INSTRUCTION: {instruction}\nCONTEXT: {context}\nQUESTION: {question}"


print(assemble_prompt("Be concise.", "AAPL is 52%.", "What is the risk?"))
