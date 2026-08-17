# M3 · AI application patterns quiz

## Multiple choice

1. Why should instructions, context, questions, and history be kept separate
   while building a model request?
   - A. It makes prompt failures easier to diagnose and change independently.
   - B. It guarantees factual answers.
   - C. It removes the need for tests.
   - D. It makes the model deterministic.

2. What should come before choosing a model or build pattern?
   - A. Define the task, required capability, data boundary, and operating constraints.
   - B. Choose the largest available model.
   - C. Add tools immediately.
   - D. Write the longest possible prompt.

3. What is the usual first pattern for a task that only needs a language
   response from supplied input?
   - A. Direct model call
   - B. Retrieval system
   - C. Fine-tuning
   - D. Agentic workflow

4. When is structured output a good addition to a prompted application?
   - A. When downstream code needs predictable fields and types.
   - B. When there is no downstream code.
   - C. When the response can be ignored.
   - D. When the model should choose its own database schema.

5. When does retrieval earn its additional complexity?
   - A. When the response depends on relevant private, current, or external information not in the prompt.
   - B. Whenever a prompt has more than one sentence.
   - C. When a deterministic rule is missing.
   - D. When the application has no data source.

6. What does fine-tuning primarily change compared with retrieval?
   - A. It changes learned behavior, format, or style; retrieval supplies information at request time.
   - B. It guarantees current facts.
   - C. It replaces all evaluation.
   - D. It is always cheaper than prompting.

7. When does an agentic workflow justify its complexity?
   - A. When the task needs dynamic multi-step decisions, tools, and feedback.
   - B. For every one-step response.
   - C. When no tools are available.
   - D. When the output is always a fixed sentence.

8. What is the difference between schema validation and business validation?
   - A. Schema validation checks shape/types; business validation checks whether the action is allowed.
   - B. Schema validation proves an answer is true.
   - C. Business validation is optional after structured output.
   - D. They are the same check.

9. Why can model selection be treated as an economic decision?
   - A. Capability, latency, cost, privacy, and operations vary across model tiers and deployment choices.
   - B. All models have identical operating costs.
   - C. The cheapest model is always sufficient.
   - D. Model choice affects only branding.

10. What is the central pattern-selection discipline?
    - A. Choose the least complex pattern that reliably meets the requirement and record why simpler options fail.
    - B. Start with an agent and remove features later.
    - C. Use retrieval whenever facts exist.
    - D. Let model confidence replace deterministic tests.

## Code reading and debugging

11. A selector checks for a need for dynamic steps before a need for formatting.
    Why might the order of these checks matter?

12. A model returns a correctly shaped trade object, but the requested allocation
    exceeds policy. What must happen before the object is used?

13. A team adds retrieval to a task whose complete, authoritative context is
    already supplied in the request. Name one likely cost or failure mode.

## Scenario

14. Select a first pattern for each requirement and give one reason:

    - Summarize text already supplied by the user.
    - Return a typed record with fixed fields.
    - Answer using a private, changing policy corpus.
    - Complete a changing sequence of tool calls.

## Capstone transfer

15. For Chronos trade preview, choose a pattern and model tier, name one simpler
    alternative you rejected, and state one deterministic policy check before
    approval.
