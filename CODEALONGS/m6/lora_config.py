"""Freeze the model. Train two small matrices per layer."""

from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"
base = AutoModelForCausalLM.from_pretrained(
    PATH, local_files_only=True
)

# #region config
config = LoraConfig(
    r=16,                    # rank: adapter capacity
    lora_alpha=32,           # how loud the adapter is
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)

model = get_peft_model(base, config)
model.print_trainable_parameters()

# trainable params: 921,600 || all params: 135,436,608
# || trainable%: 0.6805
# #endregion config

#   W = W0 + (alpha / r) * (B @ A)
#
# W0 never moves. A is r x k, B is d x r, and together
# they are a couple of MB you ship on top of the base
# model -- one adapter per client, if you want.
