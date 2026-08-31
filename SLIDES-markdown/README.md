# Workshop decks (Marp)

Every deck is a standalone [Marp](https://marp.app) markdown file:
frontmatter `marp: true`, slides split by `---`, a lead title slide, and the
full spoken narrative as an HTML comment at the end of each slide — Marp
shows those in presenter view and can print them in a notes PDF. A
slides-only export is close to unreadable by design; the notes carry the
teaching.

| File | Module |
|---|---|
| `m0-python.md` | M0 · Python foundations |
| `m1-intro-to-ai-models.md` | M1 · Introduction to AI models |
| `m2-model-tokens-context.md` | M2 · Model, tokens & context |
| `m3-application-patterns.md` | M3 · LLM application patterns |
| `m4-building-rags.md` | M4 · Building a complete baseline RAG |
| `m5-advanced-rag.md` | M5 · Advanced RAG improvements & evaluation |
| `m6-fine-tuning.md` | M6 · LLM fine-tuning |
| `m7-agentic-applications.md` | M7 · The agent loop, by hand |
| `m8-agentic-frameworks.md` | M8 · Agentic frameworks & orchestration |
| `m9-memory-verification-hitl.md` | M9 · Memory, verification & human-in-the-loop |
| `m10-mcp-fundamentals.md` | M10 · MCP fundamentals |

The code a deck quotes lives in `../CODEALONGS/` — one folder per module,
each with its own README of ordered snippets. Code fences in the decks carry
a `Source:` pointer to the real file there; the code is the source of truth.
`data/` holds the small `prices.csv` and `investment_policy.md` some
snippets read.

Around a deck you may also find `mN-lab-instructions.md` (participant lab
steps — **the m7–m9 ones are currently marked OUTDATED**; reworked labs are
coming later) and gitignored `mN-instructor-notes.md`. M7 additionally has
`m7-concepts-reference.md` (dense text version of the deck).

## Preview and export

- **VS Code**: install the "Marp for VS Code" extension, open any file, hit
  preview.
- **CLI** (no install needed):

```bash
npx @marp-team/marp-cli m0-python.md          # → m0-python.html
npx @marp-team/marp-cli m0-python.md --pdf    # → m0-python.pdf
npx @marp-team/marp-cli -s .                  # live server for the whole folder
```

In the exported HTML, press `p` for presenter view to see the speaker notes.
