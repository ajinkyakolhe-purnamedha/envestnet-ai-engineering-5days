---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M6.0 · LLM Fine-Tuning

M4/M5 taught custom knowledge with RAG.

M6 teaches custom behavior with fine-tuning.

By the end of this module, you can:

- prepare instruction/chat data
- tokenize examples and mask labels
- attach LoRA or QLoRA adapters with PEFT
- configure TRL `SFTTrainer`
- launch training through Accelerate
- evaluate and ship the adapter

<!--
Thesis: fine-tuning is a pipeline, not a magic training command. The dataset is
the project; the training run is the shortest part.
-->

---

# M6.1 · Why Fine-Tuning Exists

RAG changes what the model knows.

Fine-tuning changes how it behaves.

Good fine-tuning targets:

- strict output format
- task-specific style
- repeated classification or extraction shape
- lower-latency small-model behavior

Source: `CODEALONGS/m6_fine_tuning/01_huggingface_llm.py`

<!--
Use generic support-ticket JSON here so the code teaches fine-tuning mechanics,
not a wealth demo. Wealth can still come back in the lab.
-->

---

# M6.1 · Try Them In This Order

```text
Prompt -> few-shot -> RAG -> fine-tune
```

| Step | Use it when |
| --- | --- |
| prompt | the task is new or one-off |
| few-shot | the format is close but inconsistent |
| RAG | the missing part is knowledge |
| fine-tune | measured behavior is still unreliable |

Fine-tuning is the fourth tool, not the first instinct.

<!--
This prevents the expensive mistake: training because the team has not measured
whether a cheaper intervention already solves the failure.
-->

---

# M6.2 · Dataset And Chat Format

Fine-tuning starts with examples:

```json
{"instruction": "...", "input": "...", "output": "..."}
```

Each row describes the behavior the model should repeat.

Source: `CODEALONGS/m6_fine_tuning/02_jsonl_dataset_format.py`

<!--
The dataset is the project. If rows are inconsistent, training faithfully
learns inconsistency.
-->

---

# M6.2 · Chat Template

Instruction rows become chat messages:

```python
[
  {"role": "system", "content": "..."},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."},
]
```

Then the tokenizer renders the model-specific text.

Source: `CODEALONGS/m6_fine_tuning/02_jsonl_dataset_format.py`

<!--
Do not hand-roll the final prompt string if the tokenizer has a chat template.
The template is part of the model contract.
-->

---

# M6.2 · Hold Out Eval First

Split before training:

```text
all examples -> train set + held-out eval set
```

The eval set is how you know whether the adapter helped.

Source: `CODEALONGS/m6_fine_tuning/02_jsonl_dataset_format.py`

<!--
If learners look at eval rows while iterating on the dataset, the eval is no
longer held out. Say it plainly.
-->

---

# M6.3 · Tokens, Labels, And Loss

The trainer does not learn from strings.

It learns from:

- `input_ids`
- `attention_mask`
- `labels`

Source: `CODEALONGS/m6_fine_tuning/03_tokenize_and_mask_labels.py`

<!--
This is the M2 token lesson applied to training. The text is only the source;
tokens and labels are what reach the model.
-->

---

# M6.3 · Completion-Only Loss

For instruction tuning, train the answer.

Prompt tokens get label `-100`.

Completion tokens keep their token IDs as labels.

Source: `CODEALONGS/m6_fine_tuning/03_tokenize_and_mask_labels.py`

<!--
This is the silent bug worth spending time on. Without masking, the model
spends capacity learning to copy prompts.
-->

---

# M6.4 · PEFT With LoRA And QLoRA

PEFT freezes the base model and trains adapters.

`LoraConfig` defines:

- rank `r`
- `lora_alpha`
- dropout
- target modules

Source: `CODEALONGS/m6_fine_tuning/05_peft_lora_sft_trainer.py`

<!--
PEFT is the right library for this section. Use the real config object, not a
dictionary pretending to be one.
-->

---

# M6.4 · Prepare Model For LoRA

`get_peft_model()` wraps the base model.

After wrapping:

