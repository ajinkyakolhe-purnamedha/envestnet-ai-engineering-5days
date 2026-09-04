from labs.registry import LABS
from labs.starter_page import render_starter_page

LAB = LABS[1]
def run(user: dict, request: str) -> None:
    raise NotImplementedError("M2 starter: assemble bounded history and measure the real model request.")
def render(user: dict) -> None:
    render_starter_page(LAB, user, run)
