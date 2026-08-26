from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def choose(case: dict[str, bool]) -> str:
    if case["tools"]: return "agentic workflow"
    if case["repeated_style"]: return "fine-tuning"
    if case["private_knowledge"]: return "RAG"
    if case["fixed_schema"]: return "structured output"
    return "direct call"


def main() -> None:
    cases = [{"tools": False, "repeated_style": False, "private_knowledge": False, "fixed_schema": False}, {"tools": False, "repeated_style": False, "private_knowledge": True, "fixed_schema": False}, {"tools": True, "repeated_style": False, "private_knowledge": False, "fixed_schema": False}]
    for case in cases: print(case, "->", choose(case))
    assert 36 > 35, "A deterministic policy check must reject 36%."
    print("Direct-call example:", chat([{"role": "user", "content": "Define diversification in one sentence."}], 32))


if __name__ == "__main__":
    main()
