"""One concept: LlamaIndex retrieves Chronos policy evidence before answering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4_building_rags"))
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from workshop_llamaindex_setup import POLICY_DIR, use_local_models

use_local_models()
question = "What is the single asset concentration limit?"
documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
engine = index.as_query_engine(similarity_top_k=1)
response = engine.query(question)

print("Question:", question)
print("Local RAG answer:", response)
print("Evidence:", response.source_nodes[0].node.text)
