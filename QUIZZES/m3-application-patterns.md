# M3 · AI application patterns quiz

## Multiple choice

1. What should be separated when building a model request?
   - A. Instructions, context, the question, and history
   - B. All code into one function
   - C. The user from the application
   - D. Tests from the source code

2. Why separate these parts?
   - A. It makes failures easier to understand and fix.
   - B. It increases model size.
   - C. It removes the need for data.
   - D. It guarantees a correct answer.

3. What should model selection start with?
   - A. The task and its requirements
   - B. The biggest available model
   - C. A random provider
   - D. The longest prompt

4. What is the simplest useful application pattern?
   - A. A direct model call
   - B. A multi-agent system
   - C. Fine-tuning
   - D. A full retrieval system

5. When is structured output useful?
   - A. When the application needs a predictable response shape
   - B. When no output is needed
   - C. When the model must be hidden
   - D. When a database is unavailable

6. When is retrieval useful?
   - A. When the response needs relevant external, private, or current information
   - B. For every one-sentence question
   - C. Only for changing colors
   - D. To replace all tests

7. When might fine-tuning be useful?
   - A. When repeated behavior or style cannot be achieved reliably with simpler methods
   - B. Whenever a prompt has a typo
   - C. For storing current facts
   - D. For a health endpoint

8. When might an agentic workflow be useful?
   - A. When the system must choose and execute multiple dynamic steps
   - B. For every direct answer
   - C. When no tools exist
   - D. Only for token counting

9. What does schema validation check?
   - A. Whether output has the expected fields and types
   - B. Whether a business decision is allowed
   - C. Whether a model is truthful
   - D. Whether a user is satisfied

10. What is the main M3 design rule?
    - A. Use the least complex pattern that reliably meets the need.
    - B. Always use the most complex pattern.
    - C. Always use an agent.
    - D. Avoid deterministic code.

## Code reading and debugging

11. A function returns `"prompted"` when a requirement includes `"format"`.
    What does that tell you about the function?

12. A model returns the correct fields but an amount violates a business limit.
    What check should happen next?

13. A developer adds retrieval even though all required facts are already in the
    input. What design problem might this create?

## Scenario

14. Choose a suitable first pattern for each task:

    - Answer a question using only the user’s supplied text.
    - Return a response with fixed fields.
    - Look up private documents before answering.
    - Complete a changing sequence of tool calls.

## Capstone transfer

15. For a Chronos trade-preview feature, name the simplest suitable pattern and
    one deterministic rule that must run before any trade is approved.
