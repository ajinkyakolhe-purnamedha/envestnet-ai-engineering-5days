import streamlit as st

from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[11]


def run(user: dict, request: str) -> None:
    raise NotImplementedError(
        "M12 starter: implement host admission in labs/m12_governed_mcp/"
        "host_admission.py, then authorization, result validation, and audit "
        "in server.py."
    )


def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
    st.subheader("Self-contained MCP starter")
    st.code("uv sync --extra m12\nuv run --extra m12 python -m labs.m12_governed_mcp.client")
    st.write(
        "The real local MCP server and client are in "
        "`labs/m12_governed_mcp/`. Complete host admission, authorization, "
        "result-limit, and audit TODOs; the starter never invents a portfolio response."
    )
