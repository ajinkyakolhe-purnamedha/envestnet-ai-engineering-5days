# Instructor solution · Chronos selection clinic

| Candidate | Pattern | Why not simpler | First deterministic test |
| --- | --- | --- | --- |
| Portfolio-note explainer | Direct call | The note already supplies the facts; no response contract is required. | Every supplied number appears in the draft. |
| Support-ticket hand-off | Prompted application | Free-form prose is unsafe for a downstream system. Instructor/Pydantic make shape explicit. | A missing priority, owner, or next step is rejected. |
| Policy Q&A | RAG | The facts are private and change; a model's general language capability cannot supply a governed answer. | Returned answer cites the synthetic retrieved chunk. |

**Instructor only:** model tier is a starting hypothesis. The first test and
observed quality/cost/latency evidence decide whether a change is justified.
