# Chronos Wealth — Module 0

A working Python wealth-management simulator for the 5-day Enterprise AI and
GenAI training. Virtual money, synthetic time, real historical prices.
Educational software only — no real trades, no financial advice, and no LLM
key required.

```text
Investor side = deterministic finance app
Advisor side = deterministic, read-only client workspace
Python calculates. AI explains, retrieves, reasons, and assists.
```

Later course labs add those AI capabilities through Chronos's deterministic
data and policy boundaries; the baseline application does not simulate them.

## Stack

Python 3.13 · uv · FastAPI · Pydantic v2 · SQLAlchemy · SQLite · Pandas ·
yfinance · Streamlit · pytest

## Setup

```bash
uv sync
uv run python -m scripts.load_market_data   # yfinance -> CSV -> SQLite (one-time, needs network)
```

For the optional M12 Governed MCP extension, install its local MCP dependency:

```bash
uv sync --extra m12
```

The load script downloads AAPL, MSFT, SPY, GLD, JPM daily prices
(2020-01-01 to 2021-12-31) into `data/market/prices.csv` and the SQLite
`prices` table. The app never calls yfinance at runtime; if the database is
empty it loads the CSV, and if the CSV is missing it tells you to run the
script.

## Run

```bash
uv run uvicorn chronos.main:app --reload    # API at http://127.0.0.1:8000
uv run streamlit run ui/app.py              # UI  at http://localhost:8501
```

Demo logins (no passwords):

```text
Alice Investor   alice@example.com    INVESTOR
Demo Advisor     advisor@example.com  ADVISOR
```

Alice starts with $100,000 virtual cash at simulated date 2020-06-01. Demo
Advisor can review Alice's portfolio through a read-only workspace.
Reset everything back to that state with:

```bash
uv run python -m scripts.reset_demo_data    # or POST /demo/reset
```

## Test

```bash
uv run pytest
```

Tests use `tests/fixtures/prices_sample.csv` and never call yfinance or the
network.

## Layout

```text
chronos/    lean top-level application modules + FastAPI route modules
  application_database.py                       database tables and sessions
  demo_users_and_startup_data.py                Alice + Demo Advisor startup data
  market_data_loading_and_price_queries.py      historical prices
  investor_accounts_portfolios_and_history.py   portfolios and simulated time
  investor_trade_execution_and_preview.py       trade preview and execution
  advisor_client_lists.py                        advisor client summaries
  api_routes_{system,investor,advisor}.py       HTTP boundary by audience
ui/         Streamlit screens; ui/api_client.py is the only HTTP client
labs/       opt-in M1–M15 AI lab starters; M12 includes a local MCP starter
scripts/    load_market_data (yfinance one-time), reset_demo_data
tests/      pytest suite + offline price fixture
data/       chronos.db + market/prices.csv (generated, not committed)
```

Key rule everywhere: every price lookup uses the latest price on or before
the account's simulated date — no feature can see the future.

The live demo intentionally has two personas only: Alice Investor and Demo
Advisor. The advisor can view Alice's portfolio but cannot trade for her.
