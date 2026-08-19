# M4 · Retrieval-Augmented Generation quiz

**Ten questions, one per essential idea in the module.**

Every option is a true statement about building AI applications that this course has taught. Only the option that answers *the question actually asked* is correct. Some questions have more than one right answer; each of those says so.

---

1. Retrieval and fine-tuning are both ways to specialise a model for your organisation. What is the difference in *what each one changes*?
   - A. Retrieval runs as two separate pipelines, one before any question arrives and one while the user is waiting for an answer.
   - B. Retrieval can point back at the document a statement came from, while training spreads everything it learned across the weights.
   - C. Retrieval changes what the model can see at the moment it answers; training changes how the model behaves when it answers.
   - D. Retrieval spends context tokens on every call, while training spends money on hardware once and then serves each call cheaply.

2. Four teams each describe their problem in one sentence. Which one has described a retrieval problem?
   - A. "Our answers have to reflect a policy library that compliance revises every week."
   - B. "Our replies have to arrive in the same JSON schema on every call, without exception."
   - C. "Our task needs several tool calls, and we cannot predict their order ahead of time."
   - D. "Our prompt already works well; it is simply longer and costlier than we would like."

3. In what order does a RAG system perform its five stages?
   - A. Embed the documents, then chunk them, then retrieve, then build the index, then generate the answer.
   - B. Chunk the documents, then build the index, then embed the chunks, then generate, then retrieve passages.
   - C. Retrieve the passages, then chunk them, then embed them, then build the index, then generate the answer.
   - D. Chunk the documents, then embed the chunks, then build the index, then retrieve, then generate the answer.

4. **Select two.** A user submits a question. Which two of these run in response to that question, rather than having already happened before it?
   - A. Splitting the source documents into passages small enough to embed and large enough to still be useful.
   - B. Turning the user's question into a vector that lives in the same space as every passage already indexed.
   - C. Computing an embedding for every passage in the corpus and storing it somewhere that can be searched quickly.
   - D. Reranking the candidate passages, so that only the most relevant few are placed into the final prompt.

5. A policy manual is written as numbered rules under headings. Which chunking decision does this module recommend for it?
   - A. Fixed-size windows with an overlap, so that a fact cut at one boundary survives inside its neighbour.
   - B. Small fixed-size passages, so that each embedding stays focused on one idea and matches a query sharply.
   - C. Splitting on the headings the author already wrote, so that every passage holds one complete rule.
   - D. Semantic splitting, where a new chunk begins wherever the meaning of the text shifts noticeably.

6. **Select two.** Which two describe the cost of using large chunks?
   - A. The embedding has to represent several ideas at once, so it matches any one of them less sharply.
   - B. More of the context window fills with text that has nothing to do with the question being asked.
   - C. A single rule can be cut across a boundary and end up incomplete in both of the passages that result.
   - D. Building the index becomes slow and costly, because deciding each boundary needs its own computation.

7. Your index uses dense vector embeddings. Questions asked in ordinary language work well, but a user searching for a product code such as `X-4471`, or for an internal rule number, gets poor results. What is the argument for running a keyword index alongside the vector one?
   - A. Two retrievers together return a larger candidate set, so recall improves before anything is reranked or trimmed down.
   - B. Keyword scoring is cheap to compute and adds little latency beside the dense search that it runs alongside on every query.
   - C. A larger and more varied candidate pool gives the reranking stage more passages to score before the final selection is made.
   - D. Dense search encodes meaning and misses exact strings; keyword search matches strings and misses meaning, so each covers the other.

8. A pipeline fetches twenty candidate passages from the index, then passes only three of them to the model. Why not simply retrieve three in the first place?
   - A. A cross-encoder reads the question and the passage together, which scores relevance far more accurately than comparing two separate vectors.
   - B. Vector distance is good at pulling the right passage into a pool, and weak at ordering that pool, so a second stage re-scores what it found.
   - C. Combining a dense and a keyword ranking needs a pool that both have already ranked, so the fusion step has two orderings to merge.
   - D. Trimming to three keeps the final prompt small, which lowers the cost per call and leaves room for the instructions and the user's question.

9. A grounded assistant returns the correct source passage at the top of its results, and the answer built from that passage is still wrong. Where is the fault?
   - A. In generation: the model was given the right context and still failed to use it, so look at the prompt or the model.
   - B. In the query: it should be decomposed into independent sub-questions, each of them searched for on its own.
   - C. In the index: exact terms are being missed, so add a keyword stage beside the dense search that runs today.
   - D. In retrieval: the passages need better boundaries, so re-chunk the corpus and add a reranking stage after it.

10. Some questions cannot be answered by retrieving passages at all — totalling a client's gain across a date range, for example, needs a structured query. In the governed pattern this module shows, what does the language model actually get to decide?
    - A. The SQL statement itself, which is then parsed and checked against a schema before it is allowed to execute.
    - B. A small set of values, such as a symbol and a time window, which are validated before a reviewed query uses them.
    - C. Which table and which columns to read, restricted to a set of curated views rather than raw production tables.
    - D. The as-of date for the query, so that the answer can be made correct for whatever point in time the user asks about.
