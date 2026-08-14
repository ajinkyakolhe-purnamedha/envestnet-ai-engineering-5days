"""Evals that run in pytest, with no API key.

Run:
    uv run --project ../CODE-ALONGS \
        python -m pytest m3/test_evals.py -v
"""

import json

from eval_answers import POLICY, groundedness

REPLY = '{"symbol": "AAPL", "allocation_pct": 36.0}'


# #region tests
def test_output_parses_as_json():
    assert json.loads(REPLY)


def test_output_matches_schema():
    parsed = json.loads(REPLY)
    assert set(parsed) == {"symbol", "allocation_pct"}
    assert isinstance(parsed["allocation_pct"], float)


def test_threshold_comes_from_policy_not_the_model():
    assert "35" in POLICY


def test_grounded_answer_scores_high():
    answer = "Holdings are limited to 35% of the portfolio."
    assert groundedness(answer, POLICY) >= 0.70
# #endregion tests


def test_grounded_beats_ungrounded():
    good = groundedness("Holdings cap at 35%.", POLICY)
    bad = groundedness("Gold hedges inflation.", POLICY)
    assert good > bad


def test_metric_cannot_detect_a_plausible_lie():
    lie = groundedness("The limit is 60%.", POLICY)
    assert lie > 0.40

# Deterministic tests are exact, instant, and free.
# Statistical checks are useful but limited. The last
# test documents the limit so nobody treats one metric
# as a release gate by itself.
