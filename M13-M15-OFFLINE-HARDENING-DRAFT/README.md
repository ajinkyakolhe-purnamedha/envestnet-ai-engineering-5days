# M13–M15 · Offline hardening draft

This isolated draft is intentionally separate from the existing curriculum folders. It contains three 40-minute modules that reuse the repository’s pre-downloaded Hugging Face model runtime without requiring network access, secrets, Ollama, or hosted APIs.

```text
M13 test and evaluate → M14 attack and contain → M15 trace, improve, and serve
```

Run all cards from `CODEALONGS/` using the commands in each module README. The live cards perform actual local inference. If local weights are unavailable, they report `local_model_unavailable` rather than returning a fake success.

The dense teaching outlines live in `slides/`. The isolated material checks run with:

```bash
cd CODEALONGS
uv run python -m pytest ../M13-M15-OFFLINE-HARDENING-DRAFT/tests -q
```

Chronos data remains synthetic and educational. The LLM drafts language only; Python retains facts, calculations, policy, permissions, execution, audit, and approval.
