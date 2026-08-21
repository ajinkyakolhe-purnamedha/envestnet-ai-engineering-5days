"""One concept: choose the least complex pattern that meets the requirement.

Try:
- Classify a private, changing policy question.
- Classify a stable high-volume extraction workflow.
- Explain why dynamic steps do not automatically mean "agent."
"""


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


cases = [
    {"general_language"},
    {"format"},
    {"private_facts"},
    {"repeated_behavior"},
    {"dynamic_steps"},
]
decisions = {tuple(sorted(requirements)): choose_pattern(requirements) for requirements in cases}

for requirements, pattern in decisions.items():
    print(set(requirements), "->", pattern)
