# M0–M12 Essential Revision — Mnemonic Edition

## The whole course in one chain

**B A C C R I A O F C C G**

**Build → Access → Context → Choose → Retrieve → Improve → Adapt → Orchestrate → Finish → Connect → Curate → Govern**

- M0 Build with Python
- M1 Access models
- M2 Context and tokens
- M3 Choose the simplest pattern
- M4 Retrieve grounded facts (RAG)
- M5 Improve RAG with measurement
- M6 Adapt behaviour (fine-tuning)
- M7 Act through controlled tools
- M8 Orchestrate agentic workflows
- M9 Finish the product safely
- M10 Connect reusable capabilities with MCP
- M11 Curate enterprise data capabilities
- M12 Govern every MCP call

## The course’s non-negotiable rule

**“Model proposes; Python proves.”**

| AI may | Python/application must own |
|---|---|
| Explain, summarize, classify, draft, retrieve, suggest tools | Facts, calculations, policy, permissions, validation, execution, approvals, logging |

For Chronos: use synthetic data and virtual money only; never let the LLM calculate prices/allocations or make trade decisions.

> **How to read the code:** every short block below is written from scratch as a revision sketch. Its comments name the mnemonic stages in execution order; it intentionally teaches the concept rather than recreating the application.

## Use this revision rhythm for every module

```text
Memorize → Understand → Implement → Verify
```

1. Say the mnemonic without looking.
2. Explain what problem it solves—and why a simpler pattern is insufficient.
3. Read the small real-library call and name what each object owns.
4. Predict an observable result: an output, assertion, trace entry, or controlled denial.

---

## M0 — Python foundations

Mnemonic: **V-F-C-D-S-L-T**  
**Variables → Functions → Classes → Database → Server → Logs → Tests**

- Python is the AI-engineering default because it is readable and has a deep AI/data ecosystem.
- AI engineer ships a reliable product; AI researcher improves models.
- `uv` manages project dependencies and repeatable environments.
- Type hints document interfaces; they do not validate values at runtime.
- Functions: one job, clear name, type hints, validate inputs.
- Dataclasses group named data and related behaviour.
- SQLite: always parameterize SQL with `?`.
- Historical data rule: query `date <= simulated_date`, then latest available result.
- FastAPI maps routes to Python functions.
- Logs explain what happened; tests prove expected behaviour.
- **Notebook to explore; `.py` module to ship.**

```python
# V — Variables
share_count, purchase_price = 10, 80.50

# F — Function
def calculate_purchase_cost(share_count: int, purchase_price: float) -> float:
    if share_count <= 0 or purchase_price <= 0:
        raise ValueError("Shares and price must be positive.")
    return share_count * purchase_price

# C — Class/data object
holding_data = {"symbol": "AAPL", "shares": share_count}
# D — Database-shaped data lookup
price_by_symbol = {"AAPL": 80.50}
# S — Server-shaped response
portfolio_response = {"symbol": holding_data['symbol'], "value": calculate_purchase_cost(share_count, price_by_symbol['AAPL'])}
# L — Log useful evidence
print("portfolio response:", portfolio_response)
# T — Test/proof
assert calculate_purchase_cost(share_count, purchase_price) == 805.0
```


## M1 — Models and AI applications

Mnemonic: **M-C-P-W-S-E**  
**Model + Context + Prompt + Workflow + Safety + Evaluation = Product**

- A model is not a product.
- The model supplies language capability; the application assembles permitted context and prompt, places the result in a workflow, then adds safety and evaluation.
- Model families: proprietary/general, open-weight, specialist, multimodal.
- Access choices: provider API, local open weights, or governed cloud platform.
- Choose with: **T-Q-C-D-O-S** — **Task, Quality, Cost, Data boundary, Ownership, Serving effort**.
- Proprietary: fast capability, API/data boundary, token bill.
- Local/open: greater control and privacy, but you own serving and upgrades.
- Use the smallest sufficient model and deployment.
- Keep keys outside code; log model ID, duration, usage, and failures.
- First model call proves access—not correctness.

```python
# M — make one simple model call
from openai import OpenAI

openai_client = OpenAI()
model_response = openai_client.responses.create(
    model="gpt-5-mini",
    input="Explain diversification in one short sentence.",
)
print(model_response.output_text)
```

