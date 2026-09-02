"""M6 teaches fine-tuning as a Hugging Face training pipeline."""

from pathlib import Path
from runpy import run_path


ROOT = Path(__file__).resolve().parents[1]
M6 = ROOT / "m6_fine_tuning"
SLIDES = ROOT.parent / "SLIDES-markdown"
M6_DECK = SLIDES / "m6-fine-tuning.md"

SNIPPETS = [
    "01_huggingface_llm.py",
    "02_jsonl_dataset_format.py",
    "03_tokenize_and_mask_labels.py",
    "04_sft_trainer_dataset.py",
    "05_peft_lora_sft_trainer.py",
    "06_evaluate_and_save_adapter.py",
]


def test_m6_has_five_section_behavior_tuning_story() -> None:
    deck = M6_DECK.read_text()

    expected_sections = [
        "M6.1 · Why Fine-Tuning Exists",
        "M6.2 · Dataset And Chat Format",
        "M6.3 · Tokens, Labels, And Loss",
        "M6.4 · PEFT With LoRA And QLoRA",
        "M6.5 · Trainer And Accelerate",
        "M6.6 · Evaluate And Ship Adapter",
    ]
    for section in expected_sections:
        assert section in deck

    assert "RAG changes what the model knows" in deck
    assert "Fine-tuning changes how it behaves" in deck
    assert "dataset is the project" in deck.lower()
    assert "base + prompt" in deck
    assert "Prompt -> few-shot -> RAG -> fine-tune" in deck
    assert "SFTTrainer" in deck
    assert "Accelerate" in deck
    assert "LoraConfig" in deck
    assert "ship an adapter" in deck
    assert "rollback" in deck
    assert "validation loss rising" in deck
    assert "overfitting" in deck


def test_m6_deck_references_ordered_runnable_snippets() -> None:
    deck = M6_DECK.read_text()

    numbered_files = sorted(path.name for path in M6.glob("[0-9][0-9]_*.py"))
    assert numbered_files == SNIPPETS

    for snippet in SNIPPETS:
        assert f"CODEALONGS/m6_fine_tuning/{snippet}" in deck
        assert (M6 / snippet).exists()

    readme = (M6 / "README.md").read_text()
    for snippet in SNIPPETS:
        assert snippet in readme


def test_m6_final_adapter_snippet_stays_cookbook_sized() -> None:
    source = (M6 / "06_evaluate_and_save_adapter.py").read_text()
    assert len(source.splitlines()) <= 80
    assert "score_one" in source
    assert "ADAPTER_DIR" in source
    assert "PeftModel.from_pretrained" in source
    assert "adapter_outputs = targets" not in source


def test_m6_lora_card_runs_a_real_training_step() -> None:
    source = (M6 / "05_peft_lora_sft_trainer.py").read_text()

    assert "trainer.train()" in source
    assert "intentionally not called" not in source
    assert "lora_weight_change" in source
    assert "trainer.save_model" in source


def test_m6_huggingface_llm_snippet_calls_model_directly() -> None:
    source = (M6 / "01_huggingface_llm.py").read_text()
    assert "AutoModelForCausalLM" in source
    assert "model.generate" in source
    assert "torch.no_grad" not in source


def test_m6_numbered_snippets_run_and_expose_key_outputs() -> None:
    for snippet in SNIPPETS:
        module = run_path(M6 / snippet)
        assert module["__doc__"]

    llm = run_path(M6 / "01_huggingface_llm.py")
    assert llm["model_name"]

    dataset = run_path(M6 / "02_jsonl_dataset_format.py")
    assert len(dataset["dataset"]) == 8

    labels = run_path(M6 / "03_tokenize_and_mask_labels.py")
    assert -100 in labels["labels"]
    assert any(label != -100 for label in labels["labels"])

    trainer = run_path(M6 / "04_sft_trainer_dataset.py")
    assert trainer["trainer"].train_dataset is not None

    lora = run_path(M6 / "05_peft_lora_sft_trainer.py")
    assert lora["trainer"].model.peft_config is not None
    assert lora["trainable_percent"] < 5.0
    assert lora["train_result"].global_step >= 1
    assert lora["lora_weight_change"] > 0

    shipped = run_path(M6 / "06_evaluate_and_save_adapter.py")
    assert shipped["adapter_dir"].exists()
    assert len(shipped["base_outputs"]) == len(shipped["adapter_outputs"])
    assert shipped["loaded_outputs"] == shipped["adapter_outputs"]
