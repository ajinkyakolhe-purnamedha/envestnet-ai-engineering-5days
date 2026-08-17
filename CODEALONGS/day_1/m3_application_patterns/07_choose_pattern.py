"""One concept: choose the least complex pattern that meets the requirement."""


def choose_pattern(requirements: set[str]) -> str:
    if "dynamic_steps" in requirements:
        return "agentic"
    if "repeated_behavior" in requirements:
        return "fine_tune"
    if {"private_facts", "current_facts"} & requirements:
        return "rag"
    if "format" in requirements:
        return "prompted"
    return "base"


print(choose_pattern({"format"}))