## M2 — Tokens, context, and cost

### Mnemonic 1 — the application model call

**M-I-C-P-R**  
**Model + Instruction → Context → Prompt → Reply**

- The application assembles every request.
- The model sees only what is sent in that turn.
- There is no automatic server-side conversation memory: resend relevant history.
- Context window contains instruction + history + supplied facts + new prompt.
- More history means more tokens, cost, and latency.
- Tokens are model-specific IDs; they are not embeddings.
- Embeddings enable semantic similarity search; similarity is not truth.
- Select the smallest model that reliably passes representative tests.

### Mnemonic 2 — inside the text model

```text
Text → Tokens → Token IDs → Embeddings → Transformer → Token ID → Text

T-T-I-E-T-I-T
```

The embedding is the token's learned meaning vector. The Transformer stage includes the model's next-token prediction work; it selects the next token ID, which is decoded back to text. Generation repeats this loop until the reply is complete.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# M — selected model capability
model_tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
language_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
# I — instruction; C — context; P — current task
model_messages = [
    # I — instruction
    {"role": "system", "content": "Answer only from supplied context."},
    # C — current permitted facts
    {"role": "system", "content": "Policy: no holding may exceed 35%."},
    # P — user's task
    {"role": "user", "content": "Is AAPL too large at 42%?"},
]
# R — tokenize → generate next token IDs → decode text
prompt_text = model_tokenizer.apply_chat_template(model_messages, tokenize=False, add_generation_prompt=True)
input_token_ids = model_tokenizer(prompt_text, return_tensors="pt")
output_token_ids = language_model.generate(**input_token_ids, max_new_tokens=40, do_sample=False)
reply_text = model_tokenizer.decode(output_token_ids[0], skip_special_tokens=True)
```

```python
# T — input text; T — tokenizer splits it into subword tokens
input_text = "AAPL concentration risk"
subword_tokens = model_tokenizer.tokenize(input_text)

# I — convert tokens to model-specific IDs; E — look up their embedding vectors
token_ids = model_tokenizer(input_text, return_tensors="pt")["input_ids"]
token_embeddings = language_model.get_input_embeddings()(token_ids)

# T — `generate` runs the Transformer and chooses the next token internally
generated_token_ids = language_model.generate(input_ids=token_ids, max_new_tokens=1, do_sample=False)
next_token_id = generated_token_ids[0, -1]

# I/T — next token ID becomes decoded text
next_text = model_tokenizer.decode(next_token_id)
```

### Token count and cost with LiteLLM

**Count → Call → Price.** Count input tokens before the request; price the completed response after it returns.

```python
from litellm import completion, completion_cost, token_counter

messages = [{"role": "user", "content": "Explain diversification in one sentence."}]

# Count the request using the tokenizer for the model being called.
input_token_count = token_counter(model="gpt-4o-mini", messages=messages)

# LiteLLM makes the provider call through one common interface.
model_reply = completion(model="gpt-4o-mini", messages=messages)

# LiteLLM reads response usage and its model-pricing data to calculate USD.
call_cost_usd = completion_cost(completion_response=model_reply)
print({"input_tokens": input_token_count, "cost_usd": call_cost_usd})
```

## M3 — Application patterns

Mnemonic: **D-P-R-F-A**  
**Direct → Prompted → RAG → Fine-tune → Agent**

Use the first rung that works:

1. **Direct call** — self-contained language work.
2. **Prompted application** — controlled instructions or structured output.
3. **RAG** — current, private, or document-based facts and citations.
4. **Fine-tuning** — stable, repeated behavioural gap.
5. **Agentic workflow** — tools and next steps genuinely vary.

- Schema validation checks shape; it does not prove authorization, truth, or safety.
- Deterministic requirements belong in Python.
- A pattern choice is an argument: **data needed → likely failure → simplest pattern → boundary → first test**.

```python
# D — direct: supplied text → model answer
from openai import OpenAI
OpenAI_Client = OpenAI()
Direct_Response = OpenAI_Client.responses.create(model="gpt-5-mini", input="Rewrite this note in plain English.")
# P — prompted: add explicit instruction / output shape
from pydantic import BaseModel
class TradeIntent(BaseModel): symbol: str; shares: int
# R — retrieve: add current/private evidence before answering
from llama_index.core import Document, VectorStoreIndex
documents = [Document(text="AAPL may not exceed 35%.")]
RAG_Query_Engine = VectorStoreIndex.from_documents(documents).as_query_engine()
RAG_Response = RAG_Query_Engine.query("What is the AAPL limit?")
# F — fine-tune: use only after these baselines repeatedly fail on stable work
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM
base_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
fine_tuned_model = get_peft_model(base_model, LoraConfig(r=8, target_modules=["q_proj", "v_proj"]))
# A — agent: let the model choose among approved tools when the next step varies
from smolagents import tool
@tool
def price_tool(symbol: str) -> float:
    """Return a permitted simulated price."""
    return {"AAPL": 108.0}[symbol]
