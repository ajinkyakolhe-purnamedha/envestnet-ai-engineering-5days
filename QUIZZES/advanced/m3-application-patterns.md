# M3 · AI application patterns — advanced quiz

## Multiple choice

1. A response is wrong even though the model followed the instruction. Which
   prompt component should be investigated first if the required fact was absent?
   - A. UI color
   - B. Context/data boundary
   - C. Database connection pool size
   - D. Temperature only

2. A team chooses RAG because a task is important, but all authoritative facts
   are already passed in a compact request. What is the strongest objection?
   - A. Direct calls cannot be tested.
   - B. RAG cannot return text.
   - C. Retrieval adds a data boundary and failure modes without solving a real information gap.
   - D. RAG always changes model behavior.

3. Which requirement most clearly earns structured output?
   - A. The model should decide policy.
   - B. A downstream service must receive validated fields with stable types.
   - C. A user wants a creative paragraph.
   - D. The application has no downstream consumer.

4. Which requirement most clearly earns fine-tuning rather than retrieval?
   - A. One missing customer fact.
   - B. A deterministic allocation limit.
   - C. Access to today’s changing policy document.
   - D. Consistent classification style/format after a representative labeled dataset exists.

5. Which requirement most clearly earns an agentic workflow?
   - A. The system must validate one integer.
   - B. The system must choose tools and steps based on intermediate results.
   - C. The system must return three fixed fields.
   - D. The system must summarize one supplied paragraph.

6. Why should model tier selection be phase-aware?
   - A. Model tiers affect only licensing.
   - B. One model cannot ever serve two phases.
   - C. Planning and execution may have different capability, latency, and cost needs.
   - D. Cheap models are always better at planning.

7. What is the correct order for a generated trade object?
   - A. Let model confidence replace policy.
   - B. Retrieve a random similar trade.
   - C. Execute first, validate later.
   - D. Parse/validate schema, apply deterministic business policy, then request approval or action.

8. Why is a written pattern decision valuable in an enterprise team?
   - A. It substitutes for testing.
   - B. It makes a model open-weight.
   - C. It prevents all future redesign.
   - D. It records assumptions, rejected simpler options, and evidence for future ownership and change.

9. A direct call has adequate quality but misses private current facts. What is
   the smallest likely architectural change?
   - A. Fine-tune on the current facts.
   - B. Increase temperature.
   - C. Add a grounded retrieval/context boundary before escalating to a more complex pattern.
   - D. Add an agent immediately.

10. What is the main reason to prefer a simpler pattern when it meets the target?
    - A. Complex systems cannot be evaluated.
    - B. Simplicity guarantees model truth.
    - C. Simple systems never fail.
    - D. Fewer components reduce latency, cost, failure modes, and maintenance burden.

## Code reading and debugging

11. A selector returns `agentic` whenever requirements contain `dynamic_steps`,
    even if the task also requires private facts. What design question is still
    unresolved?

12. A structured output parser accepts a valid object with an unauthorized
    account ID. Which layer is missing, and why is the parser insufficient?

13. A pattern evaluator reports that a RAG answer is relevant but not faithful
    to the retrieved source. What should be investigated next?

## Scenario

14. For each case, choose the least-complex first pattern and one measurable
    acceptance criterion:

    - Summarize supplied text.
    - Extract a typed client request.
    - Answer from a changing internal policy corpus.
    - Coordinate several tools with conditional next steps.

## Capstone transfer

15. For Chronos trade preview, write a short architecture decision: selected
    pattern, model tier, rejected alternative, deterministic gate, and one metric
    that would trigger reconsideration.
