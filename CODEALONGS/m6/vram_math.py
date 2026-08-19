"""Why you cannot full fine-tune 8B on your laptop."""

PARAMS = 8_000_000_000

weights = PARAMS * 2       # bf16, 2 bytes per number
gradients = PARAMS * 2     # one gradient per weight
optimizer = PARAMS * 8     # Adam keeps 2 fp32 copies

total = weights + gradients + optimizer
print(f"{total / 1e9:.0f} GB before a single activation")
# 96 GB

# Add activations for the backward pass and you are at
# roughly 16x the parameter count.
#
# An H100 has 80 GB. Your laptop has 16.
#
# LoRA deletes lines 2 and 3, not line 1: freeze the
# weights and there are no gradients and no optimizer
# state for 99.8% of them.
