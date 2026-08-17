# M1 advanced answer key

1. A — Contracts, validation, fallbacks, and telemetry make variable output usable.
2. A — One internal interface plus adapters supports governance and change.
3. A — Privacy benefits must be weighed against operational responsibility.
4. A — Start with measured quality/latency/cost sufficiency.
5. A — Provider mechanics belong in adapters.
6. A — Fail clearly and preserve control; do not invent or act.
7. A — Open selection includes family/license, size, hardware, and serving.
8. A — The surrounding engineering determines production value.
9. A — Enforce the contract and make the failure observable.
10. A — Enterprise viability includes service and budget constraints.
11. Callers receive a stable primitive contract and do not depend on provider SDK object shape; empty text is explicit.
12. Invalid input/authentication are generally non-transient and repeated retries add latency, cost, and noise. Retry only classified transient failures with limits.
13. In the provider/model adapter or normalization layer, not duplicated across business features.
14. Either can be defensible. Local improves data control but adds operations; hosted may simplify audit/operations but requires trust and data-governance controls. Pilot evidence on data classification, audit requirements, latency, cost, and operating capacity should decide.
15. Example: `call_model(messages, request_id) -> str`; timeout returns a controlled unavailable result; log request ID, model/deployment, latency, token usage, and outcome without logging secrets.
