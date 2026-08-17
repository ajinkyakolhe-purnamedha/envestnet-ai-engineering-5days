# M1 · Model access quiz

## Multiple choice

1. What is the key engineering lesson of “a model is not a product”?
   - A. A model alone supplies the complete user workflow.
   - B. Product value requires an application boundary, data, policy, and user experience around the model.
   - C. Models should never be called from software.
   - D. Only researchers can ship AI.

2. Which path sends a request to a provider-managed proprietary model?
   - A. A direct Gemini API call
   - B. A local SQLite query
   - C. A Python type hint
   - D. A pytest fixture

3. What does Vertex AI add to a Gemini access path?
   - A. A governed cloud platform boundary and project identity
   - B. Automatic local GPU memory
   - C. A new Python language
   - D. A guarantee of zero latency

4. What does “open weights” mean in this module?
   - A. The model’s parameters are available under the relevant license for people to run or host.
   - B. The model has no parameters.
   - C. The model is always free to operate.
   - D. The model must run in a browser.

5. What is a common advantage of hosted open-weight inference?
   - A. Access to an open-model ecosystem without operating the hardware yourself
   - B. No token charges ever
   - C. No provider boundary
   - D. Guaranteed private data residency

6. What is a common advantage of local open-weight inference?
   - A. The request can stay on the machine under your control.
   - B. It automatically scales to millions of users.
   - C. It removes model-size constraints.
   - D. It never needs a GPU or memory.

7. Which is the soundest default model-selection rule from M1?
   - A. Always choose the largest model.
   - B. Choose the smallest model and simplest deployment that meet the requirement.
   - C. Always choose local inference.
   - D. Choose based only on brand recognition.

8. Why put provider-specific code behind an application boundary?
   - A. To isolate configuration, errors, observability, and future provider changes
   - B. To hide all tests
   - C. To prevent any model replacement
   - D. To make prompts impossible to inspect

9. Which configuration should normally remain out of source control?
   - A. A model’s public name
   - B. An API key
   - C. A function signature
   - D. A test assertion

10. What does the M1 assistant lab ask learners to preserve when calling a model?
   - A. The complete `system + history + current message` transcript
   - B. Only the current message
   - C. Only the system instruction
   - D. The API key in the transcript

## Code reading and debugging

11. In `01_gemini_text.py`, what happens when `GEMINI_API_KEY` is absent?
   - A. The program prints a configuration message and does not call the provider.
   - B. It fabricates a model response.
   - C. It raises a database error.
   - D. It downloads a local model.

12. A learner writes `call_model()` so it returns the provider response object,
    but the lab expects a string reply and tests `result == "..."`. What is the
    bug at the boundary?

13. A local-model demo forwards `local_files_only=True` into text generation and
    Transformers reports that the argument is unused. Where should the setting
    belong, and what should generation receive instead?

## Scenario

14. A team must prototype Chronos with synthetic data this afternoon, but later
    needs governed cloud deployment and usage logging. Which M1 access path do
    you recommend first, and what boundary should remain stable when the path
    changes?

## Capstone transfer

15. For a Chronos “explain my portfolio” feature, define the model-boundary
    function’s input and output types and name one safe behavior for empty or
    failed model output.
