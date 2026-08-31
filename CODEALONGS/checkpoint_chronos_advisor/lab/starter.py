"""Checkpoint lab starter: connect local chat, evidence, and one bounded agent."""

import sys
from pathlib import Path

CHECKPOINT = Path(__file__).resolve().parents[1]
CODEALONGS = CHECKPOINT.parent
sys.path.insert(0, str(CHECKPOINT))
sys.path.insert(0, str(CODEALONGS / "m4_building_rags"))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from smolagents import ToolCallingAgent, tool
from classroom_model import ClassroomModel
from offline_model import generate
from workshop_llamaindex_setup import POLICY_DIR, use_local_models

ALICE = {"client": "Alice", "cash": 25_000, "holdings": ["SPY", "QQQ", "GLD"]}
QUESTION = "What does the policy say about Alice's concentration risk?"
HISTORY = [{"role": "user", "content": "What do I own?"}]


def build_messages(question: str) -> list[dict[str, str]]:
    # TODO 1: Return system instruction, trusted ALICE facts, HISTORY[-4:], and
    # the new question. See ../01_direct_investor_chat.py.
    raise NotImplementedError("Build the local chat messages.")


def load_policy_documents():
    # TODO 2a: Call use_local_models(), then load the documents in POLICY_DIR.
    raise NotImplementedError("Load the local policy documents.")


def build_policy_engine(documents):
    # TODO 2b: Build VectorStoreIndex from documents and return its query engine.
    raise NotImplementedError("Build the policy RAG query engine.")


@tool
def portfolio_summary(client_id: str) -> dict:
    """Return Alice's read-only Chronos portfolio.

    Args:
        client_id: The allowed demo client, alice.
    """
    return ALICE if client_id.lower() == "alice" else {"error": "access denied"}


def build_policy_tool(engine):
    # TODO 3a: Use QueryEngineTool and ToolMetadata to make `policy_rag`.
    # Give it a short description that tells an agent what it can search.
    raise NotImplementedError("Turn the query engine into a policy tool.")


def run_checkpoint(engine, question: str) -> str:
    # TODO 3b: Wrap your policy tool in an @tool function, then create a
    # ToolCallingAgent with portfolio_summary, policy_rag, ClassroomModel(), and
    # max_steps=3. Run it with `question`. See ../03_advisor_agent_with_rag_tool.py.
    raise NotImplementedError("Compose the bounded framework agent.")


if __name__ == "__main__":
    chat_reply = generate(build_messages(QUESTION), max_new_tokens=80)
    print("Checkpoint 1 — local chat:", chat_reply)
    documents = load_policy_documents()
    engine = build_policy_engine(documents)
    print("Checkpoint 2 — evidence:", engine.query("concentration limit"))
    print("Checkpoint 3 — agent result:", run_checkpoint(engine, QUESTION))
