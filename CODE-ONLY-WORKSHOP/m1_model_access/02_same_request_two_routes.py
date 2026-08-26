import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def call_openai_compatible(messages: list[dict[str, str]]) -> str | None:
    base_url, api_key, model = (os.getenv(name) for name in ("OPENAI_BASE_URL", "OPENAI_API_KEY", "OPENAI_MODEL"))
    if not all((base_url, api_key, model)):
        print("Hosted call skipped: set OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL.")
        return None
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps({"model": model, "messages": messages}).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def main() -> None:
    messages = [{"role": "user", "content": "Explain one benefit of local inference."}]
    print("Local answer:", chat(messages, 40))
    hosted = call_openai_compatible(messages)
    if hosted is not None:
        print("Hosted answer:", hosted)


if __name__ == "__main__":
    main()
