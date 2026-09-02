"""One concept: a small app combines tools, policy search, workflow, and answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4_building_rags"))

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex

from workshop_framework_setup import QUESTION, check_guideline, get_current_price, get_portfolio_allocation
from workshop_llamaindex_setup import POLICY_DIR, use_local_models
from local_hf_agent import LocalSmolFunctionLLM


use_local_models()
llm = LocalSmolFunctionLLM()
Settings.llm = llm

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
policy_answer = str(index.as_query_engine(similarity_top_k=2).query("single asset concentration limit"))

price = get_current_price("AAPL")
allocation = get_portfolio_allocation("Alice", "AAPL")
guideline = check_guideline("AAPL", 36.0)
model_draft = llm.complete(
    "Write a short internal advisor note using only these facts. "
    f"Question: {QUESTION}\nPrice: {price}\nAllocation: {allocation}\n"
    f"Policy: {policy_answer}\nGuideline: {guideline}"
).text
answer = {
    "question": QUESTION,
    "allowed": guideline["allowed"],
    "evidence": [price, allocation, guideline],
    "policy_context": policy_answer,
    "model_draft": model_draft,
}
runtime = {
    "backend": "local Hugging Face inference",
    "model": llm.metadata.model_name,
    "model_calls": llm.generation_count,
    "latency_ms": llm.last_generation_latency_ms,
}

print("Runtime:", runtime)
print("Raw model text:", llm.last_response)
print("Question:", QUESTION)
print("Answer:", answer)
