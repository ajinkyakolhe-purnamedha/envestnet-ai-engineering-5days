"""M7 and M8 teach agents from plain Python into two frameworks."""

from pathlib import Path
from runpy import run_path
import sys


ROOT = Path(__file__).resolve().parents[1]
M7 = ROOT / "m7_agentic_applications"
M8 = ROOT / "m8_agentic_frameworks"
SLIDES = ROOT.parent / "SLIDES-markdown"
M7_DECK = SLIDES / "m7-agentic-applications.md"
M8_DECK = SLIDES / "m8-agentic-frameworks.md"
sys.path.insert(0, str(M8))

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


def test_m7_tool_request_card_never_replaces_live_model_output() -> None:
    source = (M7 / "03_llm_tool_request.py").read_text()

    assert "fallback_text" not in source
    assert "classroom fallback" not in source
    assert "tool_request = None" in source


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
    assert request["raw_model_text"]
    assert request["parse_error"] is None or isinstance(request["parse_error"], str)
    if request["parse_error"] is None:
        assert request["tool_request"]["tool"] == "get_current_price"
    else:
        assert request["tool_request"] is None

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


def test_m8_uses_the_committed_135m_model_without_a_download_step() -> None:
    import local_hf_agent

    assert local_hf_agent.MODEL_DIR == ROOT.parent / "OFFLINE-AI-Models" / "smollm2-135m-instruct"
    assert local_hf_agent.LocalSmolFunctionLLM().metadata.model_name == "HuggingFaceTB/SmolLM2-135M-Instruct"
    assert not (M8 / "download_local_models.py").exists()


def test_m8_agent_cards_make_live_local_model_calls() -> None:
    for snippet in (
        "01_smolagents_tool_agent.py",
        "01b_llamaindex_tool_agent.py",
        "02_smolagents_trace_limits.py",
        "02b_llamaindex_trace_limits.py",
        "03_llamaindex_function_agent.py",
        "04_llamaindex_rag_tool.py",
        "05_agentic_workflow_patterns.py",
        "06_end_to_end_agentic_app.py",
    ):
        source = (M8 / snippet).read_text()
        assert "LocalSmolFunctionLLM" in source or "LiveSmolAgentsModel" in source
        assert "Runtime:" in source

    assert "ClassroomModel" not in (M8 / "01_smolagents_tool_agent.py").read_text()


def test_m4_and_m8_share_the_offline_hugging_face_runtime() -> None:
    shared_runtime = ROOT / "shared" / "offline_hf.py"

    assert shared_runtime.exists()
    assert "LocalHuggingFaceLLM" in shared_runtime.read_text()
    assert "from offline_hf import" in (ROOT / "m4_building_rags" / "workshop_llamaindex_setup.py").read_text()
    assert "from offline_hf import" in (M8 / "local_hf_agent.py").read_text()


def test_local_smol_adapter_parses_documented_tool_call_format() -> None:
    from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
    from local_hf_agent import LocalSmolFunctionLLM

    response = ChatResponse(
        message=ChatMessage(
            role=MessageRole.ASSISTANT,
            content=(
                '<tool_call>[{"name": "get_current_price", '
                '"arguments": {"symbol": "AAPL"}}]</tool_call>'
            ),
        )
    )

    calls = LocalSmolFunctionLLM().get_tool_calls_from_response(response)

    assert calls[0].tool_name == "get_current_price"
    assert calls[0].tool_kwargs == {"symbol": "AAPL"}


def test_local_smol_adapter_passes_batch_encoding_to_generate(monkeypatch) -> None:
    import torch
    import local_hf_agent
    import offline_hf

    class BatchEncoding(dict):
        def to(self, device):
            return self

    class Tokenizer:
        eos_token_id = 0

        def apply_chat_template(self, *args, **kwargs):
            return BatchEncoding(input_ids=torch.tensor([[1, 2]]), attention_mask=torch.tensor([[1, 1]]))

        def decode(self, tokens, skip_special_tokens=True):
            return "generated"

    class Model:
        device = "cpu"

        def generate(self, **inputs):
            assert set(inputs) == {"input_ids", "attention_mask", "max_new_tokens", "do_sample", "pad_token_id"}
            return torch.tensor([[1, 2, 3]])

    monkeypatch.setattr(offline_hf, "load_text_model", lambda model_dir: (Tokenizer(), Model()))

    assert local_hf_agent.LocalSmolFunctionLLM()._generate([{"role": "user", "content": "hi"}]) == "generated"


