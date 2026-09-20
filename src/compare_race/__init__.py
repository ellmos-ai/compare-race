"""compare-race -- same prompt, several models; the starter judges.

Reuses the system-auditor identity discipline (six axes: time, prompt, system,
model, run, variant; attribute only when one axis varies) and COMA for execution. The
stopwatch (sequential mode) is only one picture: time is one dimension of the
verdict, beside quality, correctness, completeness and cost -- the judge is the
starting model by default (user decision 2026-08-16).
"""

__version__ = "0.7.2"

from .config import JUDGE_STARTER, ModelEntry, RaceSettings, load  # noqa: F401
from .judge import (  # noqa: F401
    JudgeReadiness,
    JudgeVerdict,
    assess_judgeability,
    build_judge_prompt,
    judge_race,
    write_judge_artifact,
)
from .race import RaceResult, RunResult, run_race, write_artifacts  # noqa: F401
from .report import mechanical_tally, read_race_dir, scaffold, write_scaffold  # noqa: F401
from .tokens import RacePlan, RunIdentity, plan_race, prompt_token  # noqa: F401
