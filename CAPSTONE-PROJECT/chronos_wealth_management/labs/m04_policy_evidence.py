from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[3]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M4 starter: retrieve real policy evidence and show citations or not found.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
