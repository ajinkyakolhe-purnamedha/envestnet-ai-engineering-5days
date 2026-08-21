"""M3 Pattern 2 teaches structured output, not unvalidated JSON parsing."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT.parent / "SLIDES-markdown" / "m3-application-patterns.md"
SOURCE = ROOT / "day_1" / "m3_application_patterns" / "03_prompted_extraction.py"


def test_m3_pattern_2_uses_instructor_and_separates_validation_layers() -> None:
    deck = DECK.read_text()
    source = SOURCE.read_text()

    assert "Structured Output" in deck
    assert "Schema validation is not business validation" in deck
    assert "import instructor" in source
    assert "response_model=TradeIntent" in source
    assert "validate_trade_intent" in source
