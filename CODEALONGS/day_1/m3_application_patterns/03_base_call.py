"""One concept: a direct call uses general language capability only."""


def direct_answer(question: str) -> str:
    return f"Draft answer to: {question}"


print(direct_answer("Rewrite this client note in plain English."))
