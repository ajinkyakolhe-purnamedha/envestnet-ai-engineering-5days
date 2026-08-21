# M3 · AI Application Patterns

M3 turns the M1 model capability and M2 call mechanics into one design rule:
choose the least-complex pattern that reliably solves the problem. Chronos is
the shared synthetic reference implementation, while the selection exercises
also cover support and document/private-knowledge workflows.

Each snippet is self-contained and has a short `Try:` block at the top. Run the
file first, then change the named input directly in the same file. The direct,
structured-output, and tiny-RAG snippets call local SmolLM; provider
credentials are not needed.

| Snippet | Teaches one thing | Try next |
| --- | --- | --- |
| `01_assemble_prompt.py` | separate prompt components | diagnose which component caused a failure |
| `02_direct_llm_call.py` | messages in, LLM reply out | why supplied facts are not present |
| `03_prompted_extraction.py` | typed extraction schema | malformed data and business validation |
| `04_simple_rag_architecture.py` | retrieve context, add it to prompt, answer | why M4 needs full RAG machinery |
| `05_choose_pattern.py` | first-rung selection | classify cross-workflow use cases |
| `06_test_contract.py` | one deterministic policy check | why an LLM cannot approve a numeric limit |

M4 owns RAG implementation, M6 owns fine-tuning, M7/M8 own agent runtimes,
and M13/M14 own evaluation and red teaming. This module chooses those paths;
it does not prematurely build them.
