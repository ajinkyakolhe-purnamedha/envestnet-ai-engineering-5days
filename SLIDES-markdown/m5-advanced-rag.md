---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M5.0 · Advanced RAG Improvements & Evaluation

M4 built baseline RAG. M5 improves it only after naming the failure.

By the end of this module, you can:

- run a small RAGAS-style baseline evaluation
- improve chunk shape when context is incomplete
- improve search when dense retrieval misses exact terms
- rerank noisy candidates before generation
- rewrite or decompose queries when the question is the problem

<!--
The module thesis: advanced RAG is diagnosis-driven. Do not present these
techniques as a checklist to add everywhere.
-->

---

# M5.1 · Evaluate The Baseline

Start with a small golden set:

| Item | Example |
| --- | --- |
| question | "Can AAPL be 42%?" |
| expected fact | 35% single-asset limit |
| expected source | Concentration limit |

Then inspect retrieved context before scoring the answer.

<!--
Keep the evaluation set small for class, but call it what it is: a diagnostic
tool, not a benchmark.
-->

---

# M5.1 · Quick RAGAS Pass

RAGAS-style checks ask different questions:

- **context precision**: how much retrieved context was useful?
- **context recall**: did we retrieve the needed evidence?
- **faithfulness**: is the answer supported by context?
- **answer relevance**: did it answer the question?

Source: `CODEALONGS/m5_advanced_rag/01_evaluate_baseline.py`

<!--
If precision fails, look at retrieval. If faithfulness fails with good
context, look at the prompt/model. If relevance fails, look at the question
and answer shape.
-->

---

# M5.2 · Improve Chunks

Baseline chunking fails in two opposite ways:

| Chunk shape | Failure |
| --- | --- |
| too small | precise hit, incomplete answer |
| too large | enough context, noisy retrieval |

Advanced chunking separates search unit from answer unit.

<!--
This section grows directly from M4.3. The baseline gave learners a chunking
knob; M5 shows when that knob is not enough.
-->

---

# M5.2 · Sentence-Window Chunking

```text
document
  -> sentence chunk
  -> sentence chunk + nearby window for answering
```

Search a focused sentence. Answer with its surrounding window.

Source: `CODEALONGS/m5_advanced_rag/03_sentence_window_chunking.py`

<!--
Name related patterns here: sentence windows, hierarchical parsing, and
auto-merging retrieval. The important idea is smaller retrieval units with
larger synthesis context.
-->

---

# M5.3 · Improve Search

Dense retrieval finds meaning.

Sparse retrieval finds exact terms.

Real enterprise questions contain:

- tickers
- policy codes
- percentages
- client names
- ticket IDs

Dense search alone often misses those.

<!--
This is the exact-term failure. Do not bury it in vector math; it is a search
engineering problem the room already understands from keyword systems.
-->

---

# M5.3 · Hybrid Search

```text
dense vector search + sparse BM25 search -> fused candidates
```

Use hybrid retrieval when exact identifiers matter.

Source: `CODEALONGS/m5_advanced_rag/05_hybrid_search.py`

<!--
The snippet uses a tiny deterministic score so the failure is visible: dense
can rank the wrong thing first, sparse rescues the exact term.
-->

---

# M5.4 · Improve Ranking

`top_k` is blunt:

- too narrow misses context
- too wide adds noise

Reranking uses two stages:

```text
retrieve wide -> rerank candidates -> keep the best few
```

<!--
Make the cost trade explicit. The reranker is a second model or scoring step,
so it belongs where precision matters.
-->

---

# M5.4 · Reranking

A retriever scores each chunk independently.

A reranker reads the query and candidate together.

Source: `CODEALONGS/m5_advanced_rag/07_rerank_results.py`

Reranker scores are not similarity scores. Do not compare the numbers as if
they are the same unit.

<!--
This is often the highest-value improvement after hybrid search, but it is
still a measured fix, not a default ornament.
-->

---

# M5.5 · Improve The Query

Sometimes retrieval fails because the user's question is a bad search query:

- vague wording
- comparison question
- multiple facts in one sentence
- answer spread across documents

Fix the search text before searching.

<!--
This section owns HyDE and decomposition. These techniques add LLM calls, so
they should be reserved for query shapes that need them.
-->

---

# M5.5 · Query Transformations

Three common transformations:

- query rewriting
- HyDE: search with a hypothetical answer
- sub-question decomposition

Source: `CODEALONGS/m5_advanced_rag/09_query_transformations.py`

Use them when the measured failure is the query, not the chunks or index.

<!--
HyDE and decomposition belong here, not M4. They change the query before
retrieval and add latency/cost.
-->

---

<!-- _class: lead -->

# M5.L · Lab: Diagnose And Tune RAG

1. Run the M4 baseline.
2. Evaluate a small golden question set.
3. Name the primary failure.
4. Apply one matching fix.
5. Measure before and after.

```text
bad chunks -> advanced chunking
missed exact terms -> hybrid search
noisy top_k -> reranking
bad query -> rewrite / HyDE / decomposition
```

Done when the fix is justified by evidence, not preference.

<!--
The lab should force one change at a time. If learners change chunking,
retrieval, and prompt together, they cannot know what helped.
-->
