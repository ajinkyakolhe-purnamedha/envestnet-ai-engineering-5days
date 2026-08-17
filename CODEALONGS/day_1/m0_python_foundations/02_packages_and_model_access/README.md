# M0.2 — Packages And Model Access

Each file teaches one move. Run from the repository root so the local model
path resolves.

```bash
uv sync --project CODEALONGS --extra courseware
uv run --project CODEALONGS python \
  CODEALONGS/day_1/m0_python_foundations/02_packages_and_model_access/02_huggingface_offline.py
uv run --project CODEALONGS python \
  CODEALONGS/day_1/m0_python_foundations/02_packages_and_model_access/03_gemini_api.py
uv run --project CODEALONGS jupyter lab CODEALONGS/day_1/m0_python_foundations/02_packages_and_model_access
```

The Hugging Face example needs the committed `OFFLINE-AI-Models` folder. The
Gemini example needs a root `.env` file containing
`GEMINI_API_KEY=your-key`; it deliberately makes one hosted call.
