"""One concept: fuse LlamaIndex vector results with exact keyword matches."""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from workshop_m5_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
nodes = SentenceSplitter(chunk_size=90, chunk_overlap=0).get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)

query = "35%"
dense_results = index.as_retriever(similarity_top_k=3).retrieve(query)


def terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def sparse_score(text: str) -> int:
    query_terms = Counter(terms(query))
    text_terms = Counter(terms(text))
    return sum(query_terms[token] * text_terms[token] for token in query_terms)


fused = []
for rank, result in enumerate(dense_results):
    dense_score = 1.0 / (rank + 1)
    keyword_score = sparse_score(result.node.get_content())
    fused.append((dense_score + keyword_score, result))

hybrid = sorted(fused, key=lambda row: row[0], reverse=True)
hybrid_top_text = hybrid[0][1].node.get_content()
hybrid_top_title = "Concentration limit" if "35%" in hybrid_top_text else "Other policy"

print("query:", query)
print("dense top:", dense_results[0].node.get_content())
print("hybrid top:", hybrid_top_text)