def test_local_smol_adapter_unwraps_schema_shaped_arguments() -> None:
    from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
    from local_hf_agent import LocalSmolFunctionLLM

    response = ChatResponse(
        message=ChatMessage(
            role=MessageRole.ASSISTANT,
            content=(
                '<tool_call>[{"name": "get_current_price", "arguments": '
                '{"properties": {"symbol": "AAPL"}}}]</tool_call>'
            ),
        )
    )

    calls = LocalSmolFunctionLLM().get_tool_calls_from_response(response)

    assert calls[0].tool_kwargs == {"symbol": "AAPL"}


def test_local_smol_adapter_uses_one_tool_system_prompt(monkeypatch) -> None:
    import local_hf_agent
    from llama_index.core.base.llms.types import ChatMessage, MessageRole
    from llama_index.core.tools import FunctionTool

    captured = []
    monkeypatch.setattr(local_hf_agent.LocalSmolFunctionLLM, "_generate", lambda self, messages: captured.extend(messages) or "<tool_call>[]</tool_call>")
    tool = FunctionTool.from_defaults(fn=lambda symbol: symbol, name="lookup")
    llm = local_hf_agent.LocalSmolFunctionLLM()

    llm.chat_with_tools(
        [tool],
        chat_history=[
            ChatMessage(role=MessageRole.SYSTEM, content="generic agent prompt"),
            ChatMessage(role=MessageRole.USER, content="Look up AAPL"),
        ],
    )

    assert [message["role"] for message in captured].count("system") == 1


def test_local_smol_adapter_switches_to_a_final_answer_after_tool_result(monkeypatch) -> None:
    import local_hf_agent
    from llama_index.core.base.llms.types import ChatMessage, MessageRole
    from llama_index.core.tools import FunctionTool

    captured = []
    monkeypatch.setattr(local_hf_agent.LocalSmolFunctionLLM, "_generate", lambda self, messages: captured.extend(messages) or "The price is 108.0.")
    tool = FunctionTool.from_defaults(fn=lambda symbol: symbol, name="lookup")

    local_hf_agent.LocalSmolFunctionLLM().chat_with_tools(
        [tool],
        chat_history=[
            ChatMessage(role=MessageRole.USER, content="Look up AAPL"),
            ChatMessage(role=MessageRole.TOOL, content="{'symbol': 'AAPL', 'price': 108.0}"),
        ],
    )

    assert "final answer" in captured[0]["content"].lower()
    assert "<tool_call>" not in captured[0]["content"]


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
    modules = {}
    for snippet in M8_SNIPPETS:
        modules[snippet] = run_path(M8 / snippet)
        assert modules[snippet]["__doc__"]
        runtime = modules[snippet]["runtime"]
        assert runtime["backend"] == "local Hugging Face inference"
        assert runtime["model"] == "HuggingFaceTB/SmolLM2-135M-Instruct"
        assert runtime["model_calls"] >= 1

    smol = modules["01_smolagents_tool_agent.py"]
    assert smol["agent_summary"]["framework"] == "smolagents"
    assert "check_guideline" in smol["agent_summary"]["tools"]
    assert smol["agent_summary"]["model_calls"] >= 1
    assert smol["model"].last_response

    trace = modules["02_smolagents_trace_limits.py"]
    assert trace["blocked"]["reason"] in {"framework_stop", "completed"}
    assert trace["trace"][0]["model_output"]

    llama_agent = modules["03_llamaindex_function_agent.py"]
    assert "get_current_price" in llama_agent["tool_names"]
    assert llama_agent["model_call_count"] >= 1
    assert llama_agent["llm"].last_response

    rag_tool = modules["04_llamaindex_rag_tool.py"]
    assert rag_tool["policy_tool"].metadata.name == "search_policy"

    patterns = modules["05_agentic_workflow_patterns.py"]
    assert patterns["workflow_output"]["allowed"] is False
    assert patterns["workflow_output"]["note"] == patterns["llm"].last_response

    end_to_end = modules["06_end_to_end_agentic_app.py"]
    assert end_to_end["answer"]["allowed"] is False
    assert end_to_end["answer"]["model_draft"] == end_to_end["llm"].last_response
