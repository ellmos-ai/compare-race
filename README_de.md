# compare-race

> Selber Prompt, mehrere Modelle — Stoppuhr oder echtes Rennen. Das **startende Modell
> urteilt**; Zeit ist nur eine Dimension des Urteils.

[English version](README.md)

## Was es tut

`compare-race` schickt einen Prompt an mehrere LLMs — **nacheinander** (die Stoppuhr:
eine Spur nach der anderen, saubere Einzelmessung) oder **gleichzeitig** (das echte
Rennen) — mit optionalen Wiederholungen je Modell, und sammelt jede Antwort als
Artefakt ein. Das Urteil ist **modellmanuell**: Das startende Modell liest die Spuren
und füllt eine mehrdimensionale Rubrik (Qualität, Korrektheit, Vollständigkeit,
Anweisungstreue, Latenz, Kosten). Die Stoppuhr ist nur ein Bild.

## Identität — fünf Achsen, wiederverwendet aus system-auditor

Jeder Lauf trägt `time · prompt · system · model · run`. Zugeschrieben werden darf nur,
wenn genau eine Achse variiert: Modelle variieren → das Rennen; Läufe variieren →
Varianz eines Modells; Zeit variiert → Drift über Versionen. Die Artefakt-Köpfe
sprechen den Parser von [`system-auditor`](https://github.com/ellmos-ai/system-auditor)
— das ist die eine harte Abhängigkeit.

## Installation und Nutzung

```bash
pip install -e .           # holt system-auditor von GitHub
# Ausführungsschicht (erkannt, nie vorausgesetzt):
git clone https://github.com/ellmos-ai/coma && pip install -e coma

cp config/compare-race.config.example.json compare-race.config.json
compare-race config
compare-race run --prompt-file frage.md --mode sequential --repeats 2
# ohne COMA: Spuren selbst ausführen, dann
compare-race record --model codex --output-file out.md --race-id <id>
```

Rollen-Prompt: [`prompts/RACE-STARTER.de.md`](prompts/RACE-STARTER.de.md)
(englisch: [`RACE-STARTER.en.md`](prompts/RACE-STARTER.en.md)).

## Nachbarn (erkannt, nie vorausgesetzt)

[coma](https://github.com/ellmos-ai/coma) Spawn/Polling/Dateiprotokoll ·
clutch Modellkatalog · swarm-ai N-Wiederholungs-Konsens (mechanisch) ·
MarbleRun sequenzielle Ketten. compare-race ergänzt, was keiner hat: den
**qualitativen Judge über Geschwister-Ausgaben** und das Kreuzprodukt
Wiederholungen×Modelle.

## Lizenz

MIT.
