# Checkpoint Lab Hints

## TODO 1 · Chat messages

Start from the `messages` list in `../01_direct_investor_chat.py`. Keep the
system instruction and trusted facts as separate messages. Add a small history
list and slice it with `[-4:]` before the new user question.

## TODOs 2a–2b · Policy evidence

Follow the order in `../02_policy_evidence_rag.py`:

1. In `load_policy_documents`, call `use_local_models()` and load `POLICY_DIR`.
2. In `build_policy_engine`, call `VectorStoreIndex.from_documents(...)`.
3. Return `index.as_query_engine(similarity_top_k=1)`.

Test the engine directly with `engine.query("concentration limit")` before
adding it to the agent.

## TODOs 3a–3b · Bounded agent

In 3a, use `QueryEngineTool` plus `ToolMetadata` to turn the engine into a tool
named `policy_rag`. In 3b, follow the `ToolCallingAgent(...)` construction in
`../03_advisor_agent_with_rag_tool.py`: write a small `@tool` wrapper which
calls your query tool, then pass the two tools, `ClassroomModel()`, and
`max_steps=3`.

The planner is mocked only for tool-call shape; it does not replace your local
chat or your retrieval step. If the agent fails, confirm that both tool
functions have clear docstrings and `Args:` descriptions.
