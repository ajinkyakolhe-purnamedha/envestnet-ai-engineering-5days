"""One concept: framework step limits are the same safety idea as max_turns."""

trace = [
    {"step": 1, "model_output": "I should call a tool, but the JSON is malformed.", "observation": "parse_error"},
    {"step": 2, "model_output": "Still malformed.", "observation": "parse_error"},
    {"step": 3, "model_output": "Still no valid tool call.", "observation": "parse_error"},
]

max_steps = 3
blocked = {
    "reason": "max_steps",
    "message": "Stop the agent and return a controlled failure instead of looping forever.",
}

print("Trace:")
for item in trace:
    print(item)
print("Blocked:", blocked)
