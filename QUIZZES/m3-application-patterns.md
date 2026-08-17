# M3 · AI application patterns quiz

## Multiple choice

1. Why should instructions, context, questions, and history be kept separate
   while building a model request?
   - A. It makes prompt failures easier to diagnose and change independently.
   - B. It guarantees factual answers.
   - C. It removes the need for tests.
   - D. It makes the model deterministic.

   **Answer: A.** Separation makes prompt failures easier to diagnose and change independently.
   **Why:** Engineers can identify whether the problem is the instruction, context, question, or history.

2. What should come before choosing a model or build pattern?
   - A. Define the task, required capability, data boundary, and operating constraints.
   - B. Choose the largest available model.
   - C. Add tools immediately.
   - D. Write the longest possible prompt.

   **Answer: A.** Define the task, required capability, data boundary, and operating constraints first.
   **Why:** Requirements determine which model and pattern are justified.

3. What is the usual first pattern for a task that only needs a language
   response from supplied input?
   - A. Direct model call
   - B. Retrieval system
   - C. Fine-tuning
   - D. Agentic workflow

   **Answer: A.** A direct call is the usual first pattern for supplied-input language work.
   **Why:** It has the smallest operational surface when no extra capability is required.

4. When is structured output a good addition to a prompted application?
   - A. When downstream code needs predictable fields and types.
   - B. When there is no downstream code.
   - C. When the response can be ignored.
   - D. When the model should choose its own database schema.

   **Answer: A.** Structured output is useful when downstream code needs predictable fields and types.
   **Why:** It creates a machine-readable interface, but policy checks remain separate.

5. When does retrieval earn its additional complexity?
   - A. When the response depends on relevant private, current, or external information not in the prompt.
   - B. Whenever a prompt has more than one sentence.
   - C. When a deterministic rule is missing.
   - D. When the application has no data source.

   **Answer: A.** Retrieval earns complexity when relevant private, current, or external information is missing from the prompt.
   **Why:** Retrieval addresses an information gap; it should not be added without one.

6. What does fine-tuning primarily change compared with retrieval?
   - A. It changes learned behavior, format, or style; retrieval supplies information at request time.
   - B. It guarantees current facts.
   - C. It replaces all evaluation.
   - D. It is always cheaper than prompting.

   **Answer: A.** Fine-tuning changes learned behavior, format, or style; retrieval supplies information at request time.
   **Why:** The two patterns solve different problems.

7. When does an agentic workflow justify its complexity?
   - A. When the task needs dynamic multi-step decisions, tools, and feedback.
   - B. For every one-step response.
   - C. When no tools are available.
   - D. When the output is always a fixed sentence.

   **Answer: A.** Dynamic multi-step decisions, tools, and feedback justify an agentic workflow.
   **Why:** The extra orchestration is earned by changing intermediate steps.

8. What is the difference between schema validation and business validation?
   - A. Schema validation checks shape/types; business validation checks whether the action is allowed.
   - B. Schema validation proves an answer is true.
   - C. Business validation is optional after structured output.
   - D. They are the same check.

   **Answer: A.** Schema validation checks shape and types; business validation checks whether an action is allowed.
   **Why:** A correctly shaped object can still violate policy.

9. Why can model selection be treated as an economic decision?
   - A. Capability, latency, cost, privacy, and operations vary across model tiers and deployment choices.
   - B. All models have identical operating costs.
   - C. The cheapest model is always sufficient.
   - D. Model choice affects only branding.

   **Answer: A.** Capability, latency, cost, privacy, and operations vary across choices.
   **Why:** Model selection is an economic and operating decision.

10. What is the central pattern-selection discipline?
    - A. Choose the least complex pattern that reliably meets the requirement and record why simpler options fail.
    - B. Start with an agent and remove features later.
    - C. Use retrieval whenever facts exist.
    - D. Let model confidence replace deterministic tests.

    **Answer: A.** Choose the least complex pattern that reliably meets the requirement and record why simpler options fail.
    **Why:** Simpler systems usually have fewer cost, latency, failure, and maintenance burdens.

## Code reading and debugging

11. A selector checks for a need for dynamic steps before a need for formatting.
    Why might the order of these checks matter?

    **Answer:** Requirements can overlap; checking dynamic steps first may give agentic behavior precedence over formatting.
    **Why:** Selection logic needs explicit precedence or composition rules when multiple capabilities are required.

12. A model returns a correctly shaped trade object, but the requested allocation
    exceeds policy. What must happen before the object is used?

    **Answer:** Run deterministic business-policy validation and reject or route for approval before any action.
    **Why:** Schema validity does not authorize a business action.

13. A team adds retrieval to a task whose complete, authoritative context is
    already supplied in the request. Name one likely cost or failure mode.

    **Answer:** Retrieval can add latency, cost, irrelevant context, retrieval failures, or conflicting facts.
    **Why:** It adds a failure boundary without solving a real information gap.

## Scenario

14. Select a first pattern for each requirement and give one reason:

    - Summarize text already supplied by the user.
    - Return a typed record with fixed fields.
    - Answer using a private, changing policy corpus.
    - Complete a changing sequence of tool calls.

    **Expected answer:** Direct call; structured output; retrieval; agentic workflow.
    **Why:** Each pattern is the least-complex first choice that adds the needed capability.

## Capstone transfer

15. For Chronos trade preview, choose a pattern and model tier, name one simpler
    alternative you rejected, and state one deterministic policy check before
    approval.

    **Expected answer:** Use prompted structured extraction with a fast/default model; reject an agent because preview is not dynamic multi-step work; enforce allocation and authorization policy before approval.
    **Why:** The decision connects pattern complexity, model economics, safety, and measurable policy controls.
