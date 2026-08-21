"""One concept: a regular LLM answers from text; an agent asks functions."""

rag_context = [
    "The concentration policy says no single asset may exceed 35%.",
    "Alice currently has AAPL exposure in the portfolio.",
]

function_observations = [
    {"tool": "get_current_price", "result": {"symbol": "AAPL", "price": 108.0}},
    {
        "tool": "check_guideline",
        "result": {"symbol": "AAPL", "proposed_allocation_pct": 36.0, "allowed": False},
    },
]

rag_style_answer = "RAG assembles from retrieved paragraphs already placed in context."
agentic_style_answer = "Agentic LLM assembles from function replies gathered during the loop."

print("RAG input:", rag_context)
print("Agent observations:", function_observations)
print("RAG answer:", rag_style_answer)
print("Agent answer:", agentic_style_answer)
