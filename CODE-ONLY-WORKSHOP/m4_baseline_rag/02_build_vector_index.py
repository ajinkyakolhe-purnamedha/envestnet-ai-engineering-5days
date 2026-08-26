import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chunks, embed


def main() -> None:
    text = "No single stock allocation may exceed 35 percent. Cash supports short-term liquidity. Advisors explain concentration risk."
    nodes = [{"id": i, "source": "policy.md", "text": part, "vector": embed(part)} for i, part in enumerate(chunks(text, 10, 2), 1)]
    with TemporaryDirectory() as directory:
        path = Path(directory) / "policy-index.json"
        path.write_text(json.dumps(nodes))
        loaded = json.loads(path.read_text())
        print("Persisted index:", path)
        print("Reloaded node count:", len(loaded), "vector dimensions:", len(loaded[0]["vector"]))


if __name__ == "__main__":
    main()
