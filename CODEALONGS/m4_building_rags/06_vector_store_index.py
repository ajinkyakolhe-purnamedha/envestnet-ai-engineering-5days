"""One concept: VectorStoreIndex embeds Nodes into a searchable index."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
nodes = SentenceSplitter(chunk_size=80, chunk_overlap=10).get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)

print("nodes indexed:", len(nodes))
print("index:", type(index).__name__)
