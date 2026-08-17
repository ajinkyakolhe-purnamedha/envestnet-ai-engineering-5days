# Python Courseware

Cookbooks are syntax flash cards: each tiny Python file demonstrates one visible operation and can be run independently. Read them in filename order inside each folder.

Code-alongs combine those features into one small capability. Open the notebooks in order and run each from top to bottom.

## Cookbook order

1. `cookbooks/01_python_syntax/`
2. `cookbooks/02_data_validation_and_web/`
3. `cookbooks/03_python_for_ai/`

## Code-along order

1. `01_python_portfolio.ipynb`
2. `02_validation_errors_and_tests.ipynb`
3. `03_historical_data_with_pandas.ipynb`
4. `04_database_and_fastapi.ipynb`
5. `05_llm_application_in_python.ipynb`
6. `06_rag_as_a_python_pipeline.ipynb`
7. `07_agents_as_python_control_flow.ipynb`
8. `07b_m7_manual_agent_loop.ipynb` - competing M7 notebook aligned to "The Agent Loop, By Hand"
9. `07c_m7_code_cookbook.ipynb` - notebook conversion of the M7 runnable code cookbook

## Install and run

From the `CODEALONGS/` folder:

```bash
uv sync --extra courseware
uv run python cookbooks/01_python_syntax/06_basic_f_strings.py
uv run jupyter lab
```

The notebooks and cookbooks use paths relative to the `CODEALONGS/` folder, so run everything from there.

## Optional model call

The model examples run with a labelled offline response when configuration is absent. To enable an OpenAI-compatible endpoint, set:

```bash
export MODEL_ENDPOINT="https://your-endpoint/v1"
export MODEL_API_KEY="your-key"
export MODEL_NAME="your-model"
```

Set `COURSEWARE_OFFLINE=1` to skip all external calls. The LlamaIndex section also skips when its optional package is unavailable; install `llama-index-core` separately if you want to run that final comparison.

All prices, portfolios, and policies in this package are deterministic synthetic educational data. These materials do not provide financial advice.
