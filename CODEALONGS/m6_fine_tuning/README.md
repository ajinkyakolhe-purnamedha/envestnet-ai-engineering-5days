# M6 Codealongs

M6 uses six simple scripts:

| Script | Teaches |
| --- | --- |
| `01_huggingface_llm.py` | load and call an LLM with Hugging Face `transformers` |
| `02_jsonl_dataset_format.py` | JSONL examples and chat-template text for fine-tuning |
| `03_tokenize_and_mask_labels.py` | token IDs, labels, and `-100` prompt masking |
| `04_sft_trainer_dataset.py` | send formatted examples to TRL `SFTTrainer` |
| `05_peft_lora_sft_trainer.py` | train only LoRA adapter weights with PEFT + `SFTTrainer` |
| `06_evaluate_and_save_adapter.py` | evaluate outputs and save/load the adapter artifact |

Run from `CODEALONGS`:

```bash
uv run python m6_fine_tuning/01_huggingface_llm.py
```
