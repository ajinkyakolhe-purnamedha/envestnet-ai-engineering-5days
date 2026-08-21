# M4 · Building A Complete Baseline RAG

M4 builds the baseline retrieval pipeline one visible step at a time. Each
snippet is a tiny runnable demonstration; run them in filename order.

```bash
cd CODEALONGS
uv run python m4_building_rags/01_why_rag_exists.py
```

| Snippet | Teaches one thing |
| --- | --- |
| `01_why_rag_exists.py` | RAG supplies facts through a LlamaIndex query engine |
| `02_simple_rag_llamaindex.py` | LlamaIndex can build simple RAG in a few lines |
| `03_complete_pipeline_objects.py` | the named LlamaIndex objects in the pipeline |
| `04_sentence_splitter_nodes.py` | `SentenceSplitter` turns documents into nodes |
| `05_nodes_with_metadata.py` | node metadata carries source information |
| `06_vector_store_index.py` | `VectorStoreIndex` stores searchable nodes |
| `07_storage_context.py` | `StorageContext` persists and reloads indexes |
| `08_vector_retriever_top_k.py` | retrievers return `NodeWithScore` results |
| `09_query_engine_sources.py` | grounded answers use source nodes |
| `10_end_to_end_llamaindex_rag.py` | complete baseline RAG in LlamaIndex |

Each snippet follows normal LlamaIndex getting-started style. The only workshop
setup is `use_local_models()`, which swaps in local deterministic models so the
examples run without model downloads or credentials.
