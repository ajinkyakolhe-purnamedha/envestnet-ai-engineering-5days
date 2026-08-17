# M1 answer key

1. B — Product value comes from the surrounding application system.
2. A — Direct Gemini is the proprietary provider path.
3. A — Vertex adds a governed cloud/platform boundary.
4. A — Open weights refers to available parameters under a license.
5. A — Hosting is delegated while the open ecosystem remains available.
6. A — Local inference can keep requests on the machine.
7. B — Use the smallest sufficient model and deployment.
8. A — A boundary isolates provider concerns and makes change manageable.
9. B — API keys are secrets.
10. A — The assistant sends system instructions, prior history, and the current message.
11. A — It prints the missing-key instruction and skips the call.
12. The boundary returns the wrong abstraction; normalize the provider result to the string contract expected by the assistant and tests.
13. `local_files_only` belongs in model loading/configuration. Generation should receive only generation parameters supported by the model call.
14. Start with a deterministic/offline or hosted prototype, depending on the team’s constraints, but keep a provider-neutral `call_model(messages) -> str` boundary and logging around it.
15. Example: input is a list of role/content messages; output is a string. On empty output, return a safe fallback such as “I could not produce an answer; please try again.”
