"""GIVEN: the same offline SmolLM2 loader the M8 lab used.

Re-exported so this package never imports transformers directly and the
template fallback rules stay identical to yesterday's.
"""

from labs.m8_advisor_assistant.model_loading import (  # noqa: F401
    find_offline_model_path,
    load_offline_language_model,
)
