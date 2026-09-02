"""One concept: the getting-started LlamaIndex RAG shape is tiny."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_llamaindex_setup import POLICY_DIR, runtime_evidence, use_local_models


llm = use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is the concentration limit?")

print(response)
print("sources:", [node.node.metadata.get("file_name") for node in response.source_nodes])
print("Runtime:", runtime_evidence(llm))
