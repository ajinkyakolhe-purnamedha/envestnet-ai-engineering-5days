from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, print_json


def run(retrieved_fact: str) -> str:
    request = {"instruction": "Use the supplied facts. Answer in one sentence.", "user_input": "Can AAPL be 36%?", "retrieved_fact": retrieved_fact, "format": "plain text"}
    print_json("Request parts", request)
    return chat([{"role": "system", "content": request["instruction"]}, {"role": "user", "content": f"Fact: {retrieved_fact}\nQuestion: {request['user_input']}"}], 35)


def main() -> None:
    print("35% fact:", run("AAPL has a maximum allocation of 35%."))
    print("40% fact:", run("AAPL has a maximum allocation of 40%."))


if __name__ == "__main__":
    main()
