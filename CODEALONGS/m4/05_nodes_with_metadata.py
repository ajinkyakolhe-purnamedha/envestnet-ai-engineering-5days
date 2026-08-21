"""One concept: metadata travels from Document to Node to citation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from workshop_llamaindex_setup import use_local_models


use_local_models()

document = Document(
    text="No single asset may exceed 35% of the portfolio.",
    metadata={"title": "Concentration limit", "file_name": "mini_policy.md"},
)
nodes = SentenceSplitter(chunk_size=80, chunk_overlap=10).get_nodes_from_documents([document])

print("node text:", nodes[0].text)
print("node metadata:", nodes[0].metadata)