```


## M4 — RAG foundations

Mnemonic: **L-C-E-I-S-R-S**  
**Load → Chunk → Embed → Index/Store → Search/Retrieve → Synthesize**

RAG = **search → provide evidence → synthesize an answer**

- Use RAG for private, current, and verifiable knowledge.
- RAG supplies facts; fine-tuning changes behaviour.
- A chunk is the smallest useful citeable evidence unit.
- Chunk metadata matters: source, title, page, type, date, stable ID.
- Structural chunks are usually better for policies/manuals than arbitrary fixed chunks.
- **Store** keeps vector + chunk text + metadata + stable ID. **Index** is the search structure built over the stored vectors; it makes nearest-neighbour retrieval fast.
- At query time, embed the query too, search the index, retrieve the relevant chunks, and give only that evidence to the model.
- Retrieval result = score + chunk + metadata + source.
- Similarity scores rank candidates; they do not certify truth.
- Ground prompts: “Use only supplied context.”
- Inspect retrieved evidence before trusting the synthesized answer. A good RAG system can say: **“The answer is not in the retrieved evidence.”**

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# L — Load source files into LlamaIndex Document objects.
load_documents = SimpleDirectoryReader("data").load_data()

# C — Chunk documents into small, citeable nodes for retrieval.
chunker = SentenceSplitter(chunk_size=256, chunk_overlap=32)
chunked_nodes = chunker.get_nodes_from_documents(load_documents)

# E — Embed: turn each text node into a meaning vector using an embedding model.
embedder = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# I — Index and store: keep each node, its metadata, and its vector for fast search.
index_store = VectorStoreIndex(chunked_nodes, embed_model=embedder)

# S — Search: embed the question and rank the nearest indexed nodes.
search_retriever = index_store.as_retriever(similarity_top_k=2)

# R — Retrieve: inspect the evidence nodes before trusting an answer.
retrieved_evidence = search_retriever.retrieve("Is a 42% AAPL allocation allowed?")

# S — Synthesize: ask a query engine to answer from the retrieved evidence.
synthesis_query_engine = index_store.as_query_engine(similarity_top_k=2)
synthesized_answer = synthesis_query_engine.query("Is a 42% AAPL allocation allowed?")
```

### Evidence first; abstain when there is none

**Retrieve → inspect evidence → answer, or abstain.** A fluent answer is not evidence. If retrieval returns nothing, the application must say so instead of inventing an answer.

```python
question = "What is the permitted allocation range for this account?"
retrieved_evidence = search_retriever.retrieve(question)

if not retrieved_evidence:
    # No retrieved source means there is no grounded basis for an answer.
    answer = "I cannot answer that from the available documents."
else:
    # Show the evidence that will ground the answer: source, rank score, and text.
    for evidence in retrieved_evidence:
        print({
            "source": evidence.node.metadata.get("file_name"),
            "score": evidence.score,
            "text": evidence.node.get_content(),
        })

    # Only synthesize after evidence exists. M5 improves relevance and ranking.
    answer = synthesis_query_engine.query(question)

print(answer)
```


## M5 — Advanced RAG

Mnemonic: **L-C-E-I-S-I-R-S-E**  
**Load → Chunk → Embed → Index/Store → Search → Improve → Retrieve → Synthesize → Evaluate**

- M5 keeps the M4 pipeline but improves the measured weak link.
- Start with a golden set: question, expected fact, expected source.
- Diagnose retrieval before blaming generation; evaluate the retrieved context before scoring the answer.
- Core measures:
  - Context precision: was retrieved material useful?
  - Context recall: was needed evidence found?
  - Faithfulness: is the answer supported?
  - Answer relevance: did it answer the question?
