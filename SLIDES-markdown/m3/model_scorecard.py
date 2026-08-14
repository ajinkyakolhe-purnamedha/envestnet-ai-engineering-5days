"""One scorecard for comparing model sizes.

No model download required; this records the experiment shape. Run:
    uv run --project ../CODE-ALONGS \
        python m3/model_scorecard.py
"""

from dataclasses import dataclass


@dataclass
class ModelRun:
    model: str
    knowledge: int
    arithmetic: int
    honesty: int
    summary: int
    seconds: float


# #region score
def total_score(run: ModelRun) -> int:
    return run.knowledge + run.arithmetic + run.honesty + run.summary


def report(run: ModelRun) -> str:
    return (f"{run.model:>8} score={total_score(run):02d}/20 "
            f"time={run.seconds:>4.1f}s")
# #endregion score


RUNS = [
    ModelRun("0.1B", 1, 1, 1, 2, 1.4),
    ModelRun("1B", 2, 2, 2, 3, 4.8),
    ModelRun("5B", 3, 3, 3, 4, 18.2),
    ModelRun("10B", 4, 4, 4, 4, 41.0),
]

if __name__ == "__main__":
    for run in RUNS:
        print(report(run))

# Same prompts, one variable changed. The scorecard is
# not a benchmark; it is a habit. If the larger model is
# slower, write down what quality it actually bought.
