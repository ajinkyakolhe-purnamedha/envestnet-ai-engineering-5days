# M5 · Advanced RAG patterns & evaluation quiz

**Ten questions, one per essential idea in the module.**

Every option is a true statement about building AI applications that this course has taught. Only the option that answers *the question actually asked* is correct. Some questions have more than one right answer; each of those says so.

---

1. **Select all that apply.** A team reports that their RAG assistant "needs a smarter model". Which of these can genuinely cause a RAG system to give poor answers?
   - A. The base model is too small for the amount of reasoning that this particular answer requires.
   - B. The retrieval stage is handing back passages that do not actually answer the question asked.
   - C. The chunk boundaries are cutting the relevant rule into pieces that are no longer usable.
   - D. The system prompt leaves the model more freedom to speculate than the task really needs.

2. Small chunks retrieve precisely but leave the model short of context; large chunks carry context but match poorly. How does parent-child indexing settle that argument?
   - A. It searches over the small child passages, then answers from the larger parent that contains them.
   - B. It reranks the candidates so that whichever chunk size scored best rises to the top of the list.
   - C. It stores the document at several chunk sizes and picks whichever one matches the query most closely.
   - D. It rewrites the incoming question so that both the small and the large chunks match it more closely.

3. A user's question and the passage that answers it are written in very different language, so they sit far apart in vector space. Which technique targets exactly that gap?
   - A. Adding a keyword index, so exact terms are matched alongside the meaning of the surrounding text.
   - B. Reranking with a model that reads the question and the passage together before it scores them.
   - C. Splitting the question into independent parts and running a separate search for each one of them.
   - D. Writing a hypothetical answer first, then searching with that instead of the question as it was asked.

4. Your team wants to add a query-transformation step and run it on the cheapest model available. Which technique is the wrong one to economise on, and why?
   - A. Sub-query decomposition, because a bad split silently drops one half of the question the user asked.
   - B. Reranking, because a weak scorer will discard the very passage that you most needed it to keep.
   - C. Hypothetical answer generation, because retrieval inherits the quality of the answer that is written.
   - D. Chunk summarisation, because a poor summary misrepresents the passage that it is standing in for.

5. A user asks a question whose two halves are answered in different documents, and a single search is run. What goes wrong?
   - A. The passages that come back contradict one another, and the model cannot resolve the conflict between them.
   - B. Only one half is covered by the retrieved context, and the model answers as though both halves were.
   - C. The context window overflows, so the passages that were retrieved earliest are silently truncated.
   - D. Both halves match the same passage, so the second search adds nothing the first had not already found.

6. The right passages are being retrieved, and the answer still ignores facts that are sitting inside them. What does the module's diagnostic table recommend?
   - A. Switch to parent-child indexing, so each retrieved passage arrives with its surrounding context intact.
   - B. Add a keyword stage, so exact terms in the question are matched as well as the meaning behind them.
   - C. Fine-tune the model on examples where it uses the supplied context exactly the way you intend it to.
   - D. Re-order the context and tighten the prompt, since the material is there but is being lost inside it.

7. A RAG pipeline can fail in three different places. Which set of measurements covers all three?
   - A. Context precision, faithfulness and answer relevance — retrieval, grounding, and the reply itself.
   - B. Latency, cost per call and cache hit rate — speed, spend, and the efficiency of the assembled prompt.
   - C. Chunk size, top-k and overlap — the settings that decide what retrieval ends up handing to the model.
   - D. Accuracy, precision and recall — the standard measures used whenever a classifier is being scored.

8. Your assistant states a fact that appears nowhere in the passages it retrieved. Which measurement catches that, and what does it compare?
   - A. Context precision, which compares the passages retrieved against what the question actually needed.
   - B. Answer relevance, which compares the answer that was given against the question that was asked.
   - C. Faithfulness, which compares each statement in the answer against the context that was retrieved.
   - D. Retrieval recall, which compares what was retrieved against all of the relevant material available.

9. An evaluation run reports high context precision together with low faithfulness. What does that combination tell you?
   - A. The wrong passages were retrieved, so the model had very little correct material to work from.
   - B. The right passages were retrieved, and the model did not stay inside them when it wrote the answer.
   - C. The answer was well supported by the passages but addressed a different question entirely.
   - D. Retrieval and generation are both healthy, and only the phrasing of the answer is at fault here.

10. Your relevance metric ranks a vague answer above a correct one. What should you do before you trust any of the numbers it produces?
    - A. Raise the threshold on that metric, so that vague answers fall below the passing line.
    - B. Re-run the evaluation over a much larger set of questions, to average out the noise.
    - C. Check the metric itself against a few cases where you already know the right answer.
    - D. Reword the correct answer so that it echoes the wording of the question more closely.
