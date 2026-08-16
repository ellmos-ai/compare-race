"""Run the race -- fan out one prompt, collect artefacts.

Two modes, one deliberate difference:

``sequential`` (the stopwatch)
    One lane at a time. Latency per model is *clean* -- no contention between
    processes on this machine. Slower overall, honest per-lane timing.

``parallel`` (the true race)
    All lanes at once via process handles. Faster overall; per-lane latency is
    still measured but shares the machine, so treat it as indicative.

The stopwatch is only a picture: time is ONE dimension. The verdict rubric
(quality, correctness, completeness, instruction fidelity, cost, latency) lives
in the judge template; the judge is the STARTING model by default.

Execution goes through COMA (spawn, file protocol, polling) -- one Spawner per
backend, because a Spawner holds one adapter. COMA is *detected, not assumed*:
without it, ``run`` explains itself and the starter can execute the calls
manually and drop the outputs next to the plan (the model-manual fallback).
"""

from __future__ import annotations

import time as _time
from dataclasses import dataclass, field
from pathlib import Path

from .config import ModelEntry, RaceSettings
from .tokens import RacePlan, RunIdentity, format_ts, plan_race, utcnow


@dataclass
class RunResult:
    identity: RunIdentity
    backend: str
    ok: bool
    output: str
    latency_s: float
    started_utc: str
    finished_utc: str
    error: str = ""
    #: clutch rate lookup, when the catalogue is present. est_ = derived from
    #: chars/4, an estimate by construction -- never a measurement.
    cost_gear: str = ""
    est_cost_usd: float | None = None
    #: Deterministic check results -- mechanical, reproducible from the
    #: artefacts, evaluated before any judge opinion exists.
    checks_passed: list[str] = None  # type: ignore[assignment]
    checks_failed: list[str] = None  # type: ignore[assignment]


@dataclass
class RaceResult:
    plan: RacePlan
    results: list[RunResult] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _coma_available() -> bool:
    try:
        import coma  # noqa: F401
        return True
    except ImportError:
        return False


def _entry_for(settings: RaceSettings, model_name: str) -> ModelEntry:
    for entry in settings.models:
        if entry.name == model_name:
            return entry
    raise KeyError(f"model {model_name!r} is not configured")


def _spawner(entry: ModelEntry):
    from coma import Spawner
    from coma.adapters import get_adapter

    kwargs = {"model": entry.model} if entry.model else {}
    adapter = get_adapter(entry.backend, **kwargs)
    # kimi is a scaffold adapter: COMA refuses it without the per-lane opt-in.
    return Spawner(adapter, allow_unverified=entry.allow_unverified)


