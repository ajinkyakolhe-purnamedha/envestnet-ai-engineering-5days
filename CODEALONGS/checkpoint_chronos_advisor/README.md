# Chronos Advisor Checkpoint

Build a small educational assistant for Alice, the Chronos demo investor in 90 minutes.
You will rebuild three ideas from the course:

1. **Chat** — use Alice's trusted portfolio facts and keep only recent history.
2. **Evidence** — retrieve one policy passage and answer from that evidence.
3. **One-turn agent** — let the model choose one read-only tool, validate its
   request, then show the tool trace.

This is educational software only. It cannot trade, access another client,
or turn missing policy evidence into a fact.

## Timebox

| Stage | Time |
| --- | ---: |
| Chat | 20 minutes |
| Evidence | 25 minutes |
| One-turn agent | 30 minutes |
| Run checks and reflect | 15 minutes |

MCP comes later. This checkpoint keeps its tools in the same Python process.

## Run

From `CODEALONGS/`:

```bash
uv run python -m checkpoint_chronos_advisor.starter
uv run --extra courseware python -m pytest tests/test_checkpoint_chronos_advisor.py -q
```

Use the test output as the progress meter. The tests use a mocked model on
purpose, so they prove the application boundaries without waiting for a local
model generation.

## Exit criteria

- Your chat sends trusted Alice facts and only four retained history messages.
- A concentration question returns the policy evidence containing `35%`.
- An unsupported policy question returns `Not found in the supplied investment policy.`
- The agent permits only `get_portfolio_summary` and `search_investment_policy`.
- A request for Bob's portfolio is denied before the tool runs.
- Your printed trace shows the model decision, validation, tool result, and final answer.

## Reflection

Which parts are deterministic application code? Which parts depend on model
behaviour? Why is the tool allowlist more reliable than telling the model not
to overreach?
