# M1 answer key

1. A — A model is a probabilistic function inside a larger system.
2. A — Products require surrounding data, policy, UX, and operations.
3. A — Hosted and local paths shift infrastructure/control trade-offs.
4. A — Governance centralizes identity, policy, logging, and configuration.
5. A — Selection is a capability, economics, privacy, and operations decision.
6. A — Start with the least costly/slowest sufficient option and measure gaps.
7. A — The boundary should isolate provider-specific concerns.
8. A — Contracts and validation make variable output usable.
9. A — Secrets belong in protected runtime configuration.
10. A — Safe fallback and observability prevent false success.
11. It avoids an invalid provider call when configuration is missing and gives the caller a defined result.
12. Extract the intended text, handle missing/empty fields, normalize errors, and return the documented string contract.
13. The loading and generation APIs have different options. Reproduce the call with a tiny fixture, inspect the API boundary, and move the setting to model loading.
14. Keep the application-level function signature, message/response contract, fallback behavior, logging, and tests stable; swap only the provider adapter/configuration.
15. Example: accept role/content messages and return normalized text. Validate or review claims before action, and return a safe fallback when output is empty or violates policy.