- Improve chunks: sentence-window chunking searches a precise sentence, then supplies its nearby window for answering.
- Improve search: hybrid search = dense semantic retrieval + sparse/BM25 exact-match retrieval.
- Improve ranking: retrieve wide, then rerank candidates and retain the best few.
- Improve query when query formulation caused the failure: rewrite, HyDE, or sub-question decomposition, then search again.

| M4 baseline | M5 improvement loop |
|---|---|
| Build one pipeline and inspect retrieved evidence. | Start with a failed golden-set case. |
| `top_k` retrieval supplies context. | Measure whether chunks, search, ranking, or query caused the miss. |
| Produce a grounded answer or abstain. | Change one weak stage, rerun, and compare metrics. |

```text
baseline search failure
→ improve chunks, search, ranking, or query
→ retrieve the best evidence
→ synthesize a grounded answer
→ final evaluation
```

```python
from llama_index.core.postprocessor import SentenceTransformerRerank

# L/C/E/I/S — use the M4 index and retrieve wide
wide_search_retriever = index_store.as_retriever(similarity_top_k=8)
candidate_nodes = wide_search_retriever.retrieve("Can AAPL be 42%?")
# I/R — rerank candidates, then keep the best evidence
reranking_model = SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=2)
best_evidence = reranking_model.postprocess_nodes(candidate_nodes, query_str="Can AAPL be 42%?")
# S/E — synthesize from best_evidence, then score against a golden answer
```


## M6 — Fine-tuning

Mnemonic: **P-F-R-T**, after the pretraining lifecycle  
**Prompt → Few-shot → RAG → Tune**

Fine-tuning changes **behaviour**, not current knowledge.

- Base-model lifecycle: a very large pretraining corpus (often many terabytes at frontier scale) + expensive compute + long training time → pretrained model.
- Fine-tuning starts with that pretrained model, a much smaller task-specific dataset, and a measured behaviour gap.
- With LoRA, the base model stays frozen; small trainable adapter matrices are added to selected layers and trained on the custom examples.
- The deployed result is usually **pretrained base model + task-specific adapter**.
- Good uses: repeatable format, style, classification, extraction, small-model adaptation.
- Dataset row: instruction + input + desired output.
- Hold out evaluation data before training.
- Training inputs: `input_ids`, `attention_mask`, `labels`.
- Completion-only loss: mask prompt labels with `-100`; train on the answer.
- LoRA: freeze base model, train small adapters—not a complete new foundation model.
- QLoRA: quantize frozen base model; train adapters efficiently.
- Watch validation loss: train down + validation down improves; validation up indicates overfitting.
- Evaluate against **base model + prompt**.
- Ship/version the adapter, not an entire replacement model.

```python
# P/F/R are baselines to try before training:
# prompt-only → few-shot examples → retrieved facts → fine-tune only if behaviour still fails
# P — one clear instruction
prompt_only_instruction = "Extract ticker and share count as JSON."
# F — a few labelled examples demonstrate the required shape
few_shot_examples = [("Buy 10 AAPL", '{"symbol": "AAPL", "shares": 10}')]
# R — retrieved policy supplies facts that must stay current
retrieved_policy = "Allowed symbols: AAPL, SPY, QQQ."
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM

# Pretraining: load an already pretrained base model
pretrained_base_model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
# T — LoRA adds trainable adapters while the base weights remain frozen
lora_configuration = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16,
                    target_modules=["q_proj", "v_proj"])
fine_tuned_adapter_model = get_peft_model(pretrained_base_model, lora_configuration)
fine_tuned_adapter_model.print_trainable_parameters()
```


## M7 — Agentic LLMs

Mnemonic: **P-A-V-E**  
**Parse → Allowlist → Validate → Execute**

Agent loop: **Ask → Reason/Reflect → Act → Observe → Repeat or Final**

- RAG grounds in text; agents take controlled steps through software.
- A programmer writes ordinary functions. The LLM dynamically decides whether a permitted function is needed; that model-callable function is a **tool**.
- A tool has a name, type-hinted arguments, a clear result shape, failure modes, and an owner. It is plug-and-play capability, not unrestricted code execution.
- The LLM suggests a tool + arguments; Python validates, executes, records observations, and stops loops.
- A tool request—often JSON—is not execution.
- Treat tool arguments as external API input.
- Tool execution path: `raw model output → parse → tool allowlist → argument validation → Python execution`.
- Failures become observations, not crashes.
- `max_turns` is a required safety, cost, and latency boundary.
- Trace every run: question, raw tool request, args, validation, observation, final answer, stop reason.

