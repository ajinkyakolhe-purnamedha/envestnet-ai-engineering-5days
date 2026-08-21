# M8 · Agentic frameworks quiz

**Ten questions, one per essential idea in the module.**

Every option is a true statement from the course. Only the option that answers
the question asked is correct. Some questions have more than one right answer;
each of those says so.

---

1. When reading a new agent framework, what should you look for first?
   - A. The company behind it.
   - B. Registry, planner, dispatch, limits, trace.
   - C. How many agent roles it supports.
   - D. Its latest benchmark score.

2. A framework builds tool metadata from functions, hints, and docstrings. What is it helping with?
   - A. Choosing safe business actions.
   - B. Making weak planners reliable.
   - C. Removing the need for traces.
   - D. Exposing Python functions as tools.

3. **Select two.** Which two are warning signs in a framework?
   - A. You cannot inspect prompts or tool calls.
   - B. Your Python functions stay in your code.
   - C. Validation errors appear in the trace.
   - D. You cannot locate where a failure happened.

4. A framework stops after repeated malformed calls. What is the lesson?
   - A. Any model failure makes frameworks unsafe.
   - B. Add more tools so the planner has options.
   - C. Runtime control can work while planning fails.
   - D. RAG prevents malformed tool output.

5. A question can be handled by route -> gather -> check -> draft -> review. Why prefer that over a free loop?
   - A. It removes all model-written prose.
   - B. It makes every step parallel.
   - C. It lets the model call any function.
   - D. It uses the least autonomy that works.

6. **Select two.** Which two pattern matches are correct?
   - A. Chaining: steps are known.
   - B. Routing: first branch varies.
   - C. Parallel gather: one shared DB session.
   - D. Handoff: nobody else must continue.

7. What does M8 do with the Day 2 RAG pattern?
   - A. Replace calculation tools with the vector index.
   - B. Store policy facts in memory.
   - C. Make policy search one agent tool.
   - D. Let the model write SQL.

8. Each agent step adds tokens, latency, context, and retry risk. What follows?
   - A. Raise `max_steps` freely.
   - B. Bigger planners remove tool latency.
   - C. Keep all observations forever.
   - D. Count steps before shipping.

9. A lab workflow uses one SQLAlchemy session. Should those calls be parallelized?
   - A. Yes, all tool calls should be parallel.
   - B. No, replace DB calls with a model summary.
   - C. No, shared DB-session work stays sequential.
   - D. Yes, move the calls into RAG.

10. A drafted note omits the threshold number. Which pattern belongs after drafting?
    - A. Routing.
    - B. Evaluator.
    - C. Handoff.
    - D. Parallel gather.
