"""Every planned AI module has an importable, explicit Chronos lab starter."""

import importlib

import pytest

from labs.registry import LABS, visible_labs_for_role


def test_all_m1_to_m15_lab_starters_are_registered():
    assert [lab.module_number for lab in LABS] == list(range(1, 16))

    for lab in LABS:
        starter = importlib.import_module(lab.starter_module)
        assert callable(starter.render)
        assert callable(starter.run)
        with pytest.raises(NotImplementedError):
            starter.run({"role": lab.roles[0]}, "starter input")


def test_each_demo_role_sees_relevant_lab_pages():
    assert any(lab.module_number == 1 for lab in visible_labs_for_role("INVESTOR"))
    assert any(lab.module_number == 7 for lab in visible_labs_for_role("ADVISOR"))
