# M0 advanced answer key

1. A — Duplication creates behavioral drift.
2. A — Reproducible dependencies address the CI failure.
3. A — Shared callers need one domain/application validation boundary.
4. A — Pure calculation and persistence remain independently testable.
5. A — Clients need a reliable success/error distinction.
6. A — Unit tests give fastest feedback at the rule boundary.
7. A — Scale and concurrency changed the persistence requirements.
8. A — Operational metadata supports diagnosis without secret leakage.
9. A — Environment/interpreter/path differences explain the symptom.
10. A — Deterministic rules need deterministic execution and tests.
11. It accepts invalid or nonsensical domain inputs unless the domain allows all values. For example, validate numeric finiteness, required price semantics, or whether the old price can be zero.
12. Shared mutable state or an aliasing/copying issue; inspect whether the function returns a shared list/object instead of a fresh value.
13. Persistence/reload behavior and the storage-to-domain boundary.
14. Example invariant: no holding with non-positive shares or price is persisted. A database write failure or invalid input must return an explicit failure, never a successful purchase response.
15. Example: return account ID, holdings, valuation timestamp, and source status; reject or mark the summary unavailable when prices are stale beyond the feature’s policy.
