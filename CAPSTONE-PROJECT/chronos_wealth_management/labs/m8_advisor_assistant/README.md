# M8 Lab Starter — Build The Advisor Assistant

You implement the five functions you learned this morning. The plumbing
you did *not* learn today (fact gathering, model loading) is given.

```text
route_client_question.py    YOU   the front door      (M8.2.3)
judge_against_guidelines.py YOU   Python's verdict    (M8.2.2)
draft_advisor_note.py       YOU   prose only          (M8.2.2)
review_advisor_note.py      YOU   the quality gate    (M8.2.5)
answer_client_question.py   YOU   the workflow        (M8.2.8)
gather_client_facts.py      given app plumbing
model_loading.py            given offline SmolLM2 loader
```

Your progress meter — 15 tests, green file by file:

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m8_advisor_assistant -q
```

Every stub raises `NotImplementedError` with a hint. Full instructions:
`SLIDES-markdown/m8-lab-instructions.md`.

**Your code is the feature.** The API endpoint
`POST /advisor/clients/{id}/assistant` serves THIS package — it answers
`501 — complete the M8 lab` until your stubs are implemented, and comes
alive when your tests go green.
