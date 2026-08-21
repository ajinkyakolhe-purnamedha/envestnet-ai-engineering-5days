"""One concept: framework terms map back to the same loop parts."""

framework_mapping = {
    "tool_registry": {
        "plain_python": "TOOL_FUNCTIONS and TOOL_SCHEMAS",
        "smolagents": "@tool functions passed into ToolCallingAgent",
        "LlamaIndex": "FunctionTool and QueryEngineTool",
    },
    "model_planner": {
        "plain_python": "planner(state)",
        "smolagents": "model inside ToolCallingAgent",
        "LlamaIndex": "llm inside FunctionAgent",
    },
    "max_turns": {
        "plain_python": "for turn in range(max_turns)",
        "smolagents": "max_steps",
        "LlamaIndex": "workflow or agent step limits",
    },
    "observation_trace": {
        "plain_python": "trace list",
        "smolagents": "agent step logs",
        "LlamaIndex": "tool outputs and callback events",
    },
}

for concept, mapping in framework_mapping.items():
    print(concept, "->", mapping)
