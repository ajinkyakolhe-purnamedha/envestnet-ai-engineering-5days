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
| `m4-building-rags.md` | M4 · Understanding & Building RAGs | 8 |
| `m5-advanced-rag.md` | M5 · Advanced RAG Patterns + Evaluation | 7 |
| `m6-fine-tuning.md` | M6 · LLM Fine-Tuning | 24 |
| `m7-agentic-applications.md` | M7 · The Agent Loop, By Hand | 37 |

M7 companion files:

- `m7-concepts-reference.md`: dense text reference for the concepts covered in the M7 slides.
- `m7-code-cookbook.md`: runnable, section-by-section Python recipes that demonstrate each M7 concept path.

Note: M3, M4, and M5 reference snippet files (`snippets/m3/…` etc.) that
don't exist yet in the source repo — those code blocks contain a clearly marked
placeholder comment naming the missing file, so the gap is visible.

## Preview

- **VS Code**: install the "Marp for VS Code" extension, open any file, hit preview.
- **CLI**: no install needed with npx:

```bash
npx @marp-team/marp-cli m0-python.md          # → m0-python.html
npx @marp-team/marp-cli m0-python.md --pdf    # → m0-python.pdf
npx @marp-team/marp-cli -s .                  # live server for the whole folder
```

In the exported HTML, press `p` for presenter view to see the speaker notes.
