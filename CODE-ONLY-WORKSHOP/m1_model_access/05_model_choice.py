from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat


def choose_model_route(case: dict[str, object]) -> str:
    if case["sensitive"] or not case["online"]:
        return "local model: private/offline constraint"
    if case["quality"] == "highest":
        return "hosted model: strongest managed capability"
    return "local model: smallest sufficient route"


def main() -> None:
    cases = [
        {"name": "private policy", "sensitive": True, "online": True, "quality": "standard"},
        {"name": "public research", "sensitive": False, "online": True, "quality": "highest"},
        {"name": "air-gapped help", "sensitive": False, "online": False, "quality": "standard"},
    ]
    for case in cases:
        print(case["name"], "->", choose_model_route(case))
    print("Local demonstration:", chat([{"role": "user", "content": "Give one reason to choose a smaller model."}], 35))


if __name__ == "__main__":
    main()
