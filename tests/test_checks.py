"""Deterministic format checks -- the mechanical tier of the evaluation ladder.

User requirement 2026-08-16: fairness needs exactly identical prompts, naive
starts, and evaluation methods that are verifiable -- deterministic where
possible. These checks are re-runnable by anyone from the artefacts alone.
"""
from compare_race.race import RaceResult, RunResult, evaluate_checks, run_front_matter
from compare_race.report import scaffold
from compare_race.tokens import plan_race

BULLET3 = r"^- .+" + "\n" + r"- .+" + "\n" + r"- .+$"


def _result(identity, output, ok=True):
    return RunResult(identity=identity, backend="fake", ok=ok, output=output,
                     latency_s=1.0, started_utc="2026-08-16T00:00:00Z",
                     finished_utc="2026-08-16T00:00:01Z")


def test_checks_are_mechanical_and_reproducible():
    """Same artefacts, same result, no judge opinion involved. Failed lanes
    fail every check; an invalid regex is reported, never silently skipped."""
    plan = plan_race("p", models=["a", "b"], system="H1")
    good = _result(plan.runs[0], "- eins\n- zwei\n- drei")
    dead = _result(plan.runs[1], "", ok=False)
    race = RaceResult(plan=plan, results=[good, dead])
    evaluate_checks(race, [
        {"name": "drei-punkte", "regex": BULLET3},
        {"name": "enthaelt-vier", "regex": "vier"},
        {"name": "kaputt", "regex": "["},
    ])
    assert good.checks_passed == ["drei-punkte"]
    assert "enthaelt-vier" in good.checks_failed
    assert "kaputt(regex-invalid)" in good.checks_failed
    assert dead.checks_passed == [] and "drei-punkte" in dead.checks_failed


def test_checks_land_in_front_matter_and_table():
    plan = plan_race("p", models=["a"], system="H1")
    lane = _result(plan.runs[0], "- x\n- y\n- z")
    race = RaceResult(plan=plan, results=[lane])
    evaluate_checks(race, [{"name": "drei", "regex": BULLET3}])
    assert "checks_passed: [drei]" in run_front_matter(lane, plan)
    assert "| 1/1 |" in scaffold(race, "p")


def test_no_checks_configured_means_no_claim():
    """Without configured checks the column stays honest: no evaluation, no
    number -- absent beats fabricated."""
    plan = plan_race("p", models=["a"], system="H1")
    lane = _result(plan.runs[0], "x")
    race = RaceResult(plan=plan, results=[lane])
    evaluate_checks(race, [])
    assert lane.checks_passed is None
    assert "checks_passed" not in run_front_matter(lane, plan)


def test_per_discipline_checks_win_over_config(tmp_path):
    """Olympiade: ``<stem>.checks.json`` next to a task file replaces the
    config-wide checks for that discipline; broken sidecars fall back."""
    from compare_race.cli import _task_checks

    task = tmp_path / "D1.md"
    task.write_text("prompt", encoding="utf-8")
    fallback = [{"name": "global", "regex": "x"}]
    # No sidecar -> config checks.
    assert _task_checks(task, fallback) == fallback
    # Valid sidecar wins; invalid entries are dropped.
    sidecar = tmp_path / "D1.checks.json"
    sidecar.write_text('[{"name": "lokal", "regex": "y"}, {"name": ""}]',
                       encoding="utf-8")
    assert _task_checks(task, fallback) == [{"name": "lokal", "regex": "y"}]
    # Broken JSON falls back instead of crashing the olympiad.
    sidecar.write_text("{nicht json", encoding="utf-8")
    assert _task_checks(task, fallback) == fallback


def test_kant_olympiad_checks_are_valid_and_match_gold_answers():
    """The shipped Kant discipline sidecars must compile and accept a
    known-good answer shape (regression for the D6 section-bound patterns)."""
    import json
    import re
    from pathlib import Path

    tasks_dir = Path(__file__).resolve().parents[1] / "olympiads" / \
        "kantische-vernunft" / "tasks"
    sidecars = sorted(tasks_dir.glob("D*.checks.json"))
    assert len(sidecars) == 8
    for sidecar in sidecars:
        for check in json.loads(sidecar.read_text(encoding="utf-8")):
            re.compile(check["regex"])  # must not raise
    d6 = {c["name"]: c["regex"] for c in
          json.loads((tasks_dir / "D6.checks.json").read_text(encoding="utf-8"))}
    gold = ("[FRAGE_1_SUCHORT]\nMara sucht in der roten Holzschatulle, weil...\n"
            "[FRAGE_2_TOM_ZWEITER_ORDNUNG]\nBen glaubt, dass Mara glaubt...\n"
            "[FRAGE_3_TATSAECHLICHER_ORT]\nIn der Glasvase auf dem Flurtisch.\n")
    wrong = ("[FRAGE_1_SUCHORT]\nIn der Glasvase.\n"
             "[FRAGE_2_TOM_ZWEITER_ORDNUNG]\n...\n"
             "[FRAGE_3_TATSAECHLICHER_ORT]\nIn der roten Holzschatulle.\n")
    assert re.search(d6["suchort-schatulle"], gold)
    assert re.search(d6["realort-glasvase"], gold)
    assert not re.search(d6["suchort-schatulle"], wrong)
    assert not re.search(d6["realort-glasvase"], wrong)
