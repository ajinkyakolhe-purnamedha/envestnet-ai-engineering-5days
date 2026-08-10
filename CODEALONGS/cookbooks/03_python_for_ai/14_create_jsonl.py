# Create JSONL
import json

examples = [{"text": "Buy SPY", "label": "trade"}, {"text": "Show cash", "label": "lookup"}]
jsonl_lines = [json.dumps(example) for example in examples]
print("\n".join(jsonl_lines))

