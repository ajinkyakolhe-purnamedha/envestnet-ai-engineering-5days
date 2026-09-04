from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[8]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M9 starter: add memory, verification, durable state, and human approval.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
