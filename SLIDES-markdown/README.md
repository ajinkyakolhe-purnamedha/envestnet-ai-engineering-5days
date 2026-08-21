# Marp Slides

[Marp](https://marp.app) versions of the workshop decks, converted from the
built Slidev modules (now in `../archive/slidev/modules/`), which expand
`../outline.md`. Each deck carries the full slide content, the code snippets
inlined from the Slidev repo's `snippets/` (now `../archive/slidev/snippets/`),
and the complete presenter notes as HTML comments — Marp shows those in
presenter view and can print them in a notes PDF.

| File | Module | Slides |
|---|---|---|
| `00-overview.md` | Workshop title, Day 1 / Day 2 agendas, capstone | 5 |
| `m0-python.md` | M0 · Python & its power in AI | 20 |
| `m1-intro-to-ai-models.md` | M1 · Introduction to AI Models | 17 |
| `m2-model-tokens-context.md` | M2 · Model, Tokens & Context | 16 |
| `m3-application-patterns.md` | M3 · LLM Application Patterns | 8 |
| `m4-building-rags.md` | M4 · Building A Complete Baseline RAG | 18 |
| `m5-advanced-rag.md` | M5 · Advanced RAG Improvements & Evaluation | 12 |
| `m6-fine-tuning.md` | M6 · LLM Fine-Tuning | 19 |
| `m7-agentic-applications.md` | M7 · Agentic LLMs | 19 |
| `m8-agentic-frameworks.md` | M8 · Agentic Frameworks | 18 |

M4-M8 companion files:

- `../CODEALONGS/m4/README.md`: ordered baseline RAG demonstration snippets.
- `../CODEALONGS/m5/README.md`: ordered advanced RAG and evaluation snippets.
- `../CODEALONGS/m6/README.md`: ordered fine-tuning concept snippets.
- `../CODEALONGS/m7/README.md`: ordered plain-Python agent loop snippets.
- `../CODEALONGS/m8/README.md`: ordered smolagents and LlamaIndex framework snippets.

M7 companion files:

- `m7-concepts-reference.md`: dense text reference for the concepts covered in the M7 slides.
- `m7-lab-instructions.md`: notebook lab instructions plus optional Capstone integration hints.

Note: M3 still references placeholder snippet files from the older draft. M4,
M5, M6, M7, and M8 now point to runnable snippets under `../CODEALONGS/`.

## Preview

- **VS Code**: install the "Marp for VS Code" extension, open any file, hit preview.
- **CLI**: no install needed with npx:

```bash
npx @marp-team/marp-cli m0-python.md          # → m0-python.html
npx @marp-team/marp-cli m0-python.md --pdf    # → m0-python.pdf
npx @marp-team/marp-cli -s .                  # live server for the whole folder
```

In the exported HTML, press `p` for presenter view to see the speaker notes.
