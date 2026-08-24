"""YOU implement: call the offline model boundary (M1)."""

from labs.m1_advisor_preview.model_loading import load_offline_language_model


def call_preview_model(messages: list[dict[str, str]]) -> str | None:
    """Return model text, or None when no offline model is available.

    Hints:
    - generator = load_offline_language_model()
    - return None immediately when generator is None
    - flatten messages into one prompt string for the pipeline
    - strip the generated text before returning
    """
    raise NotImplementedError("M1 lab step 2: call the preview model boundary")
