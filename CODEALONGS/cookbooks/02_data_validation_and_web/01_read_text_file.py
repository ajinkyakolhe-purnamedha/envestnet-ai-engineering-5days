# Read a text file
from pathlib import Path

policy = Path("data/mini_policy.md").read_text()
print(policy[:80])

