import torch
from llama_index.core import Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# Can this use locally downloaded offline model? 
# Add simple instrumentation using opentelemetry here. 

# Initialize local Hugging Face LLM
Settings.llm = HuggingFaceLLM(
    model_name="meta-llama/Llama-3.2-3B-Instruct",
    tokenizer_name="meta-llama/Llama-3.2-3B-Instruct",
    device_map="auto",
    model_kwargs={"torch_dtype": torch.float16},
)

# Initialize local Embedding model for RAG workflows
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Test completion
response = Settings.llm.complete("Explain vector embeddings simply.")
print(response)