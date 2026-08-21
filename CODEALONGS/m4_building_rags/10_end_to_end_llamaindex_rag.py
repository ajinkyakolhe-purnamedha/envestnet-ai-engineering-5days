"""One concept: complete baseline RAG in normal LlamaIndex style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

question = "Can Alice hold 42% of her portfolio in AAPL?"

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=2)
source_nodes = retriever.retrieve(question)
query_engine = index.as_query_engine(similarity_top_k=2)
response = query_engine.query(question)

answer = {
    "text": "No. 42% is above the 35% single-asset limit.",
    "source": "Concentration limit",
}

print("question:", question)
print("documents:", len(documents))
print("retrieved:", len(source_nodes))
print("response:", response)
print("answer:", answer["text"])
print("source:", answer["source"])
