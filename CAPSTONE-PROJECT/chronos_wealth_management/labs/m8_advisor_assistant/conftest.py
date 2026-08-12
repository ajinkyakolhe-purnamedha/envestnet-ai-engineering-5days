"""Lab test setup: reuse the app's fixtures, force the template path.

Importing * from tests.conftest brings the isolated database, seeded
demo users, and fixture prices. The autouse fixture pins every lab test
to the deterministic template note whether or not the ``agents`` extra
is installed.
"""

import pytest

from tests.conftest import *  # noqa: F401,F403

from labs.m8_advisor_assistant import draft_advisor_note as draft_module
from labs.m8_advisor_assistant import model_loading


@pytest.fixture(autouse=True)
def force_template_notes(monkeypatch):
    # Patch both the source and the name imported into the draft module.
    monkeypatch.setattr(
        model_loading, "load_offline_language_model", lambda: None
    )
    monkeypatch.setattr(
        draft_module, "load_offline_language_model", lambda: None
    )
    yield
