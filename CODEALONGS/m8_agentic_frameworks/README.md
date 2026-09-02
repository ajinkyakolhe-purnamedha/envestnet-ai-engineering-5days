# M8 Code-Alongs: Agentic Frameworks

M8 runs the committed **SmolLM2 135M Instruct** model locally. Every numbered
card performs live local inference. The model is deliberately small: malformed
tool calls, hallucinated facts, or a framework stop are evidence to inspect,
not output to replace with a fixture.

From the repository root, create the courseware environment once:

```bash
uv sync --project CODEALONGS --extra courseware
```

Then run cards from the repository root:

```bash
uv run --project CODEALONGS python CODEALONGS/m8_agentic_frameworks/01_smolagents_tool_agent.py
```

Every card prints `Runtime:` with the local model name, number of model calls,
and latest-call latency, followed by raw model text. On a CPU laptop, expect a
few seconds for each model call after the initial weight load.

Snippets:

- `01_smolagents_tool_agent.py` - smolagents attempts a tool-calling loop with the live 135M model
- `01b_llamaindex_tool_agent.py` - LlamaIndex alternative: `FunctionAgent` with the live 135M model
- `02_smolagents_trace_limits.py` - framework trace and `max_steps` around live model output
- `02b_llamaindex_trace_limits.py` - LlamaIndex alternative: live model output constrained by `max_iterations`
- `03_llamaindex_function_agent.py` - LlamaIndex `FunctionTool` and `FunctionAgent`
- `04_llamaindex_rag_tool.py` - policy RAG as `QueryEngineTool`
- `05_agentic_workflow_patterns.py` - deterministic routing and facts, with a live local-model draft
- `06_end_to_end_agentic_app.py` - end-to-end app with policy search and a live local-model draft

Python remains responsible for prices, allocations, policy checks, and tool
allowlists. The model only proposes or drafts from the facts it receives.