- base weights stay frozen
- adapter weights are trainable
- trainable parameter count drops sharply

Source: `CODEALONGS/m6_fine_tuning/05_peft_lora_sft_trainer.py`

<!--
The snippet uses a tiny in-memory model so it runs fast. The PEFT mechanism is
the same one used on a real base model.
-->

---

# M6.4 · QLoRA

QLoRA quantizes the frozen base model:

```python
BitsAndBytesConfig(load_in_4bit=True)
```

The LoRA adapters still train in higher precision.

Source: `CODEALONGS/m6_fine_tuning/05_peft_lora_sft_trainer.py`

<!--
Treat this as GPU training shape. bitsandbytes 4-bit loading is not a Mac
classroom requirement.
-->

---

# M6.5 · Trainer And Accelerate

`SFTConfig` holds the knobs:

- learning rate
- epochs
- batch size
- gradient accumulation
- eval/save strategy
- max sequence length

Source: `CODEALONGS/m6_fine_tuning/04_sft_trainer_dataset.py`

<!--
Use TRL for SFT because it is the right trainer for language-model supervised
fine-tuning.
-->

---

# M6.5 · SFTTrainer With PEFT

`SFTTrainer` wires the pieces together:

```text
model + tokenizer + dataset + SFTConfig + LoraConfig
```

Source: `CODEALONGS/m6_fine_tuning/04_sft_trainer_dataset.py`

The snippet constructs the trainer but does not call `trainer.train()`.

<!--
This is how to build the training job. Running the full training loop is a lab
or GPU-box concern, not a slide snippet requirement.
-->

---

# M6.5 · Accelerate

Trainer uses Accelerate under the hood.

Accelerate owns:

- device placement
- mixed precision
- distributed launch
- FSDP / DeepSpeed integration when needed

```bash
accelerate launch train_sft.py
```

<!--
The key operational command is `accelerate launch train_sft.py`. The Python
snippet shows the concept without requiring a multi-GPU machine.
-->

---

# M6.5 · Watch Validation Loss

Training loss falling means the optimizer is working.

validation loss rising means overfitting.

| Curve | Meaning |
| --- | --- |
| training loss down | model fits training rows |
| validation loss down | model improves on held-out rows |
| validation loss up | stop; it is memorizing |

The best checkpoint is rarely the last checkpoint.

<!--
This slide is intentionally separate from config. Learners need to diagnose a
run, not only write a config object.
-->

---

# M6.6 · Evaluate And Ship Adapter

Fine-tune evidence is not "sounds better."

Score held-out outputs:

- parses
- schema valid
- exact match
- required phrase present when needed

Source: `CODEALONGS/m6_fine_tuning/06_evaluate_and_save_adapter.py`

Always compare against base + prompt.

<!--
If base + prompt wins, ship the prompt. The adapter has to earn deployment.
-->

---

# M6.6 · What Ships

You ship an adapter, not a full new model.

That means:

- save adapter directory
- load it onto the base model
- version one adapter per task
- rollback by loading the previous adapter

Source: `CODEALONGS/m6_fine_tuning/06_evaluate_and_save_adapter.py`

<!--
This is the deployment payoff of PEFT. The artifact is small, inspectable,
versionable, and reversible.
-->

---

<!-- _class: lead -->

# M6.L · Lab

Build a small support-ticket classifier adapter:

1. Load JSONL examples.
2. Render chat text.
3. Split train/eval.
4. Attach LoRA.
5. Build `SFTTrainer`.
6. Run training only if the model/GPU is available.
7. Score base + prompt vs adapter.

Done when the ship/no-ship decision is backed by eval metrics.

<!--
The lab can swap in Chronos data later. The pipeline remains identical.
-->

---

<!-- _class: lead -->

# M6 Close

Fine-tuning workflow:

```text
examples -> chat template -> tokens/labels -> PEFT -> SFTTrainer
-> Accelerate launch -> eval -> adapter artifact
```

Facts stay in RAG.

Behavior can move into an adapter.

<!--
This closes Day 2: M4 and M5 are custom knowledge. M6 is custom behavior.
-->