```python
import json
from pydantic import BaseModel

# Programmer creates fixed, type-described tools
class ToolRequest(BaseModel): tool: str; args: dict[str, str]
Allowed_Tools = {"price": lambda symbol: {"symbol": symbol, "price": 108.0}}
# Ask/Reason: model proposes this request
Parsed_Tool_Request = ToolRequest.model_validate_json('{"tool":"price","args":{"symbol":"AAPL"}}')
# Act safely: P-A-V-E = parse, allowlist, validate, execute
Requested_Tool_Name, Requested_Arguments = Parsed_Tool_Request.tool, Parsed_Tool_Request.args
if Requested_Tool_Name not in Allowed_Tools:                  # allowlist
    raise ValueError(f"Unknown tool: {Requested_Tool_Name}")
if Requested_Arguments["symbol"] not in {"AAPL", "SPY"}: # validate arguments
    raise ValueError("Unsupported symbol")
# Observe: Python returns the deterministic result to the next model turn
Tool_Observation = {"tool": Requested_Tool_Name, "result": Allowed_Tools[Requested_Tool_Name](**Requested_Arguments)}
# Repeat only while the runtime's max_turns limit permits it.
```

## M8 — Agentic frameworks

Mnemonic: **S-M-H = Same Mechanism, Hidden differently**

- Frameworks package the same M7 loop; they do not eliminate it.
- Learn one tiny tool first: `add(a: int, b: int) -> int`. Each framework turns that same typed Python capability into a model-callable tool.

| Runtime concept | LlamaIndex | smolagents | Haystack |
|---|---|---|---|
| Expose the function | `FunctionTool` | `@tool` | component/tool wrapper |
| Planner | agent LLM | `ToolCallingAgent` model | agent/generator component |
| Dispatch | framework tool runtime | framework tool runtime | pipeline/tool runtime |
| Same essentials | tool schema, arguments, result, limit, trace | tool schema, arguments, result, limit, trace | tool schema, arguments, result, limit, trace |

- Always locate: tool registry, planner, dispatch, observations, step limit, trace.
- Frameworks are useful only when runtime behaviour remains inspectable.
- RAG can become an agent tool.
- Workflow patterns: chaining, routing, parallel gather, evaluator, handoff.
- Autonomy ladder: **Fixed workflow > Routed workflow > Agent loop**.
- Choose the least autonomy that works.
- Each step adds model tokens, tool latency, parse/retry risk, and trace volume.

### The ReAct loop that every framework packages

```python
max_turns = 3
observations = []
question = "What is AAPL's price?"
allowed_tools = {"get_price": lambda symbol: {"symbol": symbol, "price": 108.0}}

def planner(question: str, observations: list[dict]) -> dict:
    if not observations:
        return {"type": "tool", "tool": "get_price", "args": {"symbol": "AAPL"}}
    return {"type": "final", "answer": f"AAPL is {observations[-1]['result']['price']}."}

for turn in range(max_turns):
    # Reason — the model decides the next need from question + observations.
    model_step = planner(question, observations)

    # Final — stop when the model returns an answer rather than a tool request.
    if model_step["type"] == "final":
        final_answer = model_step["answer"]
        break

    # Act — Python, not the model, runs an allowed tool.
    tool_result = allowed_tools[model_step["tool"]](**model_step["args"])

    # Observe — the result becomes evidence for the next model turn.
    observations.append({"tool": model_step["tool"], "result": tool_result})
else:
    final_answer = "Stopped: max_turns reached."
```

