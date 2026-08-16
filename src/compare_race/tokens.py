"""Race identity -- six axes, one statement.

Reuses the system-auditor identity logic (the module this grew out of): an
artefact is one statement, addressed by the axes that produced it. A race run
carries **five**:

``time``    when the race started (event stamp, not a period window -- races are
            events; series over races of the same prompt compare events)
``prompt``  which prompt (slug + short hash: two different prompts with the same
            first words must not collide)
``system``  which machine ran it
``model``   which model answered (the varied axis of the race)
``run``     which repetition (the varied axis of a stability check)
``variant`` HOW the task is presented: wording, role, handed-over skills,
            environment (the varied axis of twin/clone mode)

The identifiability rule transfers verbatim from system-auditor: a difference
may only be *attributed* when exactly one axis varies. Models vary -> the race
(quality/latency per model). Runs vary -> variance of one model. Time varies ->
drift of one model across versions. More than one at once -> describe, don't
conclude.

Latency is measured, but the stopwatch is only one picture: time is ONE
dimension of the verdict, beside quality, correctness, completeness and cost.
The judge template carries the full rubric.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone

from system_auditor.tokens import format_ts  # reused, not re-invented


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def race_time_token(moment: datetime | None = None) -> str:
    """Event stamp, filename-safe, second precision."""
    return (moment or utcnow()).strftime("%Y%m%d-%H%M%S")


def _slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii").lower()
    keep = [c if (c.isalnum() or c in "-_") else "-" for c in ascii_only]
    slug = re.sub("-+", "-", "".join(keep)).strip("-")
    return slug or "x"


def prompt_token(prompt: str, words: int = 4) -> str:
    """Slug of the first words plus a short content hash.

    The slug keeps the artefact human-findable; the hash keeps two prompts with
    the same opening words apart. The hash covers the *exact* text -- a changed
    comma is a different prompt and must be a different token, or a series
    would compare answers to different questions.
    """
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
    head = "-".join(prompt.split()[:words]) or "empty"
    return f"{_slug(head)}-{digest}"


@dataclass(frozen=True)
class RunIdentity:
    """One run = one statement -- six axes.

    ``prompt`` is the TASK token (what is to be solved -- the racetrack).
    ``variant`` names HOW it is presented: prompt wording, role, handed-over
    skills, harness environment. Twin/clone mode holds model and task fixed and
    varies ONLY the variant -- that makes the influence of prompt and
    environment attributable (the identifiability rule, sixth axis).
    """

    time: str
    prompt: str
    system: str
    model: str
    run: int = 1
    variant: str = "base"

    def filename(self) -> str:
        middle = "" if self.variant == "base" else f"-v-{_slug(self.variant)}"
        return f"RUN-{_slug(self.model)}{middle}-r{self.run}.md"


@dataclass
class RacePlan:
    """The cross product models x variants x repeats, plus shared identity."""

    time: str
    prompt_token: str
    system: str
    mode: str  # "sequential" (stopwatch) | "parallel" (true race)
    runs: list[RunIdentity] = field(default_factory=list)
    #: True when model AND variant vary at once -- results are descriptive,
    #: a difference cannot be attributed to one cause.
    uncontrolled: bool = False

    @property
    def race_id(self) -> str:
        return f"{self.time}--{self.prompt_token}"


def plan_race(
    prompt: str,
    models: list[str],
    system: str,
    mode: str = "sequential",
    repeats: int = 1,
    moment: datetime | None = None,
    variants: list[str] | None = None,
) -> RacePlan:
    """Cross product models x variants x repeats.

    Axis discipline: race mode varies models (variants stays [\"base\"]);
    twin/clone mode varies variants over ONE model. Varying both at once is
    legal but demoted to description -- the plan records it in ``uncontrolled``
    so no one attributes a difference to a single cause by accident.
    """
    if mode not in ("sequential", "parallel"):
        raise ValueError(f"mode must be sequential or parallel, got {mode!r}")
    if repeats < 1:
        raise ValueError("repeats must be >= 1")
    if not models:
        raise ValueError("a race needs at least one model")
    names = variants or ["base"]
    if len(set(names)) != len(names):
        raise ValueError("variant names must be unique")
    stamp = race_time_token(moment)
    token = prompt_token(prompt)
    runs = [
        RunIdentity(time=stamp, prompt=token, system=system, model=model,
                    run=index, variant=variant)
        for model in models
        for variant in names
        for index in range(1, repeats + 1)
    ]
    plan = RacePlan(time=stamp, prompt_token=token, system=system, mode=mode, runs=runs)
    plan.uncontrolled = len(models) > 1 and len(names) > 1
    return plan


__all__ = [
    "RacePlan",
    "RunIdentity",
    "format_ts",
    "plan_race",
    "prompt_token",
    "race_time_token",
    "utcnow",
]
