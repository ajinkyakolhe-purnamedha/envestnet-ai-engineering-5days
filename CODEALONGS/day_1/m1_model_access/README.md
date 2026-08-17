# M1 · Model Access

These materials continue the M0 contract: each numbered notebook starts by
running its paired, deliberately small Python snippet. The notebook then adds
questions and controlled complexity.

Run from the repository root:

```bash
uv run --project CODEALONGS --extra courseware jupyter lab
```

Set `GEMINI_API_KEY` in the repository `.env` for the direct Gemini example.
The Vertex example additionally needs an authenticated Google Cloud identity and
`GOOGLE_CLOUD_PROJECT`. The hosted open-weight example needs `HF_TOKEN`.

| Pair | One essential idea |
|---|---|
| 01–02 | Call a proprietary model through the Gemini API |
| 03–04 | Call Gemini through the Vertex AI cloud boundary |
| 05–06 | Call a hosted open-weight model and explore modalities |
| 07–08 | Run the cohort model entirely locally |
| 09–10 | Put a model call behind a small, logged application boundary |
