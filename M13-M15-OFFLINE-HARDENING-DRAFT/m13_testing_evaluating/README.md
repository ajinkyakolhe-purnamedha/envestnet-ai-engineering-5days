# M13 · Test and evaluate a real local-model application

**Thesis:** model behaviour is measured; Python-owned safety behaviour is proved.

Run from `CODEALONGS/`, so the existing `uv` environment and local weights are used:

```bash
uv run python ../M13-M15-OFFLINE-HARDENING-DRAFT/m13_testing_evaluating/00_live_local_golden_eval.py
uv run python ../M13-M15-OFFLINE-HARDENING-DRAFT/m13_testing_evaluating/01_test_malformed_output.py
uv run python ../M13-M15-OFFLINE-HARDENING-DRAFT/m13_testing_evaluating/02_test_evidence_and_approval.py
uv run python -m pytest ../M13-M15-OFFLINE-HARDENING-DRAFT/m13_testing_evaluating/03_pytest_contracts.py -q
```

| Card | Visible evidence | Teaching point |
| --- | --- | --- |
| 00 | local backend, model, latency, draft, golden-set score | Live model output is an evaluation boundary. |
| 01 | malformed proposals rejected | Generated text is untrusted input. |
| 02 | abstention and pending draft state | Evidence and human approval are deterministic product rules. |
| 03 | passing pytest contracts | Tests prove Python’s response to known failures. |

If local weights are unavailable, card 00 prints `local_model_unavailable`; it never substitutes a canned answer.