```python
# Same typed Python capability in every framework
def add_numbers(first_number: int, second_number: int) -> int:
    return first_number + second_number

# LlamaIndex: Python function → FunctionTool
from llama_index.core.tools import FunctionTool
LlamaIndex_Add_Tool = FunctionTool.from_defaults(fn=add_numbers)

# smolagents: Python function → @tool metadata
from smolagents import tool
@tool
def Smolagents_Add_Tool(First_Number: int, Second_Number: int) -> int:
    """Add two integers."""
    return First_Number + Second_Number

# Haystack: function + JSON schema → Tool → ToolInvoker
from haystack.components.tools import ToolInvoker
from haystack.tools import Tool
Haystack_Add_Tool = Tool(name="add", description="Add two integers.", function=add_numbers,
    parameters={"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]})
Haystack_Tool_Invoker = ToolInvoker(tools=[Haystack_Add_Tool])
```

Framework syntax changes; the core is still typed Python tool → model planning → controlled dispatch → trace.

## M9 — Finish an agentic product safely

Mnemonic: **M-V-H-P**  
**Memory → Verify → Human gate → Persist**

- M9 turns an agentic workflow into a product-safe system: **agentic workflow + memory → verification → human escalation → durable state and trace**.
- Memory is application-managed history of relevant prior questions, actions, tool outputs, and drafts—not a model superpower.
- Bound memory with a window, summary, or retrieval—starting with a window.
- Scope memory by user/advisor/client/workflow/permission.
- Verification ladder: **Rules → Model judge → Human**.
- Rules run for every output.
- Model judges are advisory until measured against known labels.
- Do not use a fully automated LLM-only system for client-facing, money-moving, or regulator-visible outcomes: escalate to a human approval gate.
- Client-visible generated content begins as a **pending draft**, not as a sent message.
- State machine: `pending → approved` or `pending → rejected`.
- Only approved content reaches the client.
- Persist pending drafts, decisions, and audit traces.
- Trace: question, effective question, route, facts, draft, rules, judge verdict, approval, stop reason.

```python
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage
from openai import OpenAI

# M — LlamaIndex memory supplies bounded prior conversation
Conversation_Memory = ChatMemoryBuffer.from_defaults(token_limit=500)
Conversation_Memory.put(ChatMessage(role="user", content="Policy limit is 35%."))
Effective_Question = Conversation_Memory.get() + [ChatMessage(role="user", content="Why is that a problem?")]
# V — rules plus an advisory model judge assess the draft
Generated_Draft = "AAPL at 42% is above the 35% limit."
Rules_Pass = "35%" in Generated_Draft and len(Generated_Draft.split()) <= 30
Judge_Verdict = OpenAI().responses.create(
    model="gpt-5-mini", input=f"Does this cite a threshold? YES or NO.\n{Generated_Draft}"
).output_text.strip()                       # advisory, not final authority
def Get_Client_Visible_Drafts(All_Drafts: list[dict[str, object]]) -> list[dict[str, object]]:
    return [Draft for Draft in All_Drafts if Draft["status"] == "approved"]

# H — a real human supplies this decision; rules and judge never approve alone.
Pending_Draft = {"note": "AAPL exceeds the 35% threshold.", "status": "pending"}
def record_human_decision(draft: dict, decision: str) -> dict:
    if decision not in {"approved", "rejected"}:
        raise ValueError("Human decision must be approved or rejected.")
    draft["status"] = decision
    return draft

advisor_decision = "approved"  # supplied by the reviewing advisor, not the LLM
Pending_Draft = record_human_decision(Pending_Draft, advisor_decision)
# P — persist draft, decision, and trace; only approved rows become visible
Persisted_Drafts = [Pending_Draft]
```

## M10 — MCP fundamentals

Mnemonic: **D-U-C-R**  
**Discover → Understand → Call → Result**

MCP = a shared way for applications to find and call external capabilities.

- Roles: user → host app → MCP client → MCP server → tool.
- The model is not the network client; the application owns the connection.
- MCP primitives: tool = parameterized job; resource = named context; prompt = reusable wording.
- Function calling and MCP work together: function calling helps the model choose; MCP makes tools reusable.
- Share capabilities, not applications, prompts, permissions, or authority.
- A good MCP tool is a **small promise**: clear name, narrow inputs, predictable output.
- MCP alone does not provide authentication, authorization, limits, or audit.

```python
# fastmcp_server.py — standalone FastMCP library
from fastmcp import FastMCP

fastmcp_server = FastMCP("Portfolio Server")

@fastmcp_server.tool
def get_portfolio_summary(client_id: str) -> dict:
    """Return one client's bounded portfolio facts."""
    return {"client": client_id, "cash": 25_000}
```

