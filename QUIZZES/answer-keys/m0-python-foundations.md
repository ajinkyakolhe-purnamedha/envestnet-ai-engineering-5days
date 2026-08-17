# M0 answer key

1. A — Python combines readable code with a broad engineering ecosystem.
2. A — Declared dependencies make environments reproducible.
3. A — Validate at the boundary before persistence or action.
4. A — Functions create reusable, independently testable units.
5. A — Classes help group related state and operations.
6. A — SQLite provides durable local persistence.
7. A — An endpoint contract includes inputs, outputs, and errors.
8. A — Deterministic unit tests fit pure calculations.
9. A — Structured logs support search and diagnosis.
10. A — Check project layout, launch location, and import path first.
11. Zero shares raises `ValueError`; positive inputs return `805.0`.
12. The return-type contract is broken. Normalize or change the implementation at the function boundary, then keep the test aligned with the intended numeric contract.
13. Examples: current working directory, virtual environment/interpreter, environment variables, package installation, or server startup command.
14. Build and test calculation/validation first, then storage, then the HTTP layer. Test invalid input at the validation boundary, persistence round-trip in storage, and response/error shape at the endpoint.
15. Example: `get_portfolio_summary(account_id: str) -> PortfolioSummary`; test an unknown account or unavailable price source and verify a defined error rather than an invented summary.
