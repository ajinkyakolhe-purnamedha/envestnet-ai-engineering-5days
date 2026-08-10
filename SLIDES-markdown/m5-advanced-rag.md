---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

> Draft version: content is being refined.

# M5 · Advanced RAG Patterns & Evaluation

Advanced query transformations and empirical retrieval metrics

By the end of this module you can:

- Implement Parent-Child hierarchical indexing to decouple search from context
- Apply Hypothetical Document Embeddings (HyDE) to resolve query-doc embedding gaps
- Decompose multi-part user queries into parallel sub-retrieval execution pipelines
- Measure retrieval quality empirically using the RAG Triad (`deepeval`)
- Diagnose whether production failures stem from retrieval noise or model reasoning

<!--
Set expectations: 45 minutes of lecture, followed by a RAG evaluation clinic.

When basic RAG fails in production, teams often misdiagnose the issue as a "weak model" and attempt fine-tuning.

In practice, 80% of RAG failures stem from retrieval deficiencies: poor chunk boundaries, vector distance mismatches between questions and answers, or context window pollution.
-->

---

**Advanced RAG Patterns · 1/3**

# Pattern 1: Hierarchical Chunking (Parent-Child)

### The Dilemma

- **Small Chunks (128 tokens)**: High retrieval precision; vector embedding captures a distinct concept; missing surrounding context for LLM reasoning.
- **Large Chunks (1024 tokens)**: Preserves complete context; diluted vector embedding; lower retrieval match score.

### Parent-Child Architecture

```text
  [ Document ]
      |
  [ Parent Chunk: 1024 tokens ] (Stored in Docstore)
      |
      +---> [ Child 1: 128t ] --\
      +---> [ Child 2: 128t ] ----> Indexed in Vector DB
      +---> [ Child 3: 128t ] --/
```

1. Search matches on **Child Chunk** (high precision).
2. Fetch parent ID from metadata.
3. Pass **Parent Chunk** to LLM prompt (full context).

<!--
Walk through Parent-Child indexing.

Decoupling the unit of RETRIEVAL (small child chunk) from the unit of SYNTHESIS (large parent chunk) resolves the chunk-size dilemma.
-->

---

**Advanced RAG Patterns · 2/3**

# Pattern 2: Hypothetical Document Embeddings (HyDE)

```python
# snippets/m5/hyde.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Resolving Asymmetric Search

1. **Problem**:
   - User queries ("How do I harvest tax losses?") look vectors away from target answer passages ("Loss harvesting involves selling assets at a net loss...").
2. **HyDE Process**:
   - Ask LLM to write a *hypothetical answer* to the prompt.
   - Embed hypothetical answer vector instead of user query.
   - Search index using answer-to-answer vector distance.

<!--
HyDE transforms an asymmetric query-to-document search into a symmetric document-to-document search.

Even if the hypothetical answer contains mild factual inaccuracies, its overall vector trajectory sits close to authentic answer documents in vector space.
-->

---

**Advanced RAG Patterns · 3/3**

# Pattern 3: Sub-Query Decomposition

### Multi-Part User Queries

Users routinely ask questions requiring information from distinct domain areas:

> *"Compare AAPL's 2020 revenue growth against our internal technology exposure limit."*

Single vector search fails because no single document contains both AAPL financial statements and internal policy rules.

### Query Decomposition Pipeline

```text
               [ Complex Query ]
                       |
             (LLM Query Splitter)
                       |
       +---------------+---------------+
       |                               |
  [ Sub-Query 1:               [ Sub-Query 2:
   AAPL Revenue ]               Tech Limits ]
       |                               |
 (Vector Search 1)               (Vector Search 2)
       |                               |
       +---------------+---------------+
                       |
             [ Combined Context ]
                       |
                [ LLM Answer ]
```

<!--
Multi-query decomposition uses a fast model to parse complex questions into independent sub-queries, executes searches in parallel, and merges candidate context prior to final synthesis.
-->

---

# Measuring Retrieval Quality: The RAG Triad

```python
# snippets/m5/rag_eval.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### The 3 Core RAG Metrics

1. **Context Precision**:
   - Percentage of retrieved chunks that are actually relevant.
   - High score = minimal prompt noise.
2. **Faithfulness / Groundedness**:
   - Is every statement in completion supported by retrieved context?
   - Low score = hallucination.
3. **Answer Relevance**:
   - Does completion directly answer the original query?

<!--
The RAG Triad isolates failure locations:
- Low Context Precision $\rightarrow$ Fix retriever, chunking, or reranker.
- Low Faithfulness $\rightarrow$ Reduce system prompt creativity or change model.
- Low Answer Relevance $\rightarrow$ Fix prompt instructions or query decomposition.
-->

---

# Diagnostic Matrix: Failure Mode vs. Fix

| Symptom | Primary Failure Cause | Correct Engineering Action | Incorrect Reaction |
|---|---|---|---|
| **Hallucination in answer** | Retriever fetched irrelevant context | Add reranker; trim top-k; tighten system prompt | Fine-tune model |
| **Missing exact product IDs** | Dense vector keyword mismatch | Enable BM25 hybrid search | Switch to larger LLM |
| **Truncated / missing context** | Small chunk boundary cut sentence | Switch to Parent-Child chunking | Increase temperature |
| **Model ignores retrieved facts** | Context pollution or weak prompt | Re-order context (Lost in the Middle fix) | Fine-tune weights |

**Key Takeaway**: 80% of production RAG issues are solved in the retrieval pipeline, not by modifying weights.

<!--
Walk through the diagnostic table.

Most instincts to fine-tune stem from observing hallucinated or incomplete RAG answers.

Fixing chunking, hybrid search, or context ordering resolves these failures in hours, avoiding weeks of model fine-tuning.
-->

---

<!-- _class: lead -->

# 🧪 Lab: Evaluating & Diagnostic Tuning of Portfolio RAG (45 min)

1. Run `deepeval` test suite over 30 evaluation queries in Chronos Wealth.
2. Measure Context Precision, Faithfulness, and Answer Relevance baseline scores.
3. Add a HyDE transformer and measure precision delta.
4. Replace fixed chunking with Parent-Child indexing and evaluate Context Precision improvements.

Done when: `pytest tests/labs/test_lab5_eval.py` verifies all RAG metrics >= 0.75.

<!--
Introduce Lab 5.

Participants quantitatively benchmark retrieval metrics before and after applying advanced RAG transformations, proving quality improvements empirically.
-->