```python
# official_mcp_server.py — official MCP Python SDK v2
from mcp.server import MCPServer

mcp_server = MCPServer("Portfolio Server")

@mcp_server.tool()
def get_portfolio_summary(client_id: str) -> dict:
    """Return one client's bounded portfolio facts."""
    return {"client": client_id, "cash": 25_000}
```

Both libraries turn the same typed Python function into the same MCP tool contract: name, input schema, description, and result.

```python
# ai_application.py — the host owns the MCP client and the model call
from mcp import Client
from openai import OpenAI

async def answer_portfolio_question(question: str) -> str:
    async with Client("http://localhost:8000/mcp") as mcp_client:
        discovered_tools = await mcp_client.list_tools()       # D — Discover
        approved_tool = "get_portfolio_summary"               # U — admit/understand one tool
        tool_result = await mcp_client.call_tool(              # C/R — Call → Result
            approved_tool, {"client_id": "alice"}
        )

    model_response = OpenAI().responses.create(
        model="gpt-5-mini",
        input=f"Use these portfolio facts only: {tool_result.structured_content}\n{question}",
    )
    return model_response.output_text
```

The host application discovers and calls a server-owned capability; the model does not directly connect.

## M11 — Enterprise data tools

Mnemonic: **Q-C-C-P**  
**Question → Curated data product → Contract → Published capability**

- Do not give agents raw SQL, arbitrary tables, or generic API access.
- Ask: **What is the smallest business question this capability should answer?**
- Design a curated data product, then expose it as a narrow MCP tool.
- Contract must specify: small inputs, useful bounded result, provenance/source, freshness/as-of date, and controlled absence/not-found path.
- Match capability to the question: RAG for textual policy evidence; deterministic query/aggregation for structured facts; market-data service for prices.
- RAG does not calculate structured facts.
- Same trusted facts can support different experiences, but not identical authority or outputs.

```python
# Q — start from a business question: small current portfolio view
Business_Question = "What are Alice's two largest positions?"
# C — curated data product, not raw database rows
def Build_Portfolio_View(Client_ID: str, Maximum_Positions: int) -> dict:
    if Maximum_Positions not in {1, 2, 3}:      # C — contract-bound input
        raise ValueError("max_positions must be 1, 2, or 3")
    return {"client": Client_ID, "positions": ["SPY", "AAPL"][:Maximum_Positions], "source": "approved view"}

Curated_Portfolio_View = Build_Portfolio_View("alice", Maximum_Positions=2)
# P — publish this small contract as an MCP tool, not the database itself
from mcp.server.fastmcp import FastMCP
Curated_Data_MCP_Server = FastMCP("Curated Data")
Curated_Data_MCP_Server.tool()(Build_Portfolio_View)
```

The bounded business contract is the capability—not raw database access.

## M12 — MCP governance

Mnemonic: **A-S-B-A**  
**Admit → Scope → Bound → Audit**

A model proposal is input—not authority.

```text
model proposes
→ host admits approved tool
→ server authorizes + validates
→ bounded result or controlled denial
→ audit event
```

- **Admit:** discovered tools are not automatically model-visible.
- **Scope:** authenticate caller; server checks client/resource authorization before any data read.
- **Bound:** types are not enough—enforce business limits such as rows, fields, positions, cost, time, and concurrency.
- **Audit:** capture correlation ID, caller, tool, validated request, decision, outcome, duration.
- Do not log secrets, full private portfolios, or unnecessary tool results.
- Denial must stop downstream access—not merely return a polite message.
- Capability blast-radius ladder: read → bounded facts; draft → pending review; delivery/mutation → durable human approval workflow.

```python
# A — host admits only approved tools; S — server checks caller's scope
from pydantic import BaseModel, Field
assigned_clients = {"advisor_01": {"alice"}}
audit_log = []
class ReviewRequest(BaseModel): client_id: str; max_positions: int = Field(ge=1, le=2)
def request_client_review(caller_id: str, client_id: str) -> None:
    if client_id not in assigned_clients[caller_id]:
        # B — deny before reading; result remains bounded/contained
        print("DENY: unassigned_client; read service not called")
        audit_log.append({"caller": caller_id, "decision": "deny"})
        return
    bounded_result = {"client": client_id, "largest_position": "SPY"}  # bounded read
    print("ALLOW", bounded_result)
    audit_log.append({"caller": caller_id, "decision": "allow"})

# A — record audit event: caller, tool, validated request, decision, outcome
```

