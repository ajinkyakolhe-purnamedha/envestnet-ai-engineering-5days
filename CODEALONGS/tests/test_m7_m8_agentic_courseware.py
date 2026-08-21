"""M7 and M8 teach agents from plain Python into two frameworks."""

from pathlib import Path
from runpy import run_path


ROOT = Path(__file__).resolve().parents[1]
M7 = ROOT / "m7_agentic_applications"
M8 = ROOT / "m8_agentic_frameworks"
SLIDES = ROOT.parent / "SLIDES-markdown"
M7_DECK = SLIDES / "m7-agentic-applications.md"
M8_DECK = SLIDES / "m8-agentic-frameworks.md"

M7_SNIPPETS = [
    "01_regular_vs_agentic_llm.py",
    "02_functions_as_tools.py",
    "03_llm_tool_request.py",
    "04_python_dispatch.py",
    "05_react_loop.py",
    "06_framework_mapping.py",
]

M8_SNIPPETS = [
    "01_smolagents_tool_agent.py",
    "02_smolagents_trace_limits.py",
    "03_llamaindex_function_agent.py",
    "04_llamaindex_rag_tool.py",
    "05_agentic_workflow_patterns.py",
    "06_end_to_end_agentic_app.py",
]


def test_m7_has_five_section_intro_agent_story() -> None:
    deck = M7_DECK.read_text()

    expected_sections = [
        "M7.1 · Why Agentic LLMs Exist",
        "M7.2 · Tools Are Software Capabilities",
        "M7.3 · From Tool Request To Safe Execution",
        "M7.4 · The Agent Loop",
        "M7.5 · Handoff To Frameworks",
    ]
    for section in expected_sections:
        assert section in deck

    assert "RAG assembles from retrieved paragraphs" in deck
    assert "agentic LLM assembles from function replies" in deck
    assert "The model proposes" in deck
    assert "Python executes" in deck
    assert "max_turns" in deck
    assert "Error Observations" in deck
    assert "What To Log" in deck
    assert "Lab Success Criteria" in deck
    assert "unknown_tool" in deck


def test_m7_deck_references_ordered_runnable_snippets() -> None:
    deck = M7_DECK.read_text()

    numbered_files = sorted(path.name for path in M7.glob("[0-9][0-9]_*.py"))
    assert numbered_files == M7_SNIPPETS

    for snippet in M7_SNIPPETS:
        assert f"CODEALONGS/m7_agentic_applications/{snippet}" in deck
        assert (M7 / snippet).exists()

    readme = (M7 / "README.md").read_text()
    for snippet in M7_SNIPPETS:
        assert snippet in readme


def test_m7_shared_setup_is_small_enough_for_cookbook_context() -> None:
    source = (M7 / "workshop_agentic_setup.py").read_text()
    assert len(source.splitlines()) <= 85
    assert "TOOL_FUNCTIONS" in source
    assert "TOOL_SCHEMAS" in source
    assert "def call_smolm" in source


def test_m7_numbered_snippets_run_and_expose_key_outputs() -> None:
    for snippet in M7_SNIPPETS:
        module = run_path(M7 / snippet)
        assert module["__doc__"]

    regular = run_path(M7 / "01_regular_vs_agentic_llm.py")
    assert "paragraphs" in regular["rag_style_answer"].lower()
    assert "function replies" in regular["agentic_style_answer"].lower()

    tools = run_path(M7 / "02_functions_as_tools.py")
    assert tools["tool_result"]["symbol"] == "AAPL"

    request = run_path(M7 / "03_llm_tool_request.py")
    assert request["tool_request"]["tool"] == "get_current_price"
    assert request["raw_model_text"]
    assert request["parse_error"] is None or isinstance(request["parse_error"], str)

    dispatch = run_path(M7 / "04_python_dispatch.py")
    assert dispatch["observation"]["result"]["symbol"] == "AAPL"

    react = run_path(M7 / "05_react_loop.py")
    assert react["final_answer"]["allowed"] is False
    assert "35%" in react["final_answer"]["note"]

    mapping = run_path(M7 / "06_framework_mapping.py")
    assert "smolagents" in mapping["framework_mapping"]["max_turns"]
    assert "LlamaIndex" in mapping["framework_mapping"]["tool_registry"]


def test_m8_has_five_section_llamaindex_smolagents_story() -> None:
    deck = M8_DECK.read_text()

    expected_sections = [
        "M8.1 · From Manual Loop To Framework Runtime",
        "M8.2 · smolagents Tool Agent",
        "M8.3 · LlamaIndex Tools And RAG Capabilities",
        "M8.4 · Agentic Workflow Patterns",
        "M8.5 · End-To-End Agentic Application",
    ]
    for section in expected_sections:
        assert section in deck

    assert "ToolCallingAgent" in deck
    assert "FunctionTool" in deck
    assert "QueryEngineTool" in deck
    assert "handoff to M9" in deck
    assert "Least Autonomy That Works" in deck
    assert "Framework Tradeoff" in deck
    assert "What A Step Costs" in deck
    assert "Fixed workflow > routed workflow > agent loop" in deck
    assert "PydanticAI" not in deck
    assert "LangGraph" not in deck


def test_m8_deck_references_ordered_runnable_snippets() -> None:
    deck = M8_DECK.read_text()

    numbered_files = sorted(path.name for path in M8.glob("[0-9][0-9]_*.py"))
    assert numbered_files == M8_SNIPPETS

    for snippet in M8_SNIPPETS:
        assert f"CODEALONGS/m8_agentic_frameworks/{snippet}" in deck
        assert (M8 / snippet).exists()

    readme = (M8 / "README.md").read_text()
    for snippet in M8_SNIPPETS:
        assert snippet in readme


def test_m8_numbered_snippets_run_and_expose_key_outputs() -> None:
    for snippet in M8_SNIPPETS:
        module = run_path(M8 / snippet)
        assert module["__doc__"]

    smol = run_path(M8 / "01_smolagents_tool_agent.py")
    assert smol["agent_summary"]["framework"] == "smolagents"
    assert "check_guideline" in smol["agent_summary"]["tools"]
    assert smol["agent_summary"]["model_calls"] == 3
    assert "35%" in smol["agent_result"]

    trace = run_path(M8 / "02_smolagents_trace_limits.py")
    assert trace["blocked"]["reason"] == "max_steps"

    llama_agent = run_path(M8 / "03_llamaindex_function_agent.py")
    assert "get_current_price" in llama_agent["tool_names"]

    rag_tool = run_path(M8 / "04_llamaindex_rag_tool.py")
    assert "35%" in rag_tool["rag_result"]

    patterns = run_path(M8 / "05_agentic_workflow_patterns.py")
    assert patterns["workflow_output"]["allowed"] is False

    end_to_end = run_path(M8 / "06_end_to_end_agentic_app.py")
    assert end_to_end["answer"]["allowed"] is False
    assert "35%" in end_to_end["answer"]["note"]
