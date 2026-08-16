"""compare-race -- identity, plan, artefacts, scaffold, fallback."""
import json

import pytest

from compare_race.config import load
from compare_race.race import RaceResult, RunResult, run_front_matter, write_artifacts
from compare_race.report import mechanical_tally, read_race_dir, scaffold, write_scaffold
from compare_race.tokens import plan_race, prompt_token

# --- identity ---------------------------------------------------------------

def test_same_opening_words_different_prompts_do_not_collide():
    a = prompt_token("Schreibe einen Test fuer X und beweise ihn")
    b = prompt_token("Schreibe einen Test fuer Y und beweise ihn")
    assert a != b
    assert a.startswith("schreibe-einen-test-fuer-")


def test_plan_is_the_cross_product_models_times_repeats():
    plan = plan_race("p", models=["a", "b"], system="H1", repeats=3)
    assert len(plan.runs) == 6
    assert {(r.model, r.run) for r in plan.runs} == {
        (m, n) for m in ("a", "b") for n in (1, 2, 3)
    }
    # every lane is one distinct statement -> one distinct file
    assert len({r.filename() for r in plan.runs}) == 6


def test_plan_rejects_nonsense():
    with pytest.raises(ValueError):
        plan_race("p", models=[], system="H1")
    with pytest.raises(ValueError):
        plan_race("p", models=["a"], system="H1", mode="race")
    with pytest.raises(ValueError):
        plan_race("p", models=["a"], system="H1", repeats=0)


# --- artefacts speak the system-auditor parser -------------------------------

def _fake_result(identity, output="42", ok=True, latency=1.5):
    return RunResult(identity=identity, backend="fake", ok=ok, output=output,
                     latency_s=latency, started_utc="2026-08-16T00:00:00Z",
                     finished_utc="2026-08-16T00:00:02Z", error="" if ok else "boom")


def test_run_header_roundtrips_through_the_reused_parser(tmp_path):
    """The whole point of reusing system-auditor: its parser must read our
    headers, or the series/judge tooling would need a second reader."""
    from system_auditor.report import parse_front_matter

    plan = plan_race("What is 6*7?", models=["m1"], system="H1")
    result = _fake_result(plan.runs[0])
    header = parse_front_matter(run_front_matter(result, plan))
    assert header["model"] == "m1"
    assert header["run"] == 1
    assert header["ok"] is True
    assert header["prompt_token"] == plan.prompt_token


def test_artifacts_and_scaffold_land_in_the_race_dir(tmp_path):
    plan = plan_race("What is 6*7?", models=["m1", "m2"], system="H1")
    race = RaceResult(plan=plan, results=[_fake_result(r, output="42") for r in plan.runs])
    base = write_artifacts(race, tmp_path, "What is 6*7?")
    target = write_scaffold(race, tmp_path, "What is 6*7?")
    assert (base / "PROMPT.md").is_file()
    assert len(list(base.glob("RUN-*.md"))) == 2
    text = target.read_text(encoding="utf-8")
    assert "Judge-Urteil" in text and "| Modell | Qualitaet" in text.replace("ä", "ae")

    runs = read_race_dir(base)
    assert len(runs) == 2 and runs[0]["_body"]


def test_a_failed_lane_is_recorded_not_hidden(tmp_path):
    plan = plan_race("p", models=["m1"], system="H1")
    race = RaceResult(plan=plan, results=[_fake_result(plan.runs[0], ok=False)])
    base = write_artifacts(race, tmp_path, "p")
    text = (base / plan.runs[0].filename()).read_text(encoding="utf-8")
    assert "ok: false" in text and "boom" in text
    assert "NEIN" in scaffold(race, "p")


# --- mechanical tally is honest about free text ------------------------------

def test_tally_useful_for_categorical_useless_for_free_text():
    cat = mechanical_tally(["42", "42", "41"])
    assert cat["useful"] is True and cat["top_share"] == 0.67
    free = mechanical_tally(["a long essay", "another different essay", "third text"])
    assert free["useful"] is False


# --- config ------------------------------------------------------------------

def test_config_defaults_with_reason_and_mode_guard(tmp_path):
    missing = load(tmp_path / "nope.json")
    assert missing.source == "defaults"

    path = tmp_path / "compare-race.config.json"
    path.write_text(json.dumps({
        "system": "H1", "mode": "warp", "races_dir": "<HOME>/x",
        "models": [{"name": "codex", "backend": "codex"}],
    }), encoding="utf-8")
    settings = load(path, home="C:/U")
    assert settings.mode == "sequential"  # stopwatch fallback, with a note
    assert any("rejected" in note for note in settings.notes)
    assert settings.races_dir == "C:/U/x"
    assert settings.model_names() == ["codex"]


def test_run_without_coma_explains_the_manual_fallback(monkeypatch, tmp_path):
    import compare_race.race as race_mod

    monkeypatch.setattr(race_mod, "_coma_available", lambda: False)
    settings = load(tmp_path / "nope.json")
    settings.models = [type("E", (), {"name": "m", "backend": "codex", "model": ""})()]
    settings.system = "H1"
    with pytest.raises(RuntimeError, match="model-manually"):
        race_mod.run_race("p", settings, models=["m"])
