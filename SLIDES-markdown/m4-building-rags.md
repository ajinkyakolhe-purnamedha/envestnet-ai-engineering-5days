---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M4.0 · Building A Complete Baseline RAG

RAG is a retrieval pipeline around an LLM: prepare knowledge, index it, search
it, then answer from retrieved evidence.

By the end of this module, you can:

- Explain why retrieval is different from long context and fine-tuning
- Run a first simple RAG query with LlamaIndex
- Chunk source documents into retrieval units with source metadata
- Build a simple searchable index over chunks
- Retrieve top-k context and inspect the scores
- Generate a grounded answer with citations

<!--
M4 is the baseline RAG module. The job today is ownership of the pipeline:
document, chunk, vector, index, retrieval result, prompt, answer.
-->

---

# M4.1 · Why RAG Exists

Three facts make bare model calls insufficient:

| Gap | Why it matters |
| --- | --- |
| Private knowledge | the model has not read your policies or client notes |
| Current knowledge | policies and prices change after training |
| Verifiable knowledge | an answer needs a source a human can inspect |

```text
RAG = search -> paste -> ask
```

<!--
Connect back to M3: RAG is the custom-knowledge pattern. It earns its
complexity when the answer depends on facts outside model weights.
-->

---

# M4.1 · RAG Is Not Fine-Tuning

| Need | Better first tool |
| --- | --- |
| Add or remove a policy fact | RAG |
| Cite the source document | RAG |
| Change output format or tone | fine-tuning |
| Reduce repeated instruction cost | fine-tuning |

Fine-tuning teaches behavior. Retrieval supplies facts.

Source: `CODEALONGS/m4_building_rags/01_why_rag_exists.py`

<!--
The important boundary for Day 2: M4/M5 teach custom knowledge. M6 teaches
custom behavior. If a fact changes tomorrow, edit the file and re-index; do
not retrain weights.
-->

---

# M4.2 · Simple RAG In LlamaIndex

The first working shape is intentionally small:

```python
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
answer = index.as_query_engine().query(question)
```

Source: `CODEALONGS/m4_building_rags/02_simple_rag_llamaindex.py`

<!--
Show the win early. Participants should see that a framework can build the
whole thing quickly before we open the abstraction and inspect its parts.
-->

---

# M4.2 · What The Framework Hid

That short demo still did every RAG step:

```text
document reader -> splitter -> embedding model -> vector index
question -> retriever -> prompt builder -> answer
```

M4 opens those objects one at a time.

Source: `CODEALONGS/m4_building_rags/03_complete_pipeline_objects.py`

<!--
This prevents LlamaIndex from feeling magical. The rest of the module explains
what the framework did on their behalf.
-->

---

# M4.3 · The Complete RAG Pipeline

```text
load documents
  -> chunk documents
  -> embed chunks
  -> store in an index
  -> retrieve top-k chunks
  -> build grounded prompt
  -> generate cited answer
```

Frameworks package these same steps. They do not remove them.

<!--
Name the steps before showing framework names. The learner should be able to
point at each object in code before trusting an abstraction.
-->

---

# M4.3 · Frameworks Wrap The Same Steps

| Framework | What it gives you |
| --- | --- |
| LlamaIndex | document readers, nodes, indexes, query engines |
| LangChain | loaders, splitters, vector store adapters, chains |
| Haystack | document stores, retrievers, pipelines |

The abstraction is useful only after the pipeline is legible.

<!--
Do not turn this into a framework survey. Show that every cookbook line hides
the same load/chunk/embed/index/retrieve/prompt sequence.
-->

---

# M4.4 · Chunking

Documents are not retrieval units.

```text
document  ->  chunks / nodes  ->  searchable rows
```

A chunk should be the smallest useful piece of evidence the answer can cite.

Source: `CODEALONGS/m4_building_rags/04_sentence_splitter_nodes.py`

<!--
This is the main design idea of M4. Chunking is not cosmetic formatting; it is
the unit of retrieval.
-->

---

# M4.4 · Fixed vs Structural Chunks

| Strategy | Strength | Risk |
| --- | --- | --- |
| Fixed size | simple, predictable | cuts through facts and headings |
| Structural | follows author boundaries | variable chunk size |

