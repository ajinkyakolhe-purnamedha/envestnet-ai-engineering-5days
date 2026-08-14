# python: run it, it exits, state is gone.
uv run python m0/data_csv.py

# ipython: the same interpreter, but it stays open.
# Tab-completion, ?help, and your variables survive.
uv add ipython
uv run ipython

# jupyter: ipython with the transcript written down.
# Cells run in any order -- which is the feature AND
# the bug. Restart-and-run-all before you trust it.
uv add jupyterlab
uv run jupyter lab

# Java/C: compile, run, read the output, edit, repeat.
# Python: keep the session, poke the data, learn, keep
# the line that worked. That loop is why analysts and
# engineers ended up in the same language.
