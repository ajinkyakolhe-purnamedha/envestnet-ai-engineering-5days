---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M13 · Testing an AI Application with Pytest

LLM output varies.

We cannot make LLM output deterministic.

We can make the application response deterministic.

<!-- Timing: 1 minute. Position M13 after the product feature and MCP boundaries. Today is about proving Python reacts safely when an LLM, retriever, or tool does not behave as hoped. -->

---

# M13 turns a working feature into a tested feature

```text
M9  product state + human approval
M12 MCP policy boundary
M13 pytest proves known failure paths
```

<!-- Timing: 3 minutes. M13 does not reteach MCP governance or human approval. It tests that those controls work when the complete application receives uncertain input. -->

---

# What pytest tests—and what it does not

| Pytest proves | Pytest does not prove |
| --- | --- |
| parsing, policy, state, limits | model intelligence |
| safe errors and side effects | universal helpfulness |

<!-- Timing: 3 minutes. This prevents an impossible testing promise. We use a fake planner to prove our Python contract, not to claim the model is good. -->

---

# The small Chronos AI application

```text
request → planner → retrieval / tool → Python policy → result
                                      ↘ draft approval state
```

Uncertain: planner, retrieval, tool availability

Deterministic: Python response

<!-- Timing: 4 minutes. Point out that every external or model boundary may fail. The service is deliberately tiny so the seams fit on one screen. -->

---

# Seven contracts make uncertainty testable

```text
planner → shape → evidence → capability → dependency → budget → approval
```

<!-- Timing: 2 minutes. Preview the ladder. Each next contract only matters after the preceding failure path has been made visible. -->

---

# A pytest test has one job

```python
# Arrange an uncertain boundary.
# Act through the real application service.
# Assert the visible safe result and side effect.
```

<!-- Timing: 3 minutes. Name Arrange, Act, Assert. Stress that a test should assert application behaviour, not whether a fake object exists. -->

---

# 1 · Replace the live LLM with a scripted planner

Source: `m13_testing_evaluating_agents/01_inject_fake_planner.py`

```text
same scripted proposal
        ↓
same test result on every run
```

<!-- Timing: 4 minutes. A scripted planner is an explicit test double. It is not a fake success path; it gives the application a controlled LLM-shaped input. -->

---

# Run the permitted-path test

```python
result = app.handle("Review Alice's simulated portfolio.")

assert result.status == "complete"
assert gateway.calls == ["alice"]
```

<!-- Timing: 2 minutes. Run card 01. The assertion observes both the user-visible result and the real gateway boundary. -->

---

# 2 · The model can return malformed output

```text
missing field · extra field · wrong shape
        ↓
must not become a tool request
```

<!-- Timing: 2 minutes. A JSON-looking response is not automatically valid. Ask what must not happen: no retrieval or tool call. -->

---

# Parameterize the failure shapes

Source: `m13_testing_evaluating_agents/02_malformed_model_output.py`

```python
@pytest.mark.parametrize("bad_proposal", [
    {"client_id": "alice"},
    {"kind": "review", "client_id": "alice", "rows": "all"},
])
```

<!-- Timing: 3 minutes. Run card 02. One test contract covers several input variants without copy-paste. The expected result is controlled rejection and zero gateway calls. -->

---

# 3 · RAG without evidence must abstain

```text
policy question
    ↓
retrieval returns no trusted source
    ↓
needs_evidence—not an invented answer
```

<!-- Timing: 2 minutes. Connect to M4 and M5. This is not a retrieval-quality score; it is a deterministic application fallback when evidence is absent. -->

---

# Test the RAG fallback

Source: `m13_testing_evaluating_agents/03_no_trustworthy_evidence.py`

```python
assert result.status == "needs_evidence"
assert result.source_ids == []
assert app.audit_events == ["retrieval_empty"]
```

<!-- Timing: 3 minutes. Run card 03. The three assertions show the caller state, evidence state, and audit evidence. -->

---

# 4 · A proposed capability is not authority

```text
model proposes a tool or client
        ↓
Python admits capability and scope
        ↓
gateway call—or denial before it
```

<!-- Timing: 2 minutes. Recall M12: discovery is not admission and a claimed client is not authorization. M13 proves the application stops correctly. -->

---

# Test invalid tool and invalid scope

Source: `m13_testing_evaluating_agents/04_reject_invalid_capability.py`

```text
export_all_holdings → denied, no gateway call
Bob review          → denied, no gateway call
```

<!-- Timing: 3 minutes. Run card 04. The same boundary handles an unadmitted capability and an unassigned client. Highlight the observable absence of gateway calls. -->

---

# 5 · Dependencies can fail too

```text
retriever / MCP tool timeout
        ↓
controlled application state
        ↓
safe retry or user message
```

<!-- Timing: 2 minutes. A timeout is not a model failure, but the AI application must handle it just as deliberately. -->

---

# Test a retrieval timeout

Source: `m13_testing_evaluating_agents/05_handle_dependency_failure.py`

```python
assert result.status == "dependency_unavailable"
assert app.audit_events == ["retrieval_timeout"]
```

<!-- Timing: 3 minutes. Run card 05. The fake dependency raises a real TimeoutError; the application translates it into a stable product state. -->

---

# 6 · Valid-looking work can still run away

```text
review → review → review → ...

Python owns max_steps.
```

<!-- Timing: 2 minutes. The risk is no longer malformed output. Each proposal is valid, but unlimited repeated work is still unsafe. -->

---

# Test the agent step budget

Source: `m13_testing_evaluating_agents/06_bound_repeated_requests.py`

```python
assert result.status == "max_steps_reached"
assert result.steps == 2
assert gateway.calls == ["alice", "alice"]
```

<!-- Timing: 3 minutes. Run card 06. This proves both the stopping state and exactly how much downstream work happened before it. -->

---

# 7 · A useful draft is not delivery

```text
generated client note
        ↓
draft-1 / approval_required
        ↓
human reviews before release
```

<!-- Timing: 2 minutes. Connect to M9. This is a durable product state, not an instruction in a system prompt. -->

---

# Test the approval boundary

Source: `m13_testing_evaluating_agents/07_require_human_approval.py`

```python
assert result.draft_id == "draft-1"
assert drafts.statuses == ["approval_required"]
```

<!-- Timing: 3 minutes. Run card 07. The test does not inspect persuasive text; it proves the workflow saved a pending draft rather than delivering it. -->

---

# Regressions turn incidents into permanent evidence

```text
failure → named pytest test → fix → keep test → CI
```

<!-- Timing: 3 minutes. A production failure should become another small test with a precise name. The suite gets stronger as the application changes. -->

---

# Run the complete M13 contract suite

```bash
uv run python -m pytest m13_testing_evaluating_agents/0[1-7]_*.py -q
```

```text
9 passed
```

<!-- Timing: 2 minutes. Run this exact command. Explain that a pull request should not ship if a deterministic safety contract regresses. -->

---

<!-- _class: lead -->

# Lab · Turn seven red tests green

Implement one safe application response at a time.

<!-- Timing: 3 minutes. The lab starts from an incomplete service and seven failing test files. Learners do not add model access; they make Python own every failure path demonstrated today. -->