For policies, manuals, and code, structural chunking is the baseline.

<!--
Use the mini policy file. Fixed chunks are easy to explain, but policy rules
already have headings. Use the document's own structure before inventing one.
-->

---

# M4.4 · Size, Overlap, Metadata

Three decisions travel with every chunk:

- **size**: precise retrieval vs enough surrounding context
- **overlap**: protects boundary facts, but duplicates text
- **metadata**: source, title, page, type, last updated

```text
chunk text + metadata = citeable retrieval unit
```

Source: `CODEALONGS/m4_building_rags/05_nodes_with_metadata.py`

<!--
Metadata is the bridge from search result to citation. If you do not carry the
source forward here, you cannot show it later without guesswork.
-->

---

# M4.5 · Indexing And Vector Databases

An index stores one searchable representation per chunk.

```text
chunk -> embedding/vector -> index row
```

Each row needs:

- vector
- chunk text
- source metadata
- stable id

Source: `CODEALONGS/m4_building_rags/06_vector_store_index.py`

<!--
The snippet uses word-count vectors so the mechanism is visible. Real RAG uses
learned embedding vectors, but the shape of the object is the same.
-->

---

# M4.5 · Re-Indexing Is A Real Cost

You re-index when you change:

- the source documents
- the chunking strategy
- the embedding model
- metadata that is embedded or filtered

In-memory indexes are fine for learning. Persistent vector stores matter when
the corpus is large or reused.

Source: `CODEALONGS/m4_building_rags/07_storage_context.py`

<!--
This gives vector databases their place without making them mystical. They are
persistent searchable stores for vectors plus metadata.
-->

---

# M4.6 · Retrieval And Grounded Answering

At query time:

```text
user question -> query vector -> similarity search -> top-k chunks
```

The retrieval result is not just text:

```text
score + chunk + metadata + source
```

Source: `CODEALONGS/m4_building_rags/08_vector_retriever_top_k.py`

<!--
Make the result shape explicit. Debugging starts by printing the retrieved
chunks and asking whether the answer is actually present.
-->

---

# M4.6 · Scores Are Rankings, Not Truth

`top_k` controls how many chunks the model reads.

Too low:

- answer may be missing

Too high:

- prompt gets noisy
- cost rises
- model can be distracted

Similarity scores rank candidates. They do not certify correctness.

<!--
This prepares M5 without teaching M5 yet. Reranking and hybrid search exist
because top_k is blunt.
-->

---

# M4.6 · Grounded Prompt Construction

```python
prompt = f"""Use only the context below.

Context:
{retrieved_text}

Question: {question}
Answer with the source title."""
```

Source: `CODEALONGS/m4_building_rags/09_query_engine_sources.py`

<!--
RAG's prompt trick is deliberately simple. Most quality work is making the
retrieved text good enough to paste here.
-->

---

# M4.6 · Missing Answers

A good RAG system must say when the answer is not in the retrieved context.

Failure modes:

- retrieval missed the right chunk
- the corpus does not contain the answer
- the model ignored the instruction

M5 starts by measuring which one happened.

<!--
This is the bridge to evaluation. Do not solve it yet; name the diagnostic
question.
-->

---

# M4.7 · End-To-End Baseline RAG

The full baseline:

```text
load -> chunk -> index -> retrieve -> answer
```

Run the whole pipeline over the policy corpus, then inspect every object it
created.

Source: `CODEALONGS/m4_building_rags/10_end_to_end_llamaindex_rag.py`

<!--
This is the possession check. If learners can print document, chunks, index
rows, retrieved chunks, prompt, and answer, they own baseline RAG.
-->

---

<!-- _class: lead -->

# M4.L · Lab: First Policy RAG

Build a policy assistant that:

1. loads the policy file
2. chunks by headings
3. indexes each chunk
4. retrieves top-k evidence for a question
5. answers only from retrieved context
6. prints the source title

Done when the answer cites the retrieved policy chunk and does not invent a
missing rule.

<!--
Keep the lab scoped to baseline mechanics. The lab should leave a baseline
that M5 can improve.
-->
