"""One concept: LlamaIndex names the pipeline objects you inspect."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
splitter = SentenceSplitter(chunk_size=80, chunk_overlap=10)
nodes = splitter.get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)
retriever = index.as_retriever(similarity_top_k=2)
query_engine = index.as_query_engine(similarity_top_k=2)

print("documents:", len(documents))
print("nodes:", len(nodes))
print("index:", type(index).__name__)
print("retriever:", type(retriever).__name__)
print("query_engine:", type(query_engine).__name__)
