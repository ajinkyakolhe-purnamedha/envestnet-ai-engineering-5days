"""Choose the simplest application pattern that works.

Fully offline. Run:
    uv run --project ../CODE-ALONGS \
        python m3/pattern_selector.py
"""


# #region selector
def choose_pattern(requirements: set[str]) -> str:
    if "unknown_steps" in requirements or "dynamic_tools" in requirements:
        return "agentic"
    if "style_at_volume" in requirements:
        return "fine-tune"
    if "private_facts" in requirements or "citations" in requirements:
        return "RAG"
    if "format" in requirements or "tone" in requirements:
        return "prompted app"
    return "base call"
# #endregion selector


if __name__ == "__main__":
    cases = [
        {"tone"},
        {"private_facts", "citations"},
        {"unknown_steps", "dynamic_tools"},
    ]
    for case in cases:
        print(f"{choose_pattern(case):>12}  {sorted(case)}")

# The selector is intentionally boring. Walk up the
# ladder and stop at the first rung that satisfies the
# requirement. Architecture you do not need is a liability.
