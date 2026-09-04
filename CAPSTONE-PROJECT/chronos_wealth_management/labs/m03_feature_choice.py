from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[2]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M3 starter: record a feature-choice card; do not add a runtime yet.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
