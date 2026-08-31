# Offline model bundle

This repository is structured so **every committed file stays below GitHub's 100 MB
file limit** — no Git LFS, no Hugging Face download at clone time. Large models are
stored as **shards** (safetensors, GGUF, or ONNX); participants rejoin them locally
when a tool needs one monolithic file (e.g. `setup_ollama.sh` for Ollama).

## Committed in git

| Folder | Model | Used by |
|--------|-------|---------|
| `smollm2-135m-instruct/` | SmolLM2-135M-Instruct (sharded safetensors) | M0–M9 transformers / LlamaIndex / M6 |
| `bge-small-en-v1.5-onnx/` | BGE-small-en-v1.5 (quantized ONNX) | M4–M5 embeddings |
| `qwen35-2b-gguf/shards/` | Qwen3.5-2B Q4_K_M (sharded GGUF) | Ollama + LiteLLM |

Each shard is under 90 MB.

### Qwen3.5 — shards are in git; register with Ollama after clone

```bash
ollama serve   # separate terminal
cd OFFLINE-AI-Models/qwen35-2b-gguf
./setup_ollama.sh
uv run --project CODEALONGS python OFFLINE-AI-Models/qwen35-2b-gguf/ollama_chat.py
```

## On-demand only (not in git)

SmolLM2-1.7B for M8: `CODEALONGS/m8_agentic_frameworks/download_local_models.py`
