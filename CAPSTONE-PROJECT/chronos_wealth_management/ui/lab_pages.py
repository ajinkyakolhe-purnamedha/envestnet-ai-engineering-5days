"""Sidebar routing for explicit optional Chronos lab pages."""

import importlib

import streamlit as st

from labs.registry import LabDefinition, visible_labs_for_role


def select_lab_page(user: dict) -> LabDefinition | None:
    labs = visible_labs_for_role(user["role"])
    options = {"Dashboard": None, **{f"M{lab.module_number}: {lab.title}": lab for lab in labs}}
    selected_label = st.selectbox("Workspace", options, key="chronos_workspace")
    return options[selected_label]


def render_lab_page(lab: LabDefinition, user: dict) -> None:
    starter = importlib.import_module(lab.starter_module)
    starter.render(user)
