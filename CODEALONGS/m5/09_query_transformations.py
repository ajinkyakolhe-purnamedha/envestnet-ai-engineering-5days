"""One concept: transform the query, then retrieve with LlamaIndex."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex

from workshop_m5_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=1)

user_question = "Can Alice hold 42% in AAPL, and does someone have to approve the change?"

llm_rewritten_query = Settings.llm.complete(
    "Rewrite this as a policy-search query: " + user_question
).text
rewritten_query = llm_rewritten_query + " single asset concentration limit human confirmation"
hyde_query = (
    "A policy answer would mention the maximum single-asset percentage "
    "and whether advisor approval or human confirmation is required."
)
sub_questions = [
    "What is the single-asset concentration limit?",
    "When is human confirmation required?",
]

rewrite_hit = retriever.retrieve(rewritten_query)[0].node.get_content()
hyde_hit = retriever.retrieve(hyde_query)[0].node.get_content()
sub_question_hits = [
    retriever.retrieve(sub_question)[0].node.get_content()
    for sub_question in sub_questions
]

print("user question:", user_question)
print("LLM rewrite:", llm_rewritten_query)
print("\nrewrite hit:", rewrite_hit)
print("\nHyDE hit:", hyde_hit)
print("\nsub-question hits:")
for hit in sub_question_hits:
    print("-", hit)
