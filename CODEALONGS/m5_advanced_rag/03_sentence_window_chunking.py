"""One concept: search sentence windows, then answer with surrounding context."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceWindowNodeParser

from workshop_m5_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
parser = SentenceWindowNodeParser.from_defaults(window_size=1)
nodes = parser.get_nodes_from_documents(documents)

index = VectorStoreIndex(nodes)
retriever = index.as_retriever(similarity_top_k=1)

question = "What happens if one asset is above 35%?"
best_node = retriever.retrieve(question)[0]

matched_sentence = best_node.node.get_content()
answer_window = best_node.node.metadata["window"]

print("question:", question)
print("matched sentence:", matched_sentence)
print("answer window:", answer_window)
