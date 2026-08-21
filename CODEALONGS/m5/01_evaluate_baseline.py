"""One concept: use RAGAS to score a tiny LlamaIndex baseline."""

import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from ragas import SingleTurnSample
from ragas.metrics import NonLLMContextPrecisionWithReference, NonLLMContextRecall

from workshop_m5_setup import POLICY_DIR, REFERENCE_ANSWER, REFERENCE_CONTEXT, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
nodes = SentenceSplitter(chunk_size=120, chunk_overlap=0).get_nodes_from_documents(documents)
index = VectorStoreIndex(nodes)

question = "Can one asset be 42% of the portfolio?"
retriever = index.as_retriever(similarity_top_k=2)
retrieved_nodes = retriever.retrieve(question)
query_engine = index.as_query_engine(similarity_top_k=2)
response = query_engine.query(question)

sample = SingleTurnSample(
    user_input=question,
    retrieved_contexts=[node.text for node in retrieved_nodes],
    reference_contexts=[REFERENCE_CONTEXT],
    response=str(response),
    reference=REFERENCE_ANSWER,
)

context_precision = NonLLMContextPrecisionWithReference().single_turn_score(sample)
context_recall = NonLLMContextRecall().single_turn_score(sample)

print("question:", question)
print("answer:", str(response))
print("context_precision:", round(context_precision, 2))
print("context_recall:   ", round(context_recall, 2))
