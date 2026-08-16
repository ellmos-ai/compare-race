"""CLI -- one call per protocol step, thin over the library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import load as load_config
from .race import (
    RaceResult,
    RunResult,
    annotate_costs,
    evaluate_checks,
    run_race,
    write_artifacts,
)
from .report import read_race_dir, write_scaffold
from .report import write_scaffold as _ws  # noqa: F401 (re-export guard)
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


def _load_variants(args) -> dict[str, str] | None:
    """variants-file: JSON {name: prompt-text | {file: path}}."""
    raw_path = getattr(args, "variants_file", None)
    if not raw_path:
        return None
    raw = json.loads(Path(raw_path).read_text(encoding="utf-8"))
    variants: dict[str, str] = {}
    for name, value in raw.items():
        if isinstance(value, dict) and value.get("file"):
            variants[str(name)] = Path(value["file"]).read_text(encoding="utf-8")
        else:
            variants[str(name)] = str(value)
    return variants


def cmd_run(args) -> int:
    s = _settings(args)
    if not s.races_dir:
        print("ERROR: races_dir is not configured", file=sys.stderr)
        return 1
    prompt = _read_prompt(args)
    variants = _load_variants(args)
    models = args.models.split(",") if args.models else None
    if getattr(args, "twin", None):
        # Twin/clone mode: ONE model against itself -- only the variant
        # axis varies, so prompt/skills/role influence is attributable.
        models = [args.twin]
        if not variants or len(variants) < 2:
            print("ERROR: twin mode needs --variants-file with >= 2 variants",
                  file=sys.stderr)
            return 1
    race = run_race(prompt, s, models=models,
                    mode=args.mode or None, repeats=args.repeats or None,
                    variants=variants)
    if race.plan.uncontrolled:
        print("WARN: models AND variants vary -- results are descriptive, "
              "no single-cause attribution", file=sys.stderr)
    evaluate_checks(race, s.checks)
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


def _task_checks(task_file: Path, fallback: list[dict]) -> list[dict]:
    """Per-discipline deterministic checks: ``<stem>.checks.json`` next to the
    task file wins over the config-wide ``checks`` list. Same schema as the
    config field ([{"name", "regex"}]); invalid entries are dropped, an
    unreadable file falls back to the config checks (reported on stderr).
    """
    candidate = task_file.with_suffix(".checks.json")
    if not candidate.exists():
        return fallback
    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARN: ignoring {candidate.name}: {exc}", file=sys.stderr)
        return fallback
    if not isinstance(data, list):
        print(f"WARN: {candidate.name} must be a JSON list", file=sys.stderr)
        return fallback
    return [entry for entry in data
            if isinstance(entry, dict) and entry.get("name") and entry.get("regex")]


def cmd_olympiade(args) -> int:
    """Several disciplines (task files), one field of models.

    Per task a normal race (inferential: only the model axis varies inside
    one discipline). Across tasks the aggregate is DESCRIPTIVE -- a medal
    table may rank, but must not attribute a cause; that is the same
    demotion rule the system-auditor enforces for multi-axis aggregation.
    Per-discipline checks live in ``<stem>.checks.json`` next to each task.
    """
    s = _settings(args)
    if not s.races_dir:
        print("ERROR: races_dir is not configured", file=sys.stderr)
        return 1
    tasks = sorted(Path(args.tasks_dir).glob("*.md"))
    if len(tasks) < 2:
        print("ERROR: an olympiad needs >= 2 task files (*.md)", file=sys.stderr)
        return 1
    models = args.models.split(",") if args.models else s.model_names()
    race_ids, failures = [], 0
    for task_file in tasks:
        prompt = task_file.read_text(encoding="utf-8")
        race = run_race(prompt, s, models=models, mode=args.mode or None,
                        repeats=args.repeats or None)
        annotate_costs(race, prompt, s.getriebe_path, settings=s)
        evaluate_checks(race, _task_checks(task_file, s.checks))
        write_artifacts(race, s.races_dir, prompt)
        write_scaffold(race, s.races_dir, prompt)
        race_ids.append((task_file.stem, race.plan.race_id))
        failures += sum(1 for r in race.results if not r.ok)
        print(f"discipline {task_file.stem}: {race.plan.race_id}")
    # Descriptive aggregate scaffold -- the judge fills the medals per
    # discipline from each RACE.md, the total row stays a count, not a cause.
    lines = [
        f"# OLYMPIADE {race_ids[0][1].split('--')[0]} — {len(tasks)} Disziplinen, "
        f"{len(models)} Modelle",
        "",
        "> **Deskriptiv:** Über Disziplinen hinweg variieren Aufgabe UND Modell —",
        "> der Medaillenspiegel zählt Siege je Disziplin (dort ist nur die",
        "> Modellachse variiert), erklärt aber keine Ursache über alles.",
        "",
        "| Disziplin | Race | Sieger (aus RACE.md-Urteil) |",
        "|---|---|---|",
    ]
    lines += [f"| {stem} | {rid} | |" for stem, rid in race_ids]
    lines += ["", "## Medaillenspiegel (zählen, nicht schließen)", "",
              "| Modell | Siege | Podium |", "|---|---|---|", ""]
    target = Path(s.races_dir) / f"OLYMPIADE-{race_ids[0][1].split('--')[0]}.md"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"olympiade scaffold: {target}")
    print("next: judge each discipline's RACE.md, then fill the medal table")
    return 0 if failures == 0 else 2


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
        p.add_argument("--variants-file", default=None,
                       help="JSON {name: prompt | {file: path}} -- the variant axis")
        p.add_argument("--twin", default=None, metavar="MODEL",
                       help="twin/clone mode: one model against itself, "
                       "variants required")
        p.set_defaults(func=func)

    p = sub.add_parser("olympiade", help="several tasks, one field of models -- "
                       "per-task races plus a descriptive medal scaffold")
    p.add_argument("--tasks-dir", required=True,
                   help="directory of *.md task prompts (one race per file)")
    p.add_argument("--models", default=None)
    p.add_argument("--mode", default=None, choices=["sequential", "parallel"])
    p.add_argument("--repeats", type=int, default=None)
    p.set_defaults(func=cmd_olympiade)

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
