from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[9]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M10 starter: make one real read-only MCP client/server call and print its trace.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
