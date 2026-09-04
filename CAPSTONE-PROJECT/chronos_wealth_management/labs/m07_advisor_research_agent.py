from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[6]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M7 starter: implement a bounded, traced loop over allowlisted read-only tools.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
