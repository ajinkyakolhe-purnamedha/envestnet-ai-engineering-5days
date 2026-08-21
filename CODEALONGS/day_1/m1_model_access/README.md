# M1 · Model Access

These materials continue the M0 contract: each numbered notebook starts by
running its paired, deliberately small Python snippet. The notebook then adds
questions and controlled complexity.

Run from the repository root:

```bash
uv run --project CODEALONGS --extra courseware jupyter lab
```

Three pairs form the learning path; the fourth is an epilogue about where a
model call lives once your organisation owns it.

| Pair | One essential idea |
|---|---|
| 01–02 | Three proprietary SDKs, one identical call shape |
| 03–04 | Run an open-weight model from local files, with no network |
| 05–06 | Put the model behind a small, logged application boundary |
| 07–08 | *Later:* the same call through a governed cloud boundary |

## Keys, and what runs without them

Nothing in pairs 03–06 needs a key or a network — the local SmolLM weights are
committed to `OFFLINE-AI-Models/`. Pair 01 reports which hosted providers are
configured, and pair 07 is a governed-cloud epilogue.

| Variable | Used by | Where it comes from |
|---|---|---|
| `GEMINI_API_KEY` | pairs 01–02 | the repository `.env` |
| `OPENAI_API_KEY` | pair 01–02 | the repository `.env` |
| `ANTHROPIC_API_KEY` | pair 01–02 | the repository `.env` |
| `GOOGLE_CLOUD_PROJECT` | pair 07–08 | an authenticated Google Cloud identity |
| `HF_TOKEN` | pair 07–08 | a Hugging Face account |

Pair 05–06 calls the local SmolLM model through the same application boundary
the lab later extends.

## Lab

`lab/` is the module exercise. It starts from the pair 05–06 assistant and adds
the two things that snippet leaves out — conversation history, and a safe
response when the model returns no usable text — proven by two tests that never
call a provider.
