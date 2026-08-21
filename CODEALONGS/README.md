# CODEALONGS — the workshop code-along project

One `uv` project holding the code participants run along with the decks,
the labs, and the material-consistency tests that keep the courseware
honest. One top-level folder per module, matching the decks in
`SLIDES-markdown/`:

| Day | Modules | Folders |
| --- | --- | --- |
| 1 | M0–M3 | `m0_python_foundations/` · `m1_model_access/` · `m2_model_tokens_context/` · `m3_application_patterns/` |
| 2 | M4–M6 | `m4/` (RAG) · `m5/` (retrieval evaluation) · `m6/` (fine-tuning) |
| 3 | M7–M9 | `m7/` (agent loop) · `m8/` (frameworks) · `m9/` (memory, verification, HITL) |

## The module format

Each module folder contains:

- **Numbered snippets** (`01_…py`, `02_…py`, …) — one visible idea per file,
  small enough to read on a slide; run them in filename order. The decks
  quote these files, so the code here is the source of truth.
- **`README.md`** — a "snippet → one essential idea" table.
- **A setup helper** (`*_setup.py`) — swaps in the local offline models so
  everything runs without downloads or credentials.
- **`lab/`** — `README.md`, `mini_lab.*`, `starter.*`, `hints.md`, and an
  instructor solution. Present for m1–m3; m4–m9 labs are coming later.

m0 and m1 additionally keep paired code-along notebooks
(`NN+1_thing_code_along.ipynb`, whose first cell is `run_path("NN_thing.py")`)
as the gentler day-one on-ramp. m2 onward is snippets-only by design.

m0 is itself split into three sequential sections
(`01_share_purchase/`, `02_packages_and_model_access/`, `03_wealth_demo/`).

Shared folders: `data/` (synthetic prices, portfolio, policy files) and
`tests/` (material tests, one file per module — see below).

## Install and run

From the `CODEALONGS/` folder:

```bash
uv sync --extra courseware
uv run python m2_model_tokens_context/06_text_to_token_ids.py
uv run python m4/01_why_rag_exists.py
uv run --extra courseware jupyter lab     # for the m0/m1 notebooks
```

Run everything from `CODEALONGS/` unless a module README says otherwise.
The M0.3 wealth demo has its own unittest suite and server — see its README.

## Offline behaviour

The model examples degrade gracefully: with no `MODEL_ENDPOINT` /
`MODEL_API_KEY` / `MODEL_NAME` set they return a labelled offline response,
and `COURSEWARE_OFFLINE=1` skips all external calls. The M1 cloud examples
read `GEMINI_API_KEY`, `GOOGLE_CLOUD_PROJECT`, and `HF_TOKEN` from the
untracked repo-root `.env`. Local weights live in `../OFFLINE-AI-Models/`.

## Material tests

`tests/` doesn't test an application — it tests the materials: that each
snippet runs, behaves the way its deck claims, and that the decks'
`Source:` pointers reference real files.

```bash
uv run pytest                                     # everything
uv run pytest tests/test_m2_materials.py -k trim  # one test
```

Extend the matching test file when you change a module.

All prices, portfolios, and policies here are deterministic synthetic
educational data. These materials do not provide financial advice.
