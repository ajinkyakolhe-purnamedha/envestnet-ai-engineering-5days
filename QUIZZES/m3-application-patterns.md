# M3 · AI application patterns quiz

## Multiple choice

1. Which four request parts should an engineer keep separate while diagnosing a model failure?
   - A. Instruction, context, question, and conversation history
   - B. GPU, CPU, disk, and memory
   - C. User, database, browser, and router
   - D. Token, parameter, vendor, and license

2. What is the first model-selection question?
   - A. Which model is most famous?
   - B. What capability, data boundary, latency, cost, and operating constraints does the job require?
   - C. Which model has the longest name?
   - D. Can the prompt be made longer?

3. In open-model selection, why consider the family before the exact version?
   - A. Family behavior, license, modalities, and tool support are broader design choices than a version label.
   - B. Versions never matter.
   - C. Families determine the user’s password.
   - D. Version numbers are token IDs.

4. What is one important dial represented by open-model parameter size?
   - A. Capability and resource demand, with larger sizes generally needing more compute or memory
   - B. The number of application users
   - C. The number of validation rules
   - D. The context history itself

5. What changes when using a closed model service?
   - A. The team makes an HTTP/service call and pays for usage instead of operating model weights and GPUs.
   - B. The team receives the provider’s training data.
   - C. All operating concerns disappear.
   - D. Tokens become free.

6. Which pattern is the least complex fit for a task requiring only a direct language response?
   - A. Direct call
   - B. RAG
   - C. Fine-tuning
   - D. Agentic workflow

7. Which pattern adds typed structure to a model response?
   - A. Prompted application with structured output
   - B. SQLite
   - C. Health check
   - D. Tokenization

8. What does RAG add that a direct call does not inherently have?
   - A. A retrieval boundary for supplying relevant private or current facts
   - B. Guaranteed correctness
   - C. A larger parameter count
   - D. A local GPU

9. What is the correct relationship between schema validation and business validation?
   - A. Schema validation checks shape/types; deterministic business rules still need separate checks.
   - B. Schema validation approves every business decision.
   - C. Business validation is unnecessary after an LLM call.
   - D. They are identical.

10. What is the M3 selection discipline?
   - A. Choose the first/least-complex pattern that reliably meets the requirement and write down why.
   - B. Start with agents for every problem.
   - C. Add retrieval before understanding the data.
   - D. Let model confidence replace a test.

## Code reading and debugging

11. Given `choose_pattern({"format"})`, what does the current function return,
    and why does it not return `rag`?

12. A prompted extraction returns valid JSON with `allocation_percent: 80`,
    while policy allows at most 35. What check is missing?

13. A developer chooses an agentic workflow for a fixed one-step portfolio
    explanation. What design/debugging question should they ask first?

## Scenario

14. In the M3 selection clinic, one Chronos idea needs current private policy
    facts, another only needs a fixed response format, and a third needs a
    multi-step tool loop. Choose the first pattern for each and state one reason
    a simpler pattern would fail.

## Capstone transfer

15. For a Chronos trade-preview feature, select the least-complex application
    pattern, define one deterministic contract that must run before any action,
    and name the evidence you would use to justify the selection.
