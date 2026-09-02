"""One concept: RAG gives the model a source document to answer from."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_llamaindex_setup import POLICY_DIR, runtime_evidence, use_local_models


llm = use_local_models()

question = "What is the single asset concentration limit?"
bare_model_answer = "A bare model has not read the Chronos policy."

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=1)
response = query_engine.query(question)

print("question:", question)
print("bare model:", bare_model_answer)
print("rag response:", response)
print("source nodes:", len(response.source_nodes))
print("Runtime:", runtime_evidence(llm))
