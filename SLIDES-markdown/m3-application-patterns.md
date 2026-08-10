---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# M3 · LLM Application Patterns

The five architectural patterns and model economics

By the end of this module you can:

- Identify the five AI build patterns and select the simplest viable approach
- Evaluate trade-offs across cost, latency, determinism, and operational maintenance
- Implement model selection economics and dynamic tier routing
- Test application outputs using `deepeval` assertions
- Harden prompt interfaces against injection vulnerabilities using `promptfoo`

<!--
Set expectations: 45 minutes of theory, followed by model selection clinic.

The primary objective of this module is architectural selection. Engineers often default to complex patterns (such as fine-tuning or multi-agent loops) when a structured prompt or RAG pipeline is sufficient.

We evaluate patterns in order of increasing complexity and operational overhead. Always start with the simplest pattern that satisfies your performance and accuracy requirements.
-->

---

# The Five Build Patterns

| Pattern | Description | Primary Use Case |
|---|---|---|
| **1. Direct Model Call** | Pass raw user input directly to the API | Simple summarization, draft generation |
| **2. Prompt & Context Eng.** | System framing, few-shot examples, structured output | Schema enforcement, classification, formatting |
| **3. RAG (Grounding)** | Retrieve external documents into the context window | Dynamic knowledge, internal docs, search |
| **4. Fine-Tuning** | Update model weights on domain-specific datasets | Custom style, low-latency formatting, offline models |
| **5. Agentic Workflows** | Autonomous loop with external tool calls | Multi-step reasoning, environment interaction |

Rule of thumb: **Start at Pattern 1 and move down only when requirements demand it.**

<!--
Walk through the spectrum clearly.

Each step down the list increases engineering complexity, testing difficulty, and failure surface area:
- Pattern 1 & 2: Stateless API calls with zero infrastructure.
- Pattern 3: Requires retrieval infrastructure (chunking, embeddings, vector database).
- Pattern 4: Requires dataset curation, GPU training pipelines, and custom model serving.
- Pattern 5: Requires non-deterministic loop control, state management, and tool sandboxing.

The main takeaway: Do not adopt Pattern 5 when Pattern 2 solves the problem reliably.
-->

---

# Trade-Off Matrix

| Metric | 1. Direct | 2. Prompt Eng. | 3. RAG | 4. Fine-Tuning | 5. Agentic |
|---|---|---|---|---|---|
| **Implementation Time** | Minutes | Hours | Days | Weeks | Weeks |
| **Token Cost / Query** | Very Low | Low–Medium | Medium–High | Low (Small Base) | High (Multi-turn) |
| **Latency** | Fast (<1s) | Fast (<1s) | Medium (1-3s) | Fast (Small Base) | Slow (5-30s) |
| **Knowledge Recency** | Static | Static | Real-time | Static | Real-time |
| **Determinism** | Low | Medium | High | High | Low |
| **Maintenance** | Minimal | Low | Medium (Vector DB) | High (Re-training) | High (Loop control) |

Notice that RAG solves **knowledge freshness**, fine-tuning solves **format & style**, and agents solve **multi-step execution**.

<!--
Focus on concrete metrics:
- Latency: Direct API calls respond in sub-second time. Agentic loops make 3-10 sequential calls, multiplying latency.
- Cost: RAG inflates input tokens by packing retrieved context. Fine-tuning uses smaller prompts but incurs GPU training and hosting costs.
- Determinism: Prompting with strict schemas achieves medium-high reliability. Agentic loops can diverge or enter loops if tool errors are unhandled.
-->

---

<!-- _class: lead -->

**Model Selection Economics · 1/2**

# Three-Tier Model Hierarchy

**Fast / Edge Tier** — *e.g. Qwen2.5-0.5B, GPT-4o-mini*
- **Latency**: 50–200 ms · **Cost**: ~$0.15 / 1M tokens
- **Use**: Classification, extraction, routing, simple parsing

