# M15 · Observe, improve, and deploy a local-model workflow

**Thesis:** trace the whole run, repair the responsible layer, then serve the bounded workflow.

Run from `CODEALONGS/`:

```bash
for card in ../M13-M15-OFFLINE-HARDENING-DRAFT/m15_observability_deployment/0[0-4]_*.py; do uv run python "$card"; done
```

| Card | Evidence | Teaching point |
| --- | --- | --- |
| 00 | real model trace: run ID, backend, latency, evidence ID, outcome | Instrument the seam, not just a dashboard. |
| 01 | failed versus healthy trace | Diagnose the responsible layer. |
| 02 | same request before/after evidence repair | Measure improvement without violating safety. |
| 03 | validated, read-only API routes | Deployment is a controlled service boundary. |
| 04 | live `/health` plus 422 input validation | Smoke-test the real local API boundary. |

Start the service manually with:

```bash
uv run python -m uvicorn bounded_api:app --app-dir ../M13-M15-OFFLINE-HARDENING-DRAFT/m15_observability_deployment --port 8015
```

Trace only the minimum needed: run ID, model/backend, latency, evidence IDs, policy decision, status, and error code. Do not log secrets, raw prompts, or full portfolios. Alert on failed controls, latency/cost rise, quality regression, and abnormal tool use. Assign owners for the evaluation set, policy, runtime changes, and incidents.
