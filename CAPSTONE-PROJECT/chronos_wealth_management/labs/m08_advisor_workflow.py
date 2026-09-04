from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[7]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M8 starter: run the bounded advisor flow through a framework with its trace visible.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
