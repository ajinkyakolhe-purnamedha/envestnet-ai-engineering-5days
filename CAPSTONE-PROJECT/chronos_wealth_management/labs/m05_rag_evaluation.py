from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[4]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M5 starter: run the evidence evaluation and compare a measured retrieval change.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
