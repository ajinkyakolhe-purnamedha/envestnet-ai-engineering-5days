#!/usr/bin/env bash
cd "$(dirname "$0")"
[[ -f shards/Qwen3.5-2B-Q4_K_M.gguf.shard-000 ]] || { echo "missing shards/ — use a full git clone"; exit 1; }

cat shards/Qwen3.5-2B-Q4_K_M.gguf.shard-* > Qwen3.5-2B-Q4_K_M.gguf   # shards → one file
ollama rm qwen35-2b-chronos 2>/dev/null || true                     # safe to re-run
ollama create qwen35-2b-chronos -f Modelfile                        # register local model
