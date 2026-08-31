"""The checkpoint must be a real local-LLM/RAG/framework code-along."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "checkpoint_chronos_advisor"


def test_checkpoint_has_three_ordered_runnable_code_cards() -> None:
    expected = ["01_direct_investor_chat.py", "02_policy_evidence_rag.py", "03_advisor_agent_with_rag_tool.py"]
    assert sorted(path.name for path in LAB.glob("[0-9][0-9]_*.py")) == expected
    for name in expected:
        assert "One concept:" in (LAB / name).read_text()


def test_checkpoint_uses_local_llm_rag_and_framework_tools() -> None:
    chat = (LAB / "01_direct_investor_chat.py").read_text()
    rag = (LAB / "02_policy_evidence_rag.py").read_text()
    agent = (LAB / "03_advisor_agent_with_rag_tool.py").read_text()
    assert "chronos_offline import generate" in chat
    assert "VectorStoreIndex" in rag and "source_nodes" in rag
    assert "ToolCallingAgent" in agent and "QueryEngineTool" in agent
    assert "ClassroomModel" in agent and "max_steps=3" in agent


def test_checkpoint_lab_keeps_the_student_path_small() -> None:
    readme = (LAB / "README.md").read_text()
    starter = (LAB / "lab" / "starter.py").read_text()
    assert "90 minutes" in readme
    assert "MCP comes later" in readme
    assert "NotImplementedError" in starter
    assert len(starter.splitlines()) <= 90
