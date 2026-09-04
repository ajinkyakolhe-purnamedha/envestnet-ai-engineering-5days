"""Shared, honest Streamlit presentation for incomplete lab starters."""

from collections.abc import Callable

import streamlit as st

from labs.registry import LabDefinition


def render_starter_page(
    lab: LabDefinition, user: dict, run: Callable[[dict, str], None]
) -> None:
    st.title(f"M{lab.module_number} Lab — {lab.title}")
    st.caption(lab.outcome)
    st.info(
        "This is a starter page. It has no simulated AI response: complete the "
        "lab's run() function to connect the real model, retrieval, tool, or "
        "evaluation behavior."
    )
    request = st.text_area(
        lab.input_label,
        placeholder=lab.input_placeholder,
        key=f"{lab.lab_id}_input",
    )
    if st.button("Run lab starter", key=f"{lab.lab_id}_run"):
        try:
            run(user, request)
        except NotImplementedError as error:
            st.warning(str(error))

    st.subheader("Student implementation target")
    st.write(lab.implementation_prompt)
    st.caption(
        "Chronos supplies facts, calculations, permissions, and consequential "
        "actions. Student AI code may only explain, retrieve, classify, draft, "
        "or assist within those boundaries."
    )
