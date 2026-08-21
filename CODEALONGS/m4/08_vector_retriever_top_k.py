"""One concept: a retriever returns top-k NodeWithScore results."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=3)
results = retriever.retrieve("How much can one asset be in a portfolio?")

for result in results:
    print(f"{result.score:.3f}", result.node.metadata.get("file_name"), result.node.text[:80])
