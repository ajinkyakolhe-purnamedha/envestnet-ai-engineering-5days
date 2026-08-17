# M3 answer key

1. A — Keep instruction, context, question, and history diagnostically separate.
2. B — Selection starts with requirements and operating constraints.
3. A — Family-level properties shape the application decision.
4. A — Size affects capability and resource demand.
5. A — Closed services move operations to an HTTP/provider boundary and usage billing.
6. A — A direct call is the first rung.
7. A — Structured output adds a typed response shape.
8. A — RAG supplies relevant external/private/current facts.
9. A — Shape validity is not policy validity.
10. A — Use the least-complex reliable pattern and document the argument.
11. It returns `prompt` because `format` is checked after the RAG conditions and before the default `base` result; there is no private/current-facts requirement.
12. A deterministic business-policy validation check.
13. Ask whether the requirement truly needs dynamic multi-step decisions and tools; if not, a direct call or prompted application is simpler and easier to test.
14. Private/current policy facts → RAG because the data must be retrieved; fixed format → prompted structured output because shape is the requirement; multi-step tool loop → agentic workflow because dynamic steps are required. Explain the failed simpler alternative for each.
15. Example: prompted structured output or a direct call plus deterministic validation, depending on whether typed extraction is needed. Contract: reject any trade intent outside the allowed symbol/allocation/risk policy before execution. Evidence: required output shape, data boundary, latency/cost target, and a test showing the policy boundary.
