"""The whole building block: y = Wx + b."""

import torch
from torch import nn

layer = nn.Linear(in_features=4, out_features=2)

print(layer.weight.shape)   # torch.Size([2, 4])  -> W
print(layer.bias.shape)     # torch.Size([2])     -> b

x = torch.tensor([1.0, 0.0, 2.0, 0.5])

print(layer(x))                       # what a layer does
print(layer.weight @ x + layer.bias)  # ...is exactly this

# Same two numbers, twice. There is no third thing.
#
# Ten learned numbers here. 134 million in the model you
# ran in M1, arranged in a few hundred of these.
# "Training" means: find better values for those numbers.
