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
    return Spawner(adapter)


def run_race(
    prompt: str,
    settings: RaceSettings,
    models: list[str] | None = None,
    mode: str | None = None,
    repeats: int | None = None,
) -> RaceResult:
    """Execute the plan. Requires COMA; raises with a helpful message otherwise."""
    names = models or settings.model_names()
    plan = plan_race(
        prompt,
        models=names,
        system=settings.system or "unknown",
        mode=mode or settings.mode,
        repeats=repeats or settings.repeats,
    )
    race = RaceResult(plan=plan)
    if not _coma_available():
        raise RuntimeError(
            "COMA is not importable -- install it (pip install -e <coma clone>) or run "
            "the race model-manually: execute each lane yourself and write the outputs "
            "with `compare-race record`."
        )

    if plan.mode == "sequential":
        for identity in plan.runs:
            race.results.append(_run_one(prompt, identity, settings))
    else:
        race.results.extend(_run_parallel(prompt, plan, settings))
    return race


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


def _run_parallel(prompt: str, plan: RacePlan, settings: RaceSettings) -> list[RunResult]:
    """All lanes at once via COMA process handles, capped at max_parallel."""
    from concurrent.futures import ThreadPoolExecutor

    cap = max(1, settings.max_parallel)
    with ThreadPoolExecutor(max_workers=cap) as pool:
        futures = [
            pool.submit(_run_one, prompt, identity, settings) for identity in plan.runs
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
        f"backend: {result.backend}",
        f"mode: {plan.mode}",
        f"started_utc: {result.started_utc}",
        f"finished_utc: {result.finished_utc}",
        f"latency_s: {result.latency_s}",
        f"ok: {'true' if result.ok else 'false'}",
        "---",
    ]
    return "\n".join(lines) + "\n"


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


__all__ = ["RaceResult", "RunResult", "run_front_matter", "run_race", "write_artifacts"]
