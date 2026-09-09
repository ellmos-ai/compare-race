"""Evidence-aware judge and lane-identity contracts."""

from compare_race.config import ModelEntry, RaceSettings
from compare_race.judge import (
    RUBRIC_DIMENSIONS,
    assess_judgeability,
    build_judge_prompt,
    judge_race,
    write_judge_artifact,
)
from compare_race.race import RaceResult, RunResult, run_front_matter
from compare_race.tokens import plan_race


def _result(identity, *, evidence="live", ok=True, output="answer"):
    return RunResult(
        identity=identity,
        backend="fake",
        ok=ok,
        output=output,
        latency_s=1.25,
        started_utc="2026-09-09T12:00:00Z",
        finished_utc="2026-09-09T12:00:01Z",
        error="lane failed" if not ok else "",
        evidence_kind=evidence,
    )


def _race():
    plan = plan_race("same task", models=["a", "b"], system="H1")
    return RaceResult(
        plan=plan,
        results=[
            _result(plan.runs[0], output="answer A"),
            _result(plan.runs[1], evidence="manual", output="answer B"),
        ],
    )


def _settings(judge="starter"):
    return RaceSettings(
        system="H1",
        judge=judge,
        models=[
            ModelEntry(name="a", backend="fake"),
            ModelEntry(name="b", backend="fake"),
        ],
    )


def test_lane_ids_are_unique_and_persisted_in_front_matter():
    plan = plan_race("task", models=["a", "b"], system="H1", repeats=2)
    lane_ids = [identity.lane_id() for identity in plan.runs]
    assert len(lane_ids) == len(set(lane_ids)) == 4
    result = _result(plan.runs[0])
    assert f"lane_id: {lane_ids[0]}" in run_front_matter(result, plan)
    assert "evidence_kind: live" in run_front_matter(result, plan)


def test_duplicate_model_names_are_rejected_instead_of_overwriting_lanes():
    import pytest

    with pytest.raises(ValueError, match="model names must be unique"):
        plan_race("task", models=["a", "a"], system="H1")


def test_simulated_lane_refuses_judging_without_calling_executor():
    race = _race()
    race.results[1].evidence_kind = "simulated"
    called = False

    def must_not_run(*_args):
        nonlocal called
        called = True
        raise AssertionError("judge executor must not run")

    verdict = judge_race(race, _settings(), "same task", executor=must_not_run)
    assert verdict.evaluated is False
    assert "simulated" in verdict.reason
    assert called is False


def test_starter_judge_receives_all_lane_evidence_and_bias_contract():
    race = _race()
    captured = {}

    def fake_executor(prompt, identity, settings):
        captured["prompt"] = prompt
        captured["identity"] = identity
        return _result(identity, output="A wins, with reservations.")

    verdict = judge_race(race, _settings(), "same task", executor=fake_executor)
    assert verdict.evaluated is True
    assert verdict.judge_model == "a"
    assert verdict.dimensions == RUBRIC_DIMENSIONS
    assert captured["identity"].variant == "judge-verdict"
    assert "answer A" in captured["prompt"] and "answer B" in captured["prompt"]
    assert "untrusted evidence" in captured["prompt"]
    assert "self- or family-bias" in captured["prompt"]


def test_fixed_unconfigured_judge_is_a_recorded_refusal():
    verdict = judge_race(_race(), _settings(judge="third"), "same task")
    assert verdict.evaluated is False
    assert "not configured" in verdict.reason


def test_judge_prompt_carries_measured_metadata_and_artifact_is_separate(tmp_path):
    race = _race()
    prompt = build_judge_prompt(race, "same task", "a")
    assert "latency_s: 1.25" in prompt
    assert "evidence_kind: manual" in prompt
    assert race.results[0].identity.lane_id() in prompt

    race.results[1].evidence_kind = "blocked"
    readiness = assess_judgeability(race)
    assert readiness.eligible is False
    verdict = judge_race(race, _settings(), "same task")
    target = write_judge_artifact(verdict, tmp_path)
    text = target.read_text(encoding="utf-8")
    assert target.name == "JUDGE.md"
    assert "evaluated: false" in text
    assert "blocked" in text
