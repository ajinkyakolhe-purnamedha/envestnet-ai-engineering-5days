"""Training, entire. Predict, measure error, nudge, repeat."""

import torch
from torch import nn

torch.manual_seed(0)

# A rule we already know: position value = shares x 100
shares = torch.rand(200, 1) * 10
value = shares * 100

model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
optim = torch.optim.SGD(model.parameters(), lr=0.01)

for step in range(1001):
    predicted = model(shares)          # forward pass
    loss = loss_fn(predicted, value)   # how wrong was it?

    optim.zero_grad()
    loss.backward()                    # which way is down?
    optim.step()                       # one small step

    if step % 250 == 0:
        print(step, round(loss.item(), 3))

print(model.weight.item())    # -> 99.98...

# Nobody told it the rule. It reduced error until it had
# one. A frontier model is this loop, with more numbers
# and a harder rule to find.
