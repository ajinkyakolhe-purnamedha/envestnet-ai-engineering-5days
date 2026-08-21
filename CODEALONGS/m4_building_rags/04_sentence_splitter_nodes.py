"""One concept: SentenceSplitter turns Documents into Nodes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
splitter = SentenceSplitter(chunk_size=80, chunk_overlap=10)
nodes = splitter.get_nodes_from_documents(documents)

for node in nodes:
    print("node:", node.text.replace("\n", " ")[:90])
    print("metadata:", node.metadata)
