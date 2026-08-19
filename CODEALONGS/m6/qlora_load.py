"""Load the frozen part in 4 bits. Train adapters in 16."""

import torch
from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM

# #region quant
quant = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",     # NormalFloat4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

def load_4bit(name: str = "meta-llama/Llama-3.1-8B"):
    model = AutoModelForCausalLM.from_pretrained(
        name, quantization_config=quant, device_map="auto"
    )
    print(model.get_memory_footprint() / 1e9)   # ~5.6 GB
    return model
# #endregion quant


if __name__ == "__main__":
    try:
        load_4bit()
    except ImportError:
        print("bitsandbytes needs a CUDA GPU -- shape only.")

# bf16 would have been ~16 GB, before gradients,
# optimizer state and activations.
#
# The frozen weights are only ever READ, so 4 bits is
# enough precision. The adapters you actually train stay
# in bf16, because those are the ones learning.
#
# NOTE: bitsandbytes needs a CUDA GPU. This snippet is
# the shape you will use on a training box -- it will not
# run on a Mac, and nothing else in this folder needs it.
