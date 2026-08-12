"""YOU implement: the draft (chaining pattern step 3, M8.2.2).

Prose is the model's ONLY job. Facts and verdict arrive pre-computed;
nothing here calculates. When no model is installed, a deterministic
template note keeps the feature working — no key, no network, no model.
"""

from chronos.shared_database.api_schemas import AdvisorMetricResponse

from labs.m8_advisor_assistant.model_loading import (
    load_offline_language_model,
)

LANGUAGE_MODEL_SOURCE = "language_model"
TEMPLATE_SOURCE = "template"


def draft_advisor_note(
    question: str,
    metrics: AdvisorMetricResponse,
    verdict: str,
    recommendations: list[str],
    revision_problems: list[str] | None = None,
) -> tuple[str, str]:
    """Return (note, note_source).

    Hints:
    - generator = load_offline_language_model(); None means: build a
      template note from the metrics + verdict + recommendations and
      return it with TEMPLATE_SOURCE (include the verdict text — it
      already cites any breached threshold)
    - with a generator: prompt with the facts and the verdict marked as
      ALREADY DECIDED, ask for a two-sentence note; append
      revision_problems to the prompt when given
    - pipeline call shape:
        out = generator([{"role": "user", "content": prompt}],
                        max_new_tokens=120)
        note = out[0]["generated_text"][-1]["content"].strip()
    """
    raise NotImplementedError("M8 lab step 4: write the draft step")
