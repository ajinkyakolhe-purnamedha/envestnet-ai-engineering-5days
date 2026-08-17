# Hints

- A response shape problem starts with a prompted application; use Instructor
  and Pydantic for the schema, then validate business policy in Python.
- Private or changing facts are a retrieval requirement, not a prompt-writing
  problem. Record RAG as the decision; M4 will build it.
- Repeated, stable learned behaviour might justify fine-tuning only after a
  prompt/RAG baseline has evidence of a persistent gap.
- Dynamic steps and tool choice indicate an agentic workflow; M7/M8 own that
  implementation.
- A first test must be observable: a policy cap, a required citation, or a
  known classification—not “the response seems helpful.”
