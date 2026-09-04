from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[5]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M6 starter: run an adapter or baseline classifier and report held-out evidence.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
