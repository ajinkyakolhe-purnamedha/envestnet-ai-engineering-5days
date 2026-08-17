# M0.3 · Wealth Demo

One synthetic AAPL holding grows from variables into a small local application.
No API key or third-party package is required.

Run a snippet from the repository root:

```bash
uv run --project CODEALONGS python CODEALONGS/day_1/m0_section_3_wealth_demo/03_functions.py
```

Run the complete test suite:

```bash
cd CODEALONGS/day_1/m0_section_3_wealth_demo
uv run python -m unittest wealth_demo.test_wealth_demo -v
```

Run the local server, then in another terminal call `curl http://localhost:8000/health`
or `curl http://localhost:8000/portfolio`:

```bash
cd CODEALONGS/day_1/m0_section_3_wealth_demo
uv run uvicorn wealth_demo.server:app --reload
```

The code-alongs follow this order: values and hints, functions, classes,
SQLite storage, a local server, then logging, testing, and debugging.
