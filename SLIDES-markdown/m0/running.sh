# Run a file.
uv run python m0/functions.py

# Run the tests.
uv run pytest -q

# Drop into a debugger at the line that matters.
# Add this where you want to stop, then run normally:
#   breakpoint()
#
#   (Pdb) p shares          inspect a value
#   (Pdb) n                 next line
#   (Pdb) c                 continue

# Or let the debugger catch the failure for you.
uv run python -m pdb -c continue m0/functions.py

# Serve the API with auto-reload on every save.
uv run uvicorn m0.api_server:api --reload
