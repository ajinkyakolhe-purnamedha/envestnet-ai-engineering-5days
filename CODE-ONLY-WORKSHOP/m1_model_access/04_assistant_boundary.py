import logging
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def answer_client_question(question: str) -> dict[str, object]:
    logging.info("advisor request: %s", question)
    started = time.perf_counter()
    answer = chat([{"role": "system", "content": "You are a concise advisor assistant."}, {"role": "user", "content": f"Portfolio: AAPL 20%, cash 80%.\n{question}"}], 50)
    return {"answer": answer, "model": "local-smollm", "latency_ms": round((time.perf_counter() - started) * 1000)}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    print_json("Application response", answer_client_question("What is the current AAPL allocation?"))


if __name__ == "__main__":
    main()
