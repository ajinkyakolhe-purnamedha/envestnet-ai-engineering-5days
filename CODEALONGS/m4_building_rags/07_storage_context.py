"""One concept: StorageContext saves and reloads a LlamaIndex index."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage

from workshop_llamaindex_setup import PERSIST_DIR, POLICY_DIR, use_local_models


use_local_models()

documents = SimpleDirectoryReader(input_dir=str(POLICY_DIR)).load_data()
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir=str(PERSIST_DIR))

storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
loaded_index = load_index_from_storage(storage_context)

print("persisted:", PERSIST_DIR)
print("loaded:", type(loaded_index).__name__)
