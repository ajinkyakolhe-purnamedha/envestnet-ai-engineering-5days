"""One concept: a RAG query engine can become an agent tool."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4_building_rags"))

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool

from workshop_llamaindex_setup import POLICY_DIR, use_local_models
from local_hf_agent import LocalSmolFunctionLLM


use_local_models()
llm = LocalSmolFunctionLLM()
Settings.llm = llm

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
policy_query_engine = index.as_query_engine(similarity_top_k=2)
policy_tool = QueryEngineTool.from_defaults(
    query_engine=policy_query_engine,
    name="search_policy",
    description="Search the advisor policy manual before making a recommendation.",
)

question = "What is the single asset concentration limit?"
rag_result = str(policy_tool.call(question))
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "latency_ms": llm.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("Tool:", policy_tool.metadata.name)
print("RAG result:", rag_result)