Authorization happens on the server before the data service runs.

## Active-recall cards: boundary, misuse, and proof

| Module | Do not use it for | Ownership to say aloud | Predict / verify |
|---|---|---|---|
| M0 | hiding invalid inputs in calculations | Python owns inputs and tests | What does an invalid share count do? |
| M1 | treating a model call as a product | App owns context, workflow, safety, eval | What evidence proves model access? |
| M2 | assuming the model remembers unseen turns | App owns messages and token budget | What changes if history is removed? |
| M3 | choosing RAG/agent because the name sounds advanced | Python owns the pattern decision | Which smallest rung fits this task? |
| M4 | deterministic calculations or missing corpus facts | Retrieval owns evidence; model synthesizes | Which chunk supports the answer? |
| M5 | tuning before locating the measured failure | Evaluation owns the improvement decision | Was the miss chunk, query, rank, or generation? |
| M6 | current/private knowledge | Data teaches behaviour; retrieval supplies facts | Did adapter beat base + prompt on held-out data? |
| M7 | a fixed sequence of Python steps | Model proposes; Python validates and executes | What observation follows an unknown tool? |
| M8 | using a framework as a black box | Runtime owns limits, dispatch, trace | Where does `max_turns` stop the loop? |
| M9 | fully automated consequential delivery | Human owns final client-visible approval | Can a judge approve a draft by itself? |
| M10 | one private local helper with no reuse need | Host owns connection and model exposure | What tools did the client discover and call? |
| M11 | raw SQL or unrestricted vendor APIs | Server owns curated business facts | What is the bounded contract and provenance? |
| M12 | prompt-only permissions | Server owns authorization and audit | Does denial happen before the data read? |

## Miscellaneous implementation cards — local model integrations

These cards use a model already served locally by `ollama serve`. They are implementation choices that can support several modules; they do not replace the deterministic boundaries taught above.

### 1. LiteLLM calling an Ollama-served model

```python
from litellm import completion

ollama_response = completion(
    model="ollama/qwen3:4b",
    api_base="http://localhost:11434",
    messages=[{"role": "user", "content": "Explain diversification in one sentence."}],
)

print(ollama_response.choices[0].message.content)
```

### 2. Official Ollama Python package

```python
import ollama

ollama_response = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user", "content": "Explain diversification in one sentence."}],
)

print(ollama_response["message"]["content"])
```

### 3. LlamaIndex Settings: two local LLM routes + one embedding model

**Route A — Ollama LLM:** LlamaIndex sends generation requests to a model already served by `ollama serve`.

**Route B — Hugging Face LLM:** LlamaIndex loads the model weights through Transformers in the Python process; no Ollama server is involved.

```python
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Route A: LlamaIndex → Ollama local server → Ollama-served LLM.
Settings.llm = Ollama(model="qwen3:4b", request_timeout=120.0)

# Both routes can use the same local Hugging Face embedding model.
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.context_window = 8_192
Settings.num_output = 512
```

```python
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM

# Route B: LlamaIndex → Transformers → Hugging Face model weights in this process.
Settings.llm = HuggingFaceLLM(
    model_name="HuggingFaceTB/SmolLM2-135M-Instruct",
    tokenizer_name="HuggingFaceTB/SmolLM2-135M-Instruct",
    context_window=8_192,
    max_new_tokens=512,
    generate_kwargs={"do_sample": False},
    device_map="auto",
)

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
```

## Final exam-style checklist

Before shipping any AI application, ask:

1. What exact job is the AI doing?
2. What must remain deterministic Python?
3. Which facts are current/private and need retrieval?
4. What is the smallest model and simplest pattern that passes?
5. What is the context/token/cost budget?
6. Are output shape and business policy validated separately?
7. If tools exist, are they allowlisted, validated, bounded, traced, and loop-limited?
8. If output is high-stakes, are rules, review, approval, and durable state in place?
9. If capabilities are reused, is MCP exposing a narrow contract rather than raw internals?
10. Can an unauthorized or unsafe request be denied before any data/action occurs?

> **Use AI for language and assistance; use deterministic software for truth, authority, safety, and consequential action.**
