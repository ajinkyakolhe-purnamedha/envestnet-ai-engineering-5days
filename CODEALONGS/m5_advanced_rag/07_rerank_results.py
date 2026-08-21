"""One concept: retrieve wide with LlamaIndex, then rerank candidates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from workshop_m5_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
nodes = SentenceSplitter(chunk_size=90, chunk_overlap=0).get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)

question = "Can one asset be 42% of the portfolio?"
candidates = index.as_retriever(similarity_top_k=4).retrieve(question)


def reranker_score(candidate_text: str) -> float:
    score = 0.0
    if "asset" in candidate_text:
        score += 1.0
    if "35%" in candidate_text:
        score += 2.0
    if "portfolio" in candidate_text:
        score += 1.0
    return score


reranked_nodes = sorted(
    candidates,
    key=lambda result: reranker_score(result.node.get_content().lower()),
    reverse=True,
)
reranked = [
    {
        "title": "Concentration limit" if "35%" in result.node.get_content() else "Other policy",
        "text": result.node.get_content(),
        "retrieval_score": result.score,
        "reranker_score": reranker_score(result.node.get_content().lower()),
    }
    for result in reranked_nodes
]

print("retrieval order:")
for result in candidates:
    print(round(result.score or 0.0, 2), result.node.get_content())

print("\nreranked order:")
for row in reranked:
    print(row["reranker_score"], row["text"])
