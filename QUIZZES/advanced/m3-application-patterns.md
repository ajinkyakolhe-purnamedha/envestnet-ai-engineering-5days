# M3 · AI application patterns — advanced quiz

## Multiple choice

1. A response is wrong even though the model followed the instruction. Which
   prompt component should be investigated first if the required fact was absent?
   - A. Context/data boundary
   - B. Temperature only
   - C. UI color
   - D. Database connection pool size

2. A team chooses RAG because a task is important, but all authoritative facts
   are already passed in a compact request. What is the strongest objection?
   - A. Retrieval adds a data boundary and failure modes without solving a real information gap.
   - B. RAG cannot return text.
   - C. RAG always changes model behavior.
   - D. Direct calls cannot be tested.

3. Which requirement most clearly earns structured output?
   - A. A downstream service must receive validated fields with stable types.
   - B. A user wants a creative paragraph.
   - C. The application has no downstream consumer.
   - D. The model should decide policy.

4. Which requirement most clearly earns fine-tuning rather than retrieval?
   - A. Consistent classification style/format after a representative labeled dataset exists.
   - B. Access to today’s changing policy document.
   - C. One missing customer fact.
   - D. A deterministic allocation limit.

5. Which requirement most clearly earns an agentic workflow?
   - A. The system must choose tools and steps based on intermediate results.
   - B. The system must summarize one supplied paragraph.
   - C. The system must return three fixed fields.
   - D. The system must validate one integer.

6. Why should model tier selection be phase-aware?
   - A. Planning and execution may have different capability, latency, and cost needs.
   - B. One model cannot ever serve two phases.
   - C. Cheap models are always better at planning.
   - D. Model tiers affect only licensing.

7. What is the correct order for a generated trade object?
   - A. Parse/validate schema, apply deterministic business policy, then request approval or action.
   - B. Execute first, validate later.
   - C. Let model confidence replace policy.
   - D. Retrieve a random similar trade.

8. Why is a written pattern decision valuable in an enterprise team?
   - A. It records assumptions, rejected simpler options, and evidence for future ownership and change.
   - B. It prevents all future redesign.
   - C. It substitutes for testing.
   - D. It makes a model open-weight.

9. A direct call has adequate quality but misses private current facts. What is
   the smallest likely architectural change?
   - A. Add a grounded retrieval/context boundary before escalating to a more complex pattern.
   - B. Add an agent immediately.
   - C. Fine-tune on the current facts.
   - D. Increase temperature.

10. What is the main reason to prefer a simpler pattern when it meets the target?
    - A. Fewer components reduce latency, cost, failure modes, and maintenance burden.
    - B. Simple systems never fail.
    - C. Complex systems cannot be evaluated.
    - D. Simplicity guarantees model truth.

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