**Default Tier** — *e.g. Claude 3.5 Haiku, Llama-3.1-8B*
- **Latency**: 300–800 ms · **Cost**: ~$1.00 / 1M tokens
- **Use**: Standard RAG synthesis, summary, reporting

**Deep Reasoning Tier** — *e.g. Claude 3.5 Sonnet, o3-mini*
- **Latency**: 2.0–10.0 s · **Cost**: ~$3.00–$15.00 / 1M
- **Use**: Complex planning, code generation, multi-step analysis

<!--
Model selection is an economic decision.

Using a reasoning tier model for basic intent classification wastes budget and adds unnecessary latency.

A standard production architecture uses a fast classifier to determine request complexity, routing simple queries to cheap models and reserving expensive models for complex analytical tasks.
-->

---

**Model Selection Economics · 2/2**

# Model Routing Implementation

```python
# snippets/m3/routing.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### How Routing Works

1. **Lightweight Classification**:
   - Send prompt to a fast, low-cost tier model.
   - Constrain response to `EASY` or `HARD`.
2. **Dynamic Selection**:
   - Simple prompts execute on low-cost models (`gpt-4o-mini`).
   - Complex prompts escalate to high-capacity models (`gpt-4o`).
3. **Cost Savings**:
   - Reduces average query cost by 60–80% in typical user workloads.

<!--
Walk through the code sample.

Notice temperature is set to 0.0 for classification to maximize determinism.

Phase-based switching is another variation: use a deep model during offline planning phases to generate structured sub-tasks, then execute each individual sub-task using cheap, specialized models.
-->

---

# Testing AI Outputs with Evals

```python
# snippets/m3/deepeval_test.py — snippet file not yet written
# (module is a stub; the snippet must be authored before
#  delivery, per the module's transclusion reference)
```

### Continuous Evaluation

- **`deepeval` Harness**:
  - Runs inside standard `pytest` execution pipelines.
  - Measures non-deterministic outputs using calibrated metrics.
- **Core Metrics**:
  - **Answer Relevancy**: Does output address the input query?
  - **Faithfulness**: Is output grounded in provided context?
  - **Hallucination Rate**: Percentage of ungrounded assertions.

<!--
Software tests verify exact assertions (`assert result == 42`). AI outputs require statistical assertions (`assert relevancy >= 0.7`).

Integrating `deepeval` into pytest allows teams to catch regression issues when updating system prompts or switching model providers.
-->

---

# Hardening Prompt Interfaces with Red Teaming

### Threat Vectors

- **Prompt Injection**: User inputs overriding system instructions ("Ignore previous directives...").
- **Data Leakage**: System prompt or private context exposed in completion.
- **Jailbreaking**: Bypassing safety boundaries via roleplay or encoding.

### Hardening Workflow with `promptfoo`

```bash
# Run automated vulnerability scan
npx promptfoo eval -c promptfooconfig.yaml
```

1. Define test assertions in YAML (injections, PII leakage, refusal checks).
2. Execute automated attack benchmarks against API endpoints.
3. Block deployment if security compliance fails.

<!--
Red-teaming is automated security testing for LLM endpoints.

Promptfoo allows teams to simulate hundreds of injection attacks against prompt templates before releasing changes to production.
-->

---

<!-- _class: lead -->

# 🧪 Lab: Selecting Patterns & Routing Queries for Chronos Wealth (45 min)

1. Benchmark query cost across 3 model tiers using 50 historical portfolio questions.
2. Implement a model router that sends standard price lookups to a local/fast model and portfolio risk analysis to a high-capacity model.
3. Write a `deepeval` test suite verifying answer relevancy on portfolio summaries.

Done when: `pytest tests/labs/test_lab3_patterns.py` passes clean.

<!--
Introduce Lab 3.

Participants measure real latency and token costs across tiers using Chronos Wealth data, establishing empirical justification for model selection.
-->