def run_race(
    prompt: str,
    settings: RaceSettings,
    models: list[str] | None = None,
    mode: str | None = None,
    repeats: int | None = None,
    variants: dict[str, str] | None = None,
) -> RaceResult:
    """Execute the plan. Requires COMA; raises with a helpful message otherwise.

    ``variants`` maps variant name -> full prompt text (twin/clone mode). The
    TASK token comes from the base ``prompt``; each lane is executed with its
    variant's wording. Without variants every lane runs the base prompt.
    """
    names = models or settings.model_names()
    plan = plan_race(
        prompt,
        models=names,
        system=settings.system or "unknown",
        mode=mode or settings.mode,
        repeats=repeats or settings.repeats,
        variants=sorted(variants) if variants else None,
    )
    race = RaceResult(plan=plan)
    if not _coma_available():
        raise RuntimeError(
            "COMA is not importable -- install it (pip install -e <coma clone>) or run "
            "the race model-manually: execute each lane yourself and write the outputs "
            "with `compare-race record`."
        )

    def lane_prompt(identity: RunIdentity) -> str:
        if variants and identity.variant in variants:
            return variants[identity.variant]
        return prompt

    def execute() -> RaceResult:
        if plan.mode == "sequential":
            for identity in plan.runs:
                race.results.append(
                    _run_one(lane_prompt(identity), identity, settings))
        else:
            race.results.extend(_run_parallel_variants(plan, settings, lane_prompt))
        return race

    if settings.lane_workdir:
        # Naivety guard: spawned CLI lanes inherit our cwd; a project cwd leaks
        # hooks/rules/judge files into them (observed 2026-08-16). Run the
        # spawns from a neutral directory instead.
        import contextlib
        workdir = Path(settings.lane_workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        with contextlib.chdir(workdir):
            return execute()
    return execute()


def _run_one(prompt: str, identity: RunIdentity, settings: RaceSettings) -> RunResult:
    entry = _entry_for(settings, identity.model)
    started = utcnow()
    tick = _time.perf_counter()
    try:
        spawner = _spawner(entry)
        # COMA returns a plain dict (success/output/stderr/returncode/duration_s/
        # timed_out); timeout travels as a build_spec override.
        outcome = spawner.run(prompt, timeout=settings.timeout_seconds)
        ok = bool(outcome.get("success"))
        output = str(outcome.get("output", ""))
        error = str(outcome.get("stderr", "") or "")
        if outcome.get("timed_out"):
            ok = False
            error = f"timed out after {settings.timeout_seconds}s. {error}".strip()
    except Exception as exc:  # a crashing lane must not kill the race
        ok, output, error = False, "", f"{exc.__class__.__name__}: {exc}"
    latency = _time.perf_counter() - tick
    return RunResult(
        identity=identity,
        backend=entry.backend,
        ok=ok,
        output=output,
        latency_s=round(latency, 3),
        started_utc=format_ts(started),
        finished_utc=format_ts(utcnow()),
        error=error,
    )


def _run_parallel_variants(plan: RacePlan, settings: RaceSettings, lane_prompt) -> list[RunResult]:
    """All lanes at once, capped at max_parallel; each lane gets its variant."""
    from concurrent.futures import ThreadPoolExecutor

    cap = max(1, settings.max_parallel)
    with ThreadPoolExecutor(max_workers=cap) as pool:
        futures = [
            pool.submit(_run_one, lane_prompt(identity), identity, settings)
            for identity in plan.runs
        ]
        return [future.result() for future in futures]


# ---------------------------------------------------------------------------
# Artefacts -- one run, one file; header speaks the system-auditor parser
# ---------------------------------------------------------------------------

def run_front_matter(result: RunResult, plan: RacePlan) -> str:
    identity = result.identity
    lines = [
        "---",
        f"race_id: {plan.race_id}",
        f"time_token: {identity.time}",
        f"prompt_token: {identity.prompt}",
        f"system: {identity.system}",
        f"model: {identity.model}",
        f"run: {identity.run}",
        f"variant: {identity.variant}",
        f"backend: {result.backend}",
        f"mode: {plan.mode}",
        f"started_utc: {result.started_utc}",
        f"finished_utc: {result.finished_utc}",
        f"latency_s: {result.latency_s}",
        f"ok: {'true' if result.ok else 'false'}",
    ]
    if result.cost_gear:
        lines.append(f"cost_gear: {result.cost_gear}")
        lines.append(f"est_cost_usd: {result.est_cost_usd}")
    if result.checks_passed is not None or result.checks_failed is not None:
        lines.append(f"checks_passed: [{', '.join(result.checks_passed or [])}]")
        lines.append(f"checks_failed: [{', '.join(result.checks_failed or [])}]")
    lines.append("---")
    return "\n".join(lines) + "\n"


def annotate_costs(
    race: RaceResult,
    prompt: str,
    getriebe_path: str = "",
    settings: RaceSettings | None = None,
) -> None:
    """Attach clutch cost rates + char-based estimates to each lane, in place.

    Silent no-op when the catalogue is absent (clutch is a neighbour, detected
    not assumed) or a lane's model is unknown to it.

    The lane's configured **model id** is looked up first: the lane name is an
    identity token ("opus-5") and the backend is a family ("claude") -- the
    big race of 2026-08-16 mapped the opus lane to the first claude gear
    (claude-fable) via the backend fallback, a wrong rate with the right sign.
    """
    from .costs import load_rates, rate_for

    rates = load_rates(getriebe_path or None)
    if not rates:
        return
    model_ids = {
        entry.name: entry.model for entry in (settings.models if settings else [])
    }
    for result in race.results:
        lane = result.identity.model
        rate = rate_for(rates, model_ids.get(lane, ""), lane, result.backend)
        if rate is None:
            continue
        result.cost_gear = rate.gear
        result.est_cost_usd = rate.estimate_usd(len(prompt), len(result.output))


def evaluate_checks(race: RaceResult, checks: list[dict]) -> None:
    """Deterministic format checks, in place -- the mechanical tier of the
    evaluation ladder (deterministic > evidenced > subjective). A check passes
    when its regex matches the lane output; anyone can re-run this from the
    artefacts and get the same result. Failed lanes fail every check.
    """
    import re

    if not checks:
        return
    for result in race.results:
        passed, failed = [], []
        for check in checks:
            name = str(check.get("name"))
            try:
                hit = result.ok and re.search(str(check.get("regex")), result.output,
                                              re.MULTILINE) is not None
            except re.error:
                failed.append(f"{name}(regex-invalid)")
                continue
            (passed if hit else failed).append(name)
        result.checks_passed, result.checks_failed = passed, failed


def write_artifacts(race: RaceResult, races_dir: str | Path, prompt: str) -> Path:
    """Write RUN files plus PROMPT.md; returns the race directory."""
    base = Path(races_dir) / race.plan.race_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "PROMPT.md").write_text(prompt.rstrip() + "\n", encoding="utf-8")
    for result in race.results:
        body = result.output if result.ok else f"(lane failed)\n\n{result.error}"
        target = base / result.identity.filename()
        target.write_text(
            run_front_matter(result, race.plan) + "\n" + body.rstrip() + "\n",
            encoding="utf-8",
        )
    return base


__all__ = [
    "RaceResult", "RunResult", "annotate_costs",
    "run_front_matter", "run_race", "write_artifacts",
]
