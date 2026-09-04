from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[0]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M1 starter: call a local model with Python-supplied portfolio facts.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
