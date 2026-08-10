# Parse JSON output
import json

output = json.loads('{"decision": "REVIEW"}')
print(output["decision"])

