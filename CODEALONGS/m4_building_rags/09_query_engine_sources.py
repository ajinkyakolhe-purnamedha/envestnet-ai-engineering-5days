"""One concept: QueryEngine responses carry source_nodes for citations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=2)
response = query_engine.query("Can Alice hold 42% of her portfolio in AAPL?")

print("response:", response)
print("\nsources:")
for source in response.source_nodes:
    print("-", source.node.metadata.get("file_name"), source.node.text[:90])
