# Chronos Advisor Checkpoint

Build a small educational assistant for Alice, the Chronos demo investor in one
hour. You will rebuild three ideas from the course:

1. **Chat** — use Alice's trusted portfolio facts and keep only recent history.
2. **Evidence** — retrieve one policy passage and answer from that evidence.
3. **Bounded agent** — let a framework agent use two read-only tools and show
   the tool trace.

This is educational software only. It cannot trade, access another client,
or turn missing policy evidence into a fact.

## Timebox

| Stage | Time |
| --- | ---: |
| Read the reference cards | 10 minutes |
| Chat | 10 minutes |
| Evidence | 15 minutes |
| Bounded agent | 20 minutes |
| Check and reflect | 5 minutes |

MCP comes later. This checkpoint keeps its tools in the same Python process.
Its policy document, local model setup, and RAG support all live inside this
folder; it does not import M4 courseware.

## Run

Students: begin with [lab/README.md](lab/README.md). The numbered scripts are
completed reference snapshots; `lab/starter.py` is the integration exercise.

From `CODEALONGS/`:

```bash
uv run --extra courseware python checkpoint_chronos_advisor/lab/starter.py
uv run --extra courseware python -m pytest tests/test_checkpoint_chronos_advisor.py -q
```

Run `01_direct_investor_chat.py`, then `02_policy_evidence_rag.py`, then
`03_advisor_agent_with_rag_tool.py`. The first two use the real local 135M
model. The framework agent uses M8's explicitly labelled `ClassroomModel` for
tool-call shape because 135M does not reliably emit function-call JSON.

## Exit criteria

- Your chat sends trusted Alice facts and only four retained history messages.
- A concentration question returns the policy evidence containing `35%`.
- The agent has only `portfolio_summary` and `policy_rag`, with `max_steps=3`.
- A request for another client is denied by the portfolio tool.
- Your printed trace shows the two tool calls and the final result.

## Reflection

Which parts are deterministic application code? Which parts depend on model
behaviour? Why is the tool allowlist more reliable than telling the model not
to overreach?
