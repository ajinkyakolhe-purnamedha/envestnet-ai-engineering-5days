# M5 · Advanced RAG Improvements And Evaluation

M5 starts from the M4 baseline and improves it only after naming the failure.
Each snippet is a tiny runnable demonstration; run them in filename order.

```bash
cd CODEALONGS
uv run python m5_advanced_rag/01_evaluate_baseline.py
```

| Snippet | Teaches one thing |
| --- | --- |
| `01_evaluate_baseline.py` | evaluate retrieval and answer quality separately |
| `03_sentence_window_chunking.py` | search a sentence, answer with surrounding context |
| `05_hybrid_search.py` | dense and sparse search fail differently |
| `07_rerank_results.py` | retrieve wide, then rerank candidates |
| `09_query_transformations.py` | rewrite, HyDE, and decomposition change the query |

The snippets are deterministic stand-ins for production techniques. The point
is diagnosis: choose the cheapest improvement that fixes the measured failure.
