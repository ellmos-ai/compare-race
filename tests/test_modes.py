"""Race modes -- race, twin/clone, olympiade (user taxonomy 2026-08-16).

Race: models vary, task fixed. Twin: ONE model against itself, only the
variant axis varies -- prompt/skills/role influence becomes attributable.
Olympiade: several tasks; inferential inside a discipline, descriptive across.
"""
import json

from compare_race.config import ModelEntry, RaceSettings
from compare_race.race import RaceResult, RunResult, run_front_matter
from compare_race.tokens import plan_race


def _result(identity, output="x"):
    return RunResult(identity=identity, backend="fake", ok=True, output=output,
                     latency_s=1.0, started_utc="2026-08-16T00:00:00Z",
                     finished_utc="2026-08-16T00:00:01Z")


def test_twin_plan_is_one_model_times_variants_times_repeats():
    plan = plan_race("task", models=["opus"], system="H1", repeats=2,
                     variants=["knapp", "mit-rolle", "mit-skill"])
    assert len(plan.runs) == 6
    assert plan.uncontrolled is False  # only the variant axis varies
    assert {r.variant for r in plan.runs} == {"knapp", "mit-rolle", "mit-skill"}
    # every (variant, run) is one distinct statement -> one distinct file
    assert len({r.filename() for r in plan.runs}) == 6
    assert "RUN-opus-v-mit-rolle-r1.md" in {r.filename() for r in plan.runs}


def test_base_variant_keeps_the_old_filenames():
    """Backwards compatibility: race mode without variants must produce the
    same artefact names as before the sixth axis existed."""
    plan = plan_race("task", models=["a"], system="H1")
    assert plan.runs[0].filename() == "RUN-a-r1.md"
    assert "variant: base" in run_front_matter(_result(plan.runs[0]), plan)


def test_varying_models_and_variants_is_demoted_to_descriptive():
    plan = plan_race("task", models=["a", "b"], system="H1", variants=["v1", "v2"])
    assert plan.uncontrolled is True
    from compare_race.report import scaffold
    race = RaceResult(plan=plan, results=[_result(r) for r in plan.runs])
    assert "Deskriptiv" in scaffold(race, "task")


def test_duplicate_variant_names_are_rejected():
    import pytest

    with pytest.raises(ValueError):
        plan_race("task", models=["a"], system="H1", variants=["x", "x"])


def test_variant_prompts_reach_their_lanes(monkeypatch, tmp_path):
    """Twin mode's whole point: each lane runs ITS wording; the task token
    stays shared so the race directory holds all variants together."""
    import compare_race.race as race_mod

    seen: dict[str, str] = {}

    def fake_run_one(prompt, identity, settings):
        seen[identity.variant] = prompt
        return _result(identity, output=prompt)

    monkeypatch.setattr(race_mod, "_coma_available", lambda: True)
    monkeypatch.setattr(race_mod, "_run_one", fake_run_one)
    settings = RaceSettings(system="H1",
                            models=[ModelEntry(name="opus", backend="claude")])
    race = race_mod.run_race("BASE task", settings, models=["opus"],
                             mode="sequential",
                             variants={"knapp": "Kurz: tu X", "hoeflich": "Bitte tu X"})
    assert seen == {"knapp": "Kurz: tu X", "hoeflich": "Bitte tu X"}
    assert len({r.identity.prompt for r in race.results}) == 1  # shared task token


def test_olympiade_needs_two_disciplines_and_writes_scaffold(tmp_path, monkeypatch, capsys):
    import compare_race.cli as cli
    import compare_race.race as race_mod

    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks/sprint.md").write_text("Aufgabe eins", encoding="utf-8")
    (tmp_path / "tasks/marathon.md").write_text("Aufgabe zwei", encoding="utf-8")
    config = tmp_path / "compare-race.config.json"
    config.write_text(json.dumps({
        "system": "H1", "races_dir": str(tmp_path / "races").replace("\\", "/"),
        "models": [{"name": "a", "backend": "codex"}, {"name": "b", "backend": "codex"}],
    }), encoding="utf-8")

    monkeypatch.setattr(race_mod, "_coma_available", lambda: True)
    monkeypatch.setattr(race_mod, "_run_one",
                        lambda prompt, identity, settings: _result(identity, output="ok"))
    rc = cli.main(["--config", str(config), "olympiade",
                   "--tasks-dir", str(tmp_path / "tasks"), "--mode", "sequential"])
    assert rc == 0
    scaffolds = list((tmp_path / "races").glob("OLYMPIADE-*.md"))
    assert len(scaffolds) == 1
    text = scaffolds[0].read_text(encoding="utf-8")
    assert "2 Disziplinen" in text and "Medaillenspiegel" in text
    assert "| marathon |" in text and "| sprint |" in text
    assert "zählen, nicht schließen" in text
