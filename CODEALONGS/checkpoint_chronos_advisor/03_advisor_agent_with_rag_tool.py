"""One concept: a bounded framework agent calls portfolio and RAG tools."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m8_agentic_frameworks"))
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from smolagents import Model, ToolCallingAgent, tool
from smolagents.models import ChatMessage, ChatMessageToolCall, ChatMessageToolCallFunction, MessageRole
from rag_setup import POLICY_DIR, use_local_models

class ClassroomModel(Model):
    """Mocked tool-call response: replace with a stronger local model later."""
    def __init__(self):
        super().__init__()
        self.calls = 0
    def generate(self, messages, tools_to_call_from=None, **kwargs):
        self.calls += 1
        if self.calls == 1:
            name, arguments = "portfolio_summary", {"client_id": "alice"}
        elif self.calls == 2:
            name, arguments = "policy_rag", {"query": "concentration limit"}
        else:
            name, arguments = "final_answer", {"answer": "Alice's policy evidence is shown above."}
        call = ChatMessageToolCall(id=str(self.calls), type="function", function=ChatMessageToolCallFunction(name=name, arguments=arguments))
        return ChatMessage(role=MessageRole.ASSISTANT, tool_calls=[call])

@tool
def portfolio_summary(client_id: str) -> dict:
    """Return Alice's read-only Chronos portfolio.

    Args:
        client_id: The allowed demo client, alice.
    """
    return {"client": "alice", "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]} if client_id == "alice" else {"error": "access denied"}

use_local_models()
index = VectorStoreIndex.from_documents(SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data())
policy_rag_tool = QueryEngineTool(index.as_query_engine(), ToolMetadata(name="policy_rag", description="Search the investment policy."))
@tool
def policy_rag(query: str) -> str:
    """Search policy evidence.

    Args:
        query: The policy question to retrieve.
    """
    return str(policy_rag_tool.call(query))

agent = ToolCallingAgent(tools=[portfolio_summary, policy_rag], model=ClassroomModel(), max_steps=3)
question = "What does policy say about Alice's concentration risk?"
print("Framework agent:", agent.run(question, max_steps=3))
print("RAG tool evidence:", policy_rag_tool.call("concentration limit"))
print("Limit: max_steps=3; portfolio tool only accepts Alice.")
