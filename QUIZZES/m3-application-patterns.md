# M3 · AI application patterns quiz

## Multiple choice

1. Why should instructions, context, questions, and history be kept separate
   while building a model request?
   - A. It makes the model deterministic.
   - B. It makes prompt failures easier to diagnose and change independently.
   - C. It removes the need for tests.
   - D. It guarantees factual answers.

2. What should come before choosing a model or build pattern?
   - A. Add tools immediately.
   - B. Write the longest possible prompt.
   - C. Define the task, required capability, data boundary, and operating constraints.
   - D. Choose the largest available model.

3. What is the usual first pattern for a task that only needs a language
   response from supplied input?
   - A. Agentic workflow
   - B. Retrieval system
   - C. Fine-tuning
   - D. Direct model call

4. When is structured output a good addition to a prompted application?
   - A. When the response can be ignored.
   - B. When downstream code needs predictable fields and types.
   - C. When the model should choose its own database schema.
   - D. When there is no downstream code.

5. When does retrieval earn its additional complexity?
   - A. When the application has no data source.
   - B. Whenever a prompt has more than one sentence.
   - C. When the response depends on relevant private, current, or external information not in the prompt.
   - D. When a deterministic rule is missing.

6. What does fine-tuning primarily change compared with retrieval?
   - A. It replaces all evaluation.
   - B. It is always cheaper than prompting.
   - C. It guarantees current facts.
   - D. It changes learned behavior, format, or style; retrieval supplies information at request time.

7. When does an agentic workflow justify its complexity?
   - A. When no tools are available.
   - B. When the task needs dynamic multi-step decisions, tools, and feedback.
   - C. For every one-step response.
   - D. When the output is always a fixed sentence.

8. What is the difference between schema validation and business validation?
   - A. Business validation is optional after structured output.
   - B. They are the same check.
   - C. Schema validation proves an answer is true.
   - D. Schema validation checks shape/types; business validation checks whether the action is allowed.

9. Why can model selection be treated as an economic decision?
   - A. The cheapest model is always sufficient.
   - B. Capability, latency, cost, privacy, and operations vary across model tiers and deployment choices.
   - C. Model choice affects only branding.
   - D. All models have identical operating costs.

10. What is the central pattern-selection discipline?
    - A. Use retrieval whenever facts exist.
    - B. Let model confidence replace deterministic tests.
    - C. Start with an agent and remove features later.
    - D. Choose the least complex pattern that reliably meets the requirement and record why simpler options fail.

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
