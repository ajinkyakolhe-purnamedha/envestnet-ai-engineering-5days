"""Two linear layers with nothing between them = one layer."""

import torch
from torch import nn

flat = nn.Sequential(
    nn.Linear(4, 8),
    nn.Linear(8, 2),
)

bent = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),          # <- the entire difference
    nn.Linear(8, 2),
)

x = torch.randn(4)
print(flat(x), bent(x))

# `flat` gained nothing from being deep. Composing two
# matrix multiplies collapses back into one:
#
#     W2 @ (W1 @ x)  ==  (W2 @ W1) @ x
#
# `bent` cannot be collapsed. ReLU zeroes the negatives,
# and that kink is what lets a stack learn a curve.
#
# Depth + non-linearity = enough capacity to separate
# "thinking about selling" from "sell 40 shares".
