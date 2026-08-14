# One tool: creates the project, pins Python,
# manages every dependency.
uv init chronos
cd chronos

# Pin the interpreter. The whole team now runs
# the identical Python.
uv python pin 3.13

# Add libraries. Resolves + installs in milliseconds.
uv add pandas polars matplotlib
uv add fastapi uvicorn pydantic sqlalchemy
uv add transformers torch onnxruntime

# Run inside the project env. No "activate" step.
uv run python app.py
uv run uvicorn app:api --reload
