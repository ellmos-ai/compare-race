"""CLI -- one call per protocol step, thin over the library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import load as load_config
from .race import RaceResult, RunResult, annotate_costs, run_race, write_artifacts
from .report import read_race_dir, write_scaffold
from .tokens import RunIdentity, format_ts, plan_race, utcnow


def _settings(args):
    settings = load_config(getattr(args, "config", None))
    for note in settings.notes:
        print(f"config: {note}", file=sys.stderr)
    return settings


def _read_prompt(args) -> str:
    if getattr(args, "prompt_file", None):
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if getattr(args, "prompt", None):
        return args.prompt
    print("ERROR: give --prompt or --prompt-file", file=sys.stderr)
    raise SystemExit(1)


def cmd_config(args) -> int:
    s = _settings(args)
    print(json.dumps({
        "source": s.source, "system": s.system, "races_dir": s.races_dir,
        "mode": s.mode, "repeats": s.repeats, "judge": s.judge,
        "models": [f"{m.name} ({m.backend}{':' + m.model if m.model else ''})" for m in s.models],
        "notes": s.notes,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_plan(args) -> int:
    s = _settings(args)
    prompt = _read_prompt(args)
    plan = plan_race(prompt, models=args.models.split(",") if args.models else s.model_names(),
                     system=s.system or "unknown", mode=args.mode or s.mode,
                     repeats=args.repeats or s.repeats)
    print(json.dumps({
        "race_id": plan.race_id, "mode": plan.mode,
        "lanes": [f"{r.model} r{r.run} -> {r.filename()}" for r in plan.runs],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args) -> int:
    s = _settings(args)
    if not s.races_dir:
        print("ERROR: races_dir is not configured", file=sys.stderr)
        return 1
    prompt = _read_prompt(args)
    race = run_race(prompt, s,
                    models=args.models.split(",") if args.models else None,
                    mode=args.mode or None, repeats=args.repeats or None)
    annotate_costs(race, prompt, s.getriebe_path, settings=s)
    base = write_artifacts(race, s.races_dir, prompt)
    target = write_scaffold(race, s.races_dir, prompt)
    failed = [r for r in race.results if not r.ok]
    print(f"race: {race.plan.race_id}\nartefacts: {base}\nscaffold: {target}\n"
          f"lanes: {len(race.results)} ok: {len(race.results) - len(failed)} failed: {len(failed)}")
    print("next: the STARTING model fills the judge rubric in RACE.md")
    return 0 if not failed else 2


def cmd_record(args) -> int:
    """Model-manual fallback: file one lane's output without COMA."""
    s = _settings(args)
    if not s.races_dir:
        print("ERROR: races_dir is not configured", file=sys.stderr)
        return 1
    prompt = _read_prompt(args)
    plan = plan_race(prompt, models=[args.model], system=s.system or "unknown",
                     mode="sequential", repeats=1)
    if args.race_id:  # join an existing race instead of opening a new one
        plan.time, plan.prompt_token = args.race_id.split("--", 1)
    identity = RunIdentity(time=plan.time, prompt=plan.prompt_token,
                           system=s.system or "unknown", model=args.model, run=args.run)
    output = Path(args.output_file).read_text(encoding="utf-8")
    result = RunResult(identity=identity, backend=args.backend or "manual", ok=True,
                       output=output, latency_s=args.latency or 0.0,
                       started_utc=format_ts(utcnow()), finished_utc=format_ts(utcnow()))
    race = RaceResult(plan=plan, results=[result])
    base = write_artifacts(race, s.races_dir, prompt)
    print(f"recorded: {base / identity.filename()}")
    return 0


def cmd_report(args) -> int:
    runs = read_race_dir(args.race_dir)
    print(json.dumps({
        "runs": len(runs),
        "lanes": [f"{r.get('model')} r{r.get('run')} ok={r.get('ok')} "
                  f"latency={r.get('latency_s')}s" for r in runs],
    }, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="compare-race",
        description="Same prompt, several models -- stopwatch or true race; "
        "the starting model judges (time is only one dimension).",
    )
    parser.add_argument("--version", action="version", version=f"compare-race {__version__}")
    parser.add_argument("--config", default=None, help="path to compare-race.config.json")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("config", help="show the resolved configuration")
    p.set_defaults(func=cmd_config)

    for name, func in (("plan", cmd_plan), ("run", cmd_run)):
        p = sub.add_parser(name, help=f"{name} a race")
        p.add_argument("--prompt", default=None)
        p.add_argument("--prompt-file", default=None)
        p.add_argument("--models", default=None, help="comma list; default: config lanes")
        p.add_argument("--mode", default=None, choices=["sequential", "parallel"])
        p.add_argument("--repeats", type=int, default=None)
        p.set_defaults(func=func)

    p = sub.add_parser("record", help="file one lane's output model-manually (no COMA)")
    p.add_argument("--prompt", default=None)
    p.add_argument("--prompt-file", default=None)
    p.add_argument("--model", required=True)
    p.add_argument("--backend", default=None)
    p.add_argument("--run", type=int, default=1)
    p.add_argument("--race-id", default=None, help="join an existing race")
    p.add_argument("--latency", type=float, default=None)
    p.add_argument("--output-file", required=True)
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("report", help="list the runs of a race directory")
    p.add_argument("--race-dir", required=True)
    p.set_defaults(func=cmd_report)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
