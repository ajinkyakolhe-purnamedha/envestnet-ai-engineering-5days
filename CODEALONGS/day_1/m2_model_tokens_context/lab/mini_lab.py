"""Mini lab: measure one supplied synthetic model response."""

from pathlib import Path
from runpy import run_path

estimate_cost = run_path(Path(__file__).parents[1] / "11_instrument_reply.py")["estimate_cost"]

usage = {"input_tokens": 240, "output_tokens": 60}
cost = estimate_cost(**usage, input_rate=0.002, output_rate=0.004)
print(f"input={usage['input_tokens']} output={usage['output_tokens']} cost=${cost:.6f}")
