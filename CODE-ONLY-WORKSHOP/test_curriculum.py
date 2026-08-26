from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parent
MODULES = [
    "m1_model_access",
    "m2_tokens_and_context",
    "m3_application_patterns",
    "m4_baseline_rag",
    "m5_advanced_rag",
    "m6_fine_tuning",
    "m7_agentic_llms",
    "m8_agentic_frameworks",
    "m9_finishing_agentic_apps",
]


def test_curriculum_has_nine_modules_with_five_snippets_each() -> None:
    module_dirs = [ROOT / name for name in MODULES]

    assert all(folder.is_dir() for folder in module_dirs)
    assert all(len(list(folder.glob("[0-9][0-9]_*.py"))) == 5 for folder in module_dirs)


def test_teaching_tree_contains_python_only() -> None:
    files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]

    assert files
    assert all(path.suffix == ".py" for path in files)
