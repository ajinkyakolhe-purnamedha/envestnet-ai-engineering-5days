"""Any LLM is a PyTorch nn.Module. Nothing more exotic."""

import torch
from transformers import AutoModelForCausalLM

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"
model = AutoModelForCausalLM.from_pretrained(
    PATH, local_files_only=True
)

print(isinstance(model, torch.nn.Module))   # True

print(model.model.layers[0])
# LlamaDecoderLayer(
#   self_attn: LlamaAttention(q_proj, k_proj, v_proj, o_proj)
#   mlp:       LlamaMLP(gate_proj, up_proj, down_proj, SiLU)
#   input_layernorm / post_attention_layernorm
# )

n = sum(p.numel() for p in model.parameters())
print(f"{n:,} parameters")       # 134,515,008

# Thirty of those layers stacked, and that is SmolLM2 --
# the same model you have been calling since M1.
#
# A frontier model is the same block, wider and deeper,
# with a few hundred billion more numbers in it. There
# is no additional mechanism hiding in the large ones.
