# M1 Capstone Lab · Advisor Portfolio Explanation Preview

You implement the first Day 1 feature inside Chronos Wealth: a bounded advisor
preview that explains deterministic portfolio facts.

```text
build_preview_messages.py   YOU   labelled instruction/context/question
call_preview_model.py       YOU   offline model boundary
draft_portfolio_preview.py  YOU   template fallback when no model
gather_preview_facts.py     given app plumbing
model_loading.py            given offline SmolLM2 loader
```

Progress meter:

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m1_advisor_preview -q
```

When your tests pass, `POST /advisor/clients/{id}/preview` returns a grounded
note in the **Advisor Preview (Day 1 Labs)** panel. No trade execution, no
retrieval, no durable memory.

**Safety boundary:** Python gathers facts; the model only explains supplied
numbers. When no model is available, a template note still cites portfolio
value, cash ratio, and deterministic recommendations.
