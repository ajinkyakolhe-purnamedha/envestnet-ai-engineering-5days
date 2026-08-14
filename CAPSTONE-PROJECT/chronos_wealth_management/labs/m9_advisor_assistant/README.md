# M9 Lab Starter — Finish The Advisor Assistant

You implement the gate and the memory; the UI is given and already
wired. Build order is payoff-first — NOT deck order:

```text
submit_note_for_approval.py   YOU · 1   the gate's intake   (M9.4.1)
decide_note_draft.py          YOU · 2   the human decision  (M9.3.6)
answer_with_memory.py         YOU · 3   the memory seam     (M9.2.5)
judge_note_with_model.py      YOU · S   stretch: model judge (M9.3.3)
m8_reference_assistant.py     given     M8 stand-in for this lab
condense_conversation_history given     windowing helper
note_draft_queries.py         given     reads + row builder
model_loading.py              given     re-exported from M8
```

Your progress meter — 13 tests (+2 stretch, skipped until the judge
exists), green step by step:

```bash
cd CAPSTONE-PROJECT/chronos_wealth_management
uv run python -m pytest labs/m9_advisor_assistant -q
```

**The payoff is at step 2.** With submit and decide done, the loop
closes on screen: ask the assistant on the advisor dashboard, watch the
draft land in the approval queue, approve it — and the note appears on
Alice's investor dashboard. Reject one; Alice never sees it.

M9 includes a compact M8 reference assistant, so the lab and live UI run
even if your M8 lab is unfinished. Swapping in your own M8 workflow is a
stretch after M9 is green.

Full instructions: `SLIDES-markdown/m9-lab-instructions.md`.
