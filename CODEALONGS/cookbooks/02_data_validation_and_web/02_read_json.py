# Read JSON
import json
from pathlib import Path

portfolio = json.loads(Path("data/sample_portfolio.json").read_text())
print(portfolio["risk_profile"])

