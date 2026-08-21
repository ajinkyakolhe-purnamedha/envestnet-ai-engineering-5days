# M2 Lab · Budget a Multi-Turn Assistant

Timebox: 60–90 minutes. Extend the M1 assistant idea; do not build a new chat
application and do not make a provider call in your tests.

1. Run `mini_lab.py` and explain why the same context has different costs.
2. Complete `starter.py`: assemble messages, project monthly cost, and choose
   the first model tier to try.
3. Add one synthetic history turn and describe which token component grew.
4. Remove supplied context and record what cost changed and what answer quality
   risk you introduced.

Success: a reviewer can inspect the assembled request, reproduce the token and
cost estimates offline, and understand the cost / latency / model-size trade.
`solution.py` is **Instructor only:** after learners have attempted the starter.
