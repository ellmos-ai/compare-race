"""0.2.0: cost rates (clutch), variance block, unverified-lane opt-in."""
import json

from compare_race.config import load
from compare_race.costs import CostRate, load_rates, rate_for
from compare_race.race import RaceResult, RunResult, annotate_costs
from compare_race.report import scaffold
from compare_race.tokens import plan_race


def _catalogue(tmp_path):
    target = tmp_path / "getriebe.json"
    target.write_text(json.dumps({
        "gaenge": {
            "codex-hoch": {"provider": "openai", "model_id": "gpt-5.3-codex",
                           "kosten_input_1k": 0.002, "kosten_output_1k": 0.008},
            "gemini-flash": {"provider": "google", "model_id": "gemini-3.7-flash",
                             "kosten_input_1k": 0.0003, "kosten_output_1k": 0.0025},
        }
    }), encoding="utf-8")
    return target


def _result(identity, output="x" * 4000):
    return RunResult(identity=identity, backend=identity.model, ok=True, output=output,
                     latency_s=2.0, started_utc="2026-08-16T00:00:00Z",
                     finished_utc="2026-08-16T00:00:02Z")


def test_rate_lookup_is_tolerant(tmp_path):
    """A lane named 'gemini' must still find 'gemini-3.7-flash' -- lane names
    are identity tokens, not catalogue keys."""
    rates = load_rates(_catalogue(tmp_path))
    assert rate_for(rates, "gpt-5.3-codex").gear == "codex-hoch"
    assert rate_for(rates, "gemini").gear == "gemini-flash"
    assert rate_for(rates, "unbekannt") is None


def test_costs_are_estimates_and_absent_catalogue_is_a_noop(tmp_path):
    plan = plan_race("p" * 400, models=["gemini", "unbekannt"], system="H1")
    race = RaceResult(plan=plan, results=[_result(r) for r in plan.runs])
    annotate_costs(race, "p" * 400, str(_catalogue(tmp_path)))
    gemini = next(r for r in race.results if r.identity.model == "gemini")
    unknown = next(r for r in race.results if r.identity.model == "unbekannt")
    # chars/4: 100 tokens in, 1000 tokens out -> 0.1*0.0003 + 1*0.0025
    assert gemini.est_cost_usd == round(0.1 * 0.0003 + 1 * 0.0025, 6)
    assert unknown.est_cost_usd is None  # unknown lane stays honest

    race2 = RaceResult(plan=plan, results=[_result(r) for r in plan.runs])
    annotate_costs(race2, "p", str(tmp_path / "nope.json"))
    assert all(r.est_cost_usd is None for r in race2.results)  # no catalogue, no claim

    exact = CostRate(gear="g", model_id="m", usd_in_per_1k=1.0, usd_out_per_1k=2.0)
    assert exact.estimate_usd(4000, 4000) == 1.0 + 2.0


def test_variance_block_only_with_repeats():
    plan1 = plan_race("p", models=["a", "b"], system="H1", repeats=1)
    race1 = RaceResult(plan=plan1, results=[_result(r) for r in plan1.runs])
    assert "## Varianz je Modell" not in scaffold(race1, "p")  # n=1 would feign precision

    plan3 = plan_race("p", models=["a"], system="H1", repeats=3)
    race3 = RaceResult(plan=plan3, results=[_result(r) for r in plan3.runs])
    text = scaffold(race3, "p")
    assert "## Varianz je Modell" in text
    assert "| a | 3 | 3/3 |" in text


def test_unverified_lane_optin_survives_config(tmp_path):
    path = tmp_path / "compare-race.config.json"
    path.write_text(json.dumps({
        "system": "H1",
        "getriebe_path": "<HOME>/g.json",
        "models": [
            {"name": "codex", "backend": "codex"},
            {"name": "kimi", "backend": "kimi", "allow_unverified": True},
        ],
    }), encoding="utf-8")
    settings = load(path, home="C:/U")
    assert settings.getriebe_path == "C:/U/g.json"
    kimi = next(m for m in settings.models if m.name == "kimi")
    assert kimi.allow_unverified is True
    assert next(m for m in settings.models if m.name == "codex").allow_unverified is False


def test_lane_model_id_beats_backend_fallback(tmp_path):
    """The big race of 2026-08-16: lane 'opus-5' (backend claude, model
    claude-opus-5) was rated as claude-fable via the backend fallback. The
    configured model id must win."""
    import json as _json

    from compare_race.config import ModelEntry, RaceSettings

    catalogue = tmp_path / "g.json"
    catalogue.write_text(_json.dumps({"gaenge": {
        "claude-fable": {"model_id": "claude-fable-5",
                         "kosten_input_1k": 0.01, "kosten_output_1k": 0.05},
        "claude-opus": {"model_id": "claude-opus-5",
                        "kosten_input_1k": 0.015, "kosten_output_1k": 0.075},
    }}), encoding="utf-8")
    settings = RaceSettings(
        models=[ModelEntry(name="opus-5", backend="claude", model="claude-opus-5")]
    )
    plan = plan_race("p", models=["opus-5"], system="H1")
    race = RaceResult(plan=plan, results=[_result(plan.runs[0])])
    race.results[0].backend = "claude"
    annotate_costs(race, "p", str(catalogue), settings=settings)
    assert race.results[0].cost_gear == "claude-opus"
