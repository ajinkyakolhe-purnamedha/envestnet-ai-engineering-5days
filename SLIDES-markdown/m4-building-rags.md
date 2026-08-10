---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M4 · Retrieval-Augmented Generation (RAG)

Grounding language models in dynamic & structured knowledge

By the end of this module you can:

- Build an end-to-end vector retrieval pipeline from raw documents
- Select chunking strategies appropriate for specific document layouts
- Implement hybrid search combining dense vectors with sparse keyword indexing
- Apply reranking models to improve precision on top-k context retrieval
- Connect LLMs to structured data stores using Text-to-SQL over DuckDB / Parquet

<!--
Set expectations: 60 minutes lecture, followed by a hands-on RAG implementation lab.

RAG addresses the fundamental limitation of LLM parametric memory: models cannot access private, offline, or real-time enterprise data without re-training.

Rather than altering model weights, RAG retrieves relevant document passages at query time and injects them directly into the context window.
-->

---

# The 5-Step RAG Architecture

```text
  [ Raw Data ] ---> 1. Chunking ---> 2. Embeddings ---> [ Vector Database ]
                                                               |
  [ User Query ] ---> 3. Retrieve Top-K Passages <--------------+
                             |
                             v
  [ Prompt Construction ] ---> 4. LLM Generation ---> [ Grounded Response ]
```

### Ingestion Pipeline (Offline)
1. Load raw files (PDF, Markdown, HTML, CSV).
2. Split documents into discrete text chunks.
3. Generate dense vector embeddings per chunk.
4. Persist vectors and metadata in an index.

### Query Pipeline (Online)
1. Convert incoming user query into vector space.
2. Search index for top-k nearest neighbors.
3. Assemble context prompt: System + Context + Query.
4. Pass context prompt to LLM for final synthesis.

<!--
Walk through the separation between ingestion (offline/batch) and query resolution (online/real-time).

Ingestion happens asynchronously as data changes. Query resolution must run within user latency budgets.
-->

---

# Text Chunking Strategies

**Fixed Character / Token** — *e.g. 512 tokens, 50 overlap*
- **Pros**: Fast, simple implementation.
- **Cons**: Splits sentences and key facts mid-phrase.
- **Use**: Generic unstructured text without strong formatting.

**Structural / Sentence** — *e.g. Markdown headers, Python functions*
- **Pros**: Preserves natural semantic boundaries.
- **Cons**: Variable chunk size; headers can yield tiny chunks.
- **Use**: Technical documentation, codebases, manuals.

**Semantic Splitting** — *e.g. Embedding distance threshold*
- **Pros**: Groups text by semantic coherence.
- **Cons**: High computational cost during ingestion.
- **Use**: Dense articles with shifting topics.

<!--
Chunk size represents a trade-off:
- Smaller chunks (128–256 tokens): Higher retrieval precision, but risks losing surrounding context.
- Larger chunks (1024+ tokens): Retains context, but increases noise and consumes context window space.
- Overlap (10-20%): Prevents information loss at boundary splits.
-->

---

# Naive RAG Implementation

```python
# snippets/m4/naive_rag.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Pipeline Breakdown

1. **`SimpleDirectoryReader`**: Loads documents from specified filesystem path.
2. **`VectorStoreIndex`**: Chunks document text, calls embedding model, and constructs in-memory vector store.
3. **`as_query_engine`**: Assembles retrieval prompt and passes retrieved context to LLM.

<!--
This is the baseline implementation using LlamaIndex.

While naive RAG works well on small, distinct document sets, production enterprise datasets expose three major failure modes:
1. Vocabulary mismatch (synonyms missed by dense vector distance).
2. Out-of-order information loss across chunks.
3. Irrelevant context polluting the prompt when top-k returns noisy chunks.
-->

---

# Improving Retrieval: Naive vs. Advanced RAG

### Limitations of Naive Vector Search

- **Exact Term Sensitivity**: Product SKU codes or acronyms can fail dense vector distance lookups.
- **Fixed Top-k Noise**: Fetching top 10 chunks may return 2 relevant passages and 8 irrelevant passages.
- **Single-Query Dependence**: User queries are often vague or poorly framed for vector search.

### The Production RAG Pipeline

1. **Query Transformation**: Rewrite user query into multiple specific search variations.
2. **Hybrid Search**: Combine Dense Vector Search (semantic) with Sparse BM25 Search (exact keywords).
3. **Cross-Encoder Reranking**: Re-score top 20 candidate chunks down to top 3 high-precision passages.

<!--
Explain why production RAG uses hybrid search + reranking.

Dense embeddings capture conceptual similarity ("cost" ≈ "price"), while sparse BM25 index captures exact identifiers ("AAPL", "Rule 401b").

A cross-encoder reranker evaluates the full query-chunk pair jointly, scoring relevance far more accurately than bi-encoder vector similarity alone.
-->

---

# Hybrid Search & Reranking

```python
# snippets/m4/hybrid_rerank.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Two-Stage Retrieval

1. **Stage 1 (Retrieval)**:
   - Over-fetch top 10–20 candidates using hybrid vector + keyword search.
   - Low latency, high recall.
2. **Stage 2 (Reranking)**:
   - Pass candidate passages to `SentenceTransformerRerank` (cross-encoder).
   - Re-score and trim candidates to top 2 high-precision chunks.

<!--
Walk through the code logic.

Stage 1 optimizes for recall (getting the right document into the candidate pool).
Stage 2 optimizes for precision (ensuring only relevant context reaches the LLM context window).
-->

---

# Structured Retrieval: Text-to-SQL

### When Vector RAG Fails

Vector similarity search cannot reliably calculate sums, averages, or point-in-time constraints over tabular numbers:

> *"What was the total return of Alice's portfolio between March and June 2020?"*

Vector search returns static CSV rows; it cannot perform mathematical aggregation across trade dates.

### Governed Structured Retrieval

- **Data Product**: Curate views over DuckDB / Parquet files rather than exposing raw production databases.
- **Pydantic Validation**: Force Text-to-SQL models to output validated SQL syntax.
- **Execution Sandbox**: Run SQL queries in read-only sessions with timeouts.

<!--
Point-in-time correctness and financial aggregations require structured retrieval (Text-to-SQL / Pandas execution), not document vector search.

In Chronos Wealth, portfolio trades and historical close prices live in SQLite/Parquet, so portfolio value calculations execute as SQL queries.
-->

---

<!-- _class: lead -->

# 🧪 Lab: Building a Portfolio RAG Assistant for Chronos Wealth (70 min)

1. Ingest market reports and investment policy PDFs using structural chunking.
2. Index document chunks with local embedding weights (`snowflake-arctic-embed-xs`).
3. Build a hybrid query engine with a cross-encoder reranker.
4. Implement SQL tool retrieval over SQLite portfolio data to answer point-in-time balance queries.

Done when: `uv run pytest tests/labs -m lab` passes Lab 3 tests clean.

<!--
Introduce Lab 3.

Participants complete the RAG pipeline by connecting unstructured policy document retrieval with structured SQL querying over Chronos Wealth portfolio tables.
-->
