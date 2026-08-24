"""Lab test setup: force the template path for deterministic previews."""

import pytest

from tests.conftest import *  # noqa: F401,F403

from labs.m1_advisor_preview import call_preview_model as call_module
from labs.m1_advisor_preview import model_loading


@pytest.fixture(autouse=True)
def force_template_preview(monkeypatch):
    monkeypatch.setattr(model_loading, "load_offline_language_model", lambda: None)
    monkeypatch.setattr(call_module, "load_offline_language_model", lambda: None)
    yield
