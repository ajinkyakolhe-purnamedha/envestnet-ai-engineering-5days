# M7 · Agentic LLMs quiz

**Ten questions, one per essential idea in the module.**

Every option is a true statement from the course. Only the option that answers
the question asked is correct. Some questions have more than one right answer;
each of those says so.

---

1. One assistant answers from policy text. Another asks tools for facts, observes them, then answers. What makes the second one agentic?
   - A. It grounds the answer in retrieved policy text.
   - B. It keeps the transcript for later turns.
   - C. It returns a schema for downstream code.
   - D. It builds the answer from tool observations.

2. The model returns `{"tool": "get_current_price", "args": {"symbol": "AAPL"}}`. What is that output?
   - A. A text request Python must validate and run.
   - B. A trusted function call already in progress.
   - C. A trace record proving which data was used.
   - D. An observation for the next planning turn.

3. **Select two.** Which two jobs belong to Python in the M7 boundary?
   - A. Choose the next missing fact.
   - B. Check the tool allowlist.
   - C. Run the function and catch errors.
   - D. Suggest argument values.

4. A planner asks for an unregistered tool. What should the runtime do?
   - A. Record an error observation.
   - B. Add the tool to the registry.
   - C. Ignore the step and answer anyway.
   - D. Fine-tune the model later.

5. A tool schema has vague descriptions. What failure becomes more likely?
   - A. The function loses database access.
   - B. Trace timing stops being recorded.
   - C. Context grows faster each turn.
   - D. The model guesses bad tool arguments.

6. An agent repeats the same malformed request. What limits the damage?
   - A. A RAG policy tool.
   - B. A Pydantic schema.
   - C. A `max_turns` loop limit.
   - D. A deterministic planner.

7. **Select two.** Which two fields help replay a failed tool step?
   - A. Raw model text and parsed args.
   - B. Final answer and user satisfaction.
   - C. Tool name and observation or error.
   - D. Model family and workflow label.

8. A tool returned the right allocation, but the next turn never saw it. What was missing?
   - A. Better tool schema text.
   - B. Observation feedback in state.
   - C. A framework runtime.
   - D. A model judge.

9. Why start the lab with a deterministic planner?
   - A. To prove agents should avoid models.
   - B. To let models execute Python directly.
   - C. To remove the need for traces.
   - D. To learn the runtime before model variability.

10. What M7 mental model should carry into frameworks?
    - A. Frameworks remove validation.
    - B. Frameworks make RAG the app.
    - C. Frameworks package the same loop parts.
    - D. Frameworks make models catch errors.
