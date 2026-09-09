# M14 · Harness, contain, and red-team an AI application

**Thesis:** a harness is enforceable Python around an uncertain model; red-team evidence proves what it contains.

Run from `CODEALONGS/`:

```bash
for card in ../M13-M15-OFFLINE-HARDENING-DRAFT/m14_harness_redteaming/0[0-4]_*.py; do uv run python "$card"; done
```

| Card | Evidence | Teaching point |
| --- | --- | --- |
| 00 | actual local-model response and latency | Injection text can reach a model; generated text remains untrusted. |
| 01 | failure → remedy map | Diagnose before tuning a prompt. |
| 02 | denied tool request, no result | Admit/scope before a data read. |
| 03 | contained repeated request | Bound valid-looking work. |
| 04 | repeatable attack outcomes and audit IDs | Preserve attacks as regression evidence. |

This is **application-level containment**, not an OS/process/filesystem/network sandbox. It teaches capability admission, schema validation, client scope, bounded results, step limits, and audit evidence.
