"""M4/M5 teach baseline RAG, then diagnosis-driven RAG improvement."""

from pathlib import Path
from runpy import run_path


ROOT = Path(__file__).resolve().parents[1]
M4 = ROOT / "m4_building_rags"
M5 = ROOT / "m5_advanced_rag"
SLIDES = ROOT.parent / "SLIDES-markdown"
M4_DECK = SLIDES / "m4-building-rags.md"
M5_DECK = SLIDES / "m5-advanced-rag.md"


def test_m4_has_six_section_baseline_rag_story() -> None:
    deck = M4_DECK.read_text()

    expected_sections = [
        "M4.1 · Why RAG Exists",
        "M4.2 · Simple RAG In LlamaIndex",
        "M4.3 · The Complete RAG Pipeline",
        "M4.4 · Chunking",
        "M4.5 · Indexing And Vector Databases",
        "M4.6 · Retrieval And Grounded Answering",
        "M4.7 · End-To-End Baseline RAG",
    ]
    for section in expected_sections:
        assert section in deck

    for snippet in [
        "01_why_rag_exists.py",
        "02_simple_rag_llamaindex.py",
        "03_complete_pipeline_objects.py",
        "04_sentence_splitter_nodes.py",
        "05_nodes_with_metadata.py",
        "06_vector_store_index.py",
        "07_storage_context.py",
        "08_vector_retriever_top_k.py",
        "09_query_engine_sources.py",
        "10_end_to_end_llamaindex_rag.py",
    ]:
        assert f"CODEALONGS/m4_building_rags/{snippet}" in deck
        assert (M4 / snippet).exists()
        text = (M4 / snippet).read_text()
        assert "workshop_llamaindex_setup" in text
        assert "llama_index.core" in text

    assert "HyDE" not in deck
    assert "parent-child" not in deck.lower()


def test_m5_has_evaluation_then_advanced_rag_improvements() -> None:
    deck = M5_DECK.read_text()

    expected_sections = [
        "M5.1 · Evaluate The Baseline",
        "M5.2 · Improve Chunks",
        "M5.3 · Improve Search",
        "M5.4 · Improve Ranking",
        "M5.5 · Improve The Query",
    ]
    for section in expected_sections:
        assert section in deck

    for snippet in [
        "01_evaluate_baseline.py",
        "03_sentence_window_chunking.py",
        "05_hybrid_search.py",
        "07_rerank_results.py",
        "09_query_transformations.py",
    ]:
        assert f"CODEALONGS/m5_advanced_rag/{snippet}" in deck
        assert (M5 / snippet).exists()
        text = (M5 / snippet).read_text()
        assert "llama_index.core" in text

    assert "ragas" in (M5 / "01_evaluate_baseline.py").read_text()

    assert "RAGAS" in deck
    assert "HyDE" in deck
    assert "sub-question decomposition" in deck


def test_m4_numbered_snippets_run_and_expose_pipeline_objects() -> None:
    for snippet in [
        "01_why_rag_exists.py",
        "02_simple_rag_llamaindex.py",
        "03_complete_pipeline_objects.py",
        "04_sentence_splitter_nodes.py",
        "05_nodes_with_metadata.py",
        "06_vector_store_index.py",
        "07_storage_context.py",
        "08_vector_retriever_top_k.py",
        "09_query_engine_sources.py",
        "10_end_to_end_llamaindex_rag.py",
    ]:
        module = run_path(M4 / snippet)
        assert module["__doc__"]

    end_to_end = run_path(M4 / "10_end_to_end_llamaindex_rag.py")
    assert end_to_end["answer"]["source"] == "Concentration limit"
    assert "35%" in end_to_end["answer"]["text"]

    setup = run_path(M4 / "workshop_llamaindex_setup.py")
    assert setup["POLICY_DIR"].exists()
    setup_source = (M4 / "workshop_llamaindex_setup.py").read_text()
    assert "AutoModelForCausalLM" in setup_source
    assert "apply_chat_template" in setup_source
    assert "model.generate" in setup_source
    assert "bge-small-en-v1.5-onnx" in setup_source
    assert "onnxruntime" in setup_source
    assert "local-policy-llm" not in setup_source
    assert "LocalPolicyEmbedding" not in setup_source


def test_m5_numbered_snippets_run_and_show_specific_improvements() -> None:
    for snippet in [
        "01_evaluate_baseline.py",
        "03_sentence_window_chunking.py",
        "05_hybrid_search.py",
        "07_rerank_results.py",
        "09_query_transformations.py",
    ]:
        module = run_path(M5 / snippet)
        assert module["__doc__"]

    hybrid = run_path(M5 / "05_hybrid_search.py")
    assert hybrid["hybrid_top_title"] == "Concentration limit"

    rerank = run_path(M5 / "07_rerank_results.py")
    assert rerank["reranked"][0]["title"] == "Concentration limit"

    query_transform = run_path(M5 / "09_query_transformations.py")
    assert query_transform["llm_rewritten_query"]
