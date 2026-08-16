"""The race report scaffold -- mechanics by the tool, verdict by the judge.

The tool writes what is measurable (lane table, latencies, failures, a
mechanical answer tally for short categorical answers). The **verdict is
model-manual**: the starting model fills the judge rubric in RACE.md -- time is
only one dimension there, beside quality, correctness, completeness,
instruction fidelity and cost. This mirrors the system-auditor meta-audit
pattern: the library prepares and cross-checks, the model judges.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from system_auditor.report import parse_front_matter  # reused reader

from .race import RaceResult

_JUDGE_TEMPLATE = """## Judge-Urteil (modellmanuell -- Default: das startende Modell)

> Rubrik ausfuellen, je Zeile ein Modell (bei Wiederholungen: ueber die Laeufe
> mitteln und Varianz nennen). Die Stoppuhr ist nur EIN Bild -- Zeit ist eine
> Dimension unter mehreren. Danach die Blockquote-Hinweise loeschen.

| Modell | Qualitaet | Korrektheit | Vollstaendigkeit | Anweisungstreue | Latenz | Urteil |
|---|---|---|---|---|---|---|

### Begruendung je Modell

### Sieger und Vorbehalte

<Nur eine Achse variiert (Modelle)? Dann ist der Unterschied zuschreibbar.
Variieren Laeufe mit, gilt: erst Varianz je Modell ansehen, dann vergleichen.>
"""


def _normalise(text: str) -> str:
    return re.sub(r"\W+", " ", text.strip().lower()).strip()


def mechanical_tally(outputs: list[str]) -> dict:
    """Majority count over normalised answers -- only meaningful for SHORT,
    categorical answers (the swarm-ai consensus insight); free text rarely
    matches string-wise, so the tally reports usefulness honestly."""
    normalised = [_normalise(item)[:120] for item in outputs if item.strip()]
    counts = Counter(normalised)
    top, top_count = (counts.most_common(1)[0] if counts else ("", 0))
    return {
        "valid": len(normalised),
        "distinct": len(counts),
        "top_share": round(top_count / len(normalised), 2) if normalised else 0.0,
        "useful": len(counts) < len(normalised),  # any agreement at all?
        "top_answer": top[:80],
    }


def scaffold(race: RaceResult, prompt: str) -> str:
    plan = race.plan
    ok_results = [r for r in race.results if r.ok]
    lines = [
        "---",
        f"race_id: {plan.race_id}",
        f"time_token: {plan.time}",
        f"prompt_token: {plan.prompt_token}",
        f"system: {plan.system}",
        f"mode: {plan.mode}",
        f"lanes: {len(race.results)}",
        f"failed: {len(race.results) - len(ok_results)}",
        "judge: starter",
        "---",
        "",
        f"# RACE {plan.race_id} — {plan.mode}"
        + (" (Stoppuhr: Laufzeiten sauber je Spur)" if plan.mode == "sequential"
           else " (echtes Rennen: Laufzeiten teilen sich die Maschine)"),
        "",
        "## Prompt",
        "",
        "> " + prompt.strip().replace("\n", "\n> "),
        "",
        "## Spuren (gemessen)",
        "",
        "| Modell | Lauf | Backend | ok | Latenz s | ~Kosten USD (Schätzung) | Output |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(race.results, key=lambda x: (x.identity.model, x.identity.run)):
        cost = f"~{r.est_cost_usd} ({r.cost_gear})" if getattr(r, "cost_gear", "") else "—"
        lines.append(
            f"| {r.identity.model} | {r.identity.run} | {r.backend} | "
            f"{'ja' if r.ok else 'NEIN'} | {r.latency_s} | {cost} | {r.identity.filename()} |"
        )

    # Variance block: only when repetitions exist -- with n=1 a spread would
    # feign precision. Latency spread is measured; output-length spread is a
    # cheap proxy the judge refines qualitatively.
    per_model: dict[str, list] = {}
    for r in race.results:
        per_model.setdefault(r.identity.model, []).append(r)
    if any(len(v) > 1 for v in per_model.values()):
        lines += [
            "",
            "## Varianz je Modell (Wiederholungsachse)",
            "",
            "| Modell | n | ok | Latenz min/Ø/max s | Output-Länge min/Ø/max |",
            "|---|---|---|---|---|",
        ]
        for model, runs in sorted(per_model.items()):
            lat = [x.latency_s for x in runs]
            length = [len(x.output) for x in runs if x.ok]
            ok_n = sum(1 for x in runs if x.ok)
            lat_cell = f"{min(lat)}/{round(sum(lat) / len(lat), 1)}/{max(lat)}"
            len_cell = (
                f"{min(length)}/{round(sum(length) / len(length))}/{max(length)}"
                if length else "—"
            )
            lines.append(
                f"| {model} | {len(runs)} | {ok_n}/{len(runs)} | {lat_cell} | {len_cell} |"
            )
        lines += [
            "",
            "> Nur die **run**-Achse variiert innerhalb einer Zeile — Streuung hier ist",
            "> Modell-Varianz, kein Modellvergleich. Der Vergleich zwischen den Zeilen",
            "> gehört dem Judge.",
        ]
    tally = mechanical_tally([r.output for r in ok_results])
    lines += [
        "",
        "## Mechanische Vorstufe (nur fuer kurze, kategoriale Antworten aussagekraeftig)",
        "",
        f"- gueltige Antworten: {tally['valid']} · verschiedene (normalisiert): "
        f"{tally['distinct']} · Anteil haeufigste: {tally['top_share']}",
        f"- verwertbar: {'ja' if tally['useful'] else 'nein -- Freitext, der Judge entscheidet'}",
        "",
        _JUDGE_TEMPLATE,
    ]
    return "\n".join(lines) + "\n"


def write_scaffold(race: RaceResult, races_dir: str | Path, prompt: str) -> Path:
    target = Path(races_dir) / race.plan.race_id / "RACE.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(scaffold(race, prompt), encoding="utf-8")
    return target


def read_race_dir(race_dir: str | Path) -> list[dict]:
    """Read all RUN artefacts of a race directory (for the judge / a series)."""
    found = []
    for path in sorted(Path(race_dir).glob("RUN-*.md")):
        text = path.read_text(encoding="utf-8")
        header = parse_front_matter(text)
        if header:
            header["_body"] = text.split("---", 2)[-1].strip()
            header["_file"] = path.name
            found.append(header)
    return found


__all__ = ["mechanical_tally", "read_race_dir", "scaffold", "write_scaffold"]
