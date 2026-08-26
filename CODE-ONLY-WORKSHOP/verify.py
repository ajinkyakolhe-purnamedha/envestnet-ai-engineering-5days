from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent
MODULES = [
    "m1_model_access", "m2_tokens_and_context", "m3_application_patterns",
    "m4_baseline_rag", "m5_advanced_rag", "m6_fine_tuning",
    "m7_agentic_llms", "m8_agentic_frameworks", "m9_finishing_agentic_apps",
]


def main() -> None:
    missing = [name for name in MODULES if not (ROOT / name).is_dir()]
    wrong_counts = [
        name for name in MODULES
        if (ROOT / name).is_dir() and len(list((ROOT / name).glob("[0-9][0-9]_*.py"))) != 5
    ]
    non_python = [
        path for path in ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".py"
    ]
    assert not missing, f"Missing module directories: {missing}"
    assert not wrong_counts, f"Modules need exactly five snippets: {wrong_counts}"
    assert not non_python, f"Teaching tree must contain only Python: {non_python}"
    for path in ROOT.rglob("[0-9][0-9]_*.py"):
        source = path.read_text()
        assert "def main()" in source and "__main__" in source, path
    print("structure: 9 modules × 5 executable snippets")
    if "--live" in sys.argv:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "m1_model_access" / "01_local_model_call.py")],
            check=True, text=True, capture_output=True,
        )
        assert "Generated answer:" in completed.stdout
        print("live local model call: non-empty generated response")


if __name__ == "__main__":
    main()
