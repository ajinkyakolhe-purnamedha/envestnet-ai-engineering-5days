# M9 Code-Alongs: Finish Agentic Applications

M7 built the loop by hand. M8 used frameworks to build an agentic workflow.
M9 finishes the feature with LlamaIndex-backed implementation patterns:
memory, verification, human approval, durable state, and an end-to-end
product-safe path.

Run from the repository root:

```bash
uv run --project CODEALONGS python CODEALONGS/m9_memory_verification_hitl/01_memory_is_messages.py
```

Snippets:

- `01_memory_is_messages.py` - LlamaIndex memory with and without history
- `02_bounded_memory.py` - bounded LlamaIndex memory before model calls
- `03_effective_question.py` - LlamaIndex rewrite before routing
- `04_verify_generated_draft.py` - verify a LlamaIndex draft with rules
- `05_model_judge.py` - measure a LlamaIndex judge against a rule
- `06_human_gate_and_state.py` - gate M8 workflow drafts and reload state

Optional stretch:

- `streaming.py` - stream generated tokens for perceived latency
