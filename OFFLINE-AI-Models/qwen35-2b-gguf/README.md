# Qwen3.5-2B GGUF · Ollama

Sharded weights in `shards/` ship with the repo. After `git clone`, run setup — no download step.

## Setup (once per machine)

```bash
ollama serve                         # terminal 1

cd OFFLINE-AI-Models/qwen35-2b-gguf
./setup_ollama.sh                    # terminal 2
```

`setup_ollama.sh` glues shards into one `.gguf` file, then runs `ollama create`.

**Why glue shards?** Git stores 14 files under 90 MB each. Ollama does **not**
read shards directly — `Modelfile` needs one `FROM ./….gguf` file. The combined
file is gitignored; students only commit/use `shards/`.

## Chat

**Ollama client** (direct)

```bash
uv run --project CODEALONGS python OFFLINE-AI-Models/qwen35-2b-gguf/ollama_chat.py
```

```python
import ollama

response = ollama.chat(
    model="qwen35-2b-chronos",
    messages=[{"role": "user", "content": "Your question here."}],
    think=False,
)

print(response["message"]["content"])
```

**LiteLLM** (same `completion()` shape as cloud providers)

```bash
uv run --project CODEALONGS python OFFLINE-AI-Models/qwen35-2b-gguf/litellm_ollama_chat.py
```

```python
from litellm import completion

response = completion(
    model="ollama/qwen35-2b-chronos",
    api_base="http://localhost:11434",
    messages=[{"role": "user", "content": "Your question here."}],
    think=False,
)

print(response.choices[0].message.content)
```

`think=False` — Qwen3.5 is a thinking model; without it, answers land in a
reasoning trace instead of `content`.
