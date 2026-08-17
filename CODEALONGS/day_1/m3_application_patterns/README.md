# M3 · AI Application Patterns

M3 turns the M1 model capability and M2 call mechanics into one design rule:
choose the least-complex pattern that reliably solves the problem. Chronos is
the shared synthetic reference implementation, while the selection exercises
also cover support and document/private-knowledge workflows.

Each code-along begins by running its exact cookbook snippet with `run_path`.
Then it introduces a controlled fake output or small synthetic data so
participants can inspect one decision without needing a provider key.

| Cookbook snippet | Teaches one thing | Code-along then explores |
| --- | --- | --- |
| `01_assemble_prompt.py` | separate prompt components | diagnose which component caused a failure |
| `03_base_call.py` | direct language capability | why supplied facts are not present |
| `05_prompted_extraction.py` | typed extraction schema | malformed data and business validation |
| `07_choose_pattern.py` | first-rung selection | classify cross-workflow use cases |
| `09_test_contract.py` | one deterministic policy check | why an LLM cannot approve a numeric limit |

M4 owns RAG implementation, M6 owns fine-tuning, M7/M8 own agent runtimes,
and M13/M14 own evaluation and red teaming. This module chooses those paths;
it does not prematurely build them.
