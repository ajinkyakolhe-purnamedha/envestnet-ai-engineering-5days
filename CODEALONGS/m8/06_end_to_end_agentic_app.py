"""One concept: a small app combines tools, policy search, workflow, and answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "m4"))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from workshop_framework_setup import QUESTION, check_guideline, draft_advisor_note, get_current_price, get_portfolio_allocation
from workshop_llamaindex_setup import POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
policy_answer = str(index.as_query_engine(similarity_top_k=2).query("single asset concentration limit"))

price = get_current_price("AAPL")
allocation = get_portfolio_allocation("Alice", "AAPL")
guideline = check_guideline("AAPL", 36.0)
answer = draft_advisor_note(price, allocation, guideline)
answer["policy_context"] = policy_answer
answer["question"] = QUESTION

print("Question:", QUESTION)
print("Answer:", answer)
