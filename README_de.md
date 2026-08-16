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

## Identität — sechs Achsen, wiederverwendet aus system-auditor

Jeder Lauf trägt `time · prompt · system · model · run · variant`. Zugeschrieben werden
darf nur, wenn genau eine Achse variiert: Modelle variieren → das Rennen; Läufe
variieren → Varianz eines Modells; Varianten variieren (Twin-Modus) → die Wirkung von
Prompt-Wortlaut, Skills oder Umgebung; Zeit variiert → Drift über Versionen. Die
Artefakt-Köpfe sprechen den Parser von
[`system-auditor`](https://github.com/ellmos-ai/system-auditor) — das ist die eine
harte Abhängigkeit.

## Rennmodi

| Modus | Was variiert | Was er beantwortet |
|---|---|---|
| **Race** (`run`) | Modell | welches Modell diese Aufgabe am besten löst |
| **Twin/Clone** (`run --twin`) | Variante (Prompt/Skills/Umgebung), ein Modell | was eine Prompt-Technik kausal wert ist |
| **Olympiade** (`olympiade`) | Modell je Disziplin, Aufgabe darüber hinweg | ein deskriptiver Medaillenspiegel über ein Testbundle |

Eine Olympiade ist ein **Testbundle**: je Disziplin eine Task-Datei, jede als normales
Race gefahren und je Disziplin gejudgt; das Aggregat bleibt deskriptiv — **zählen,
nicht schließen** (über Disziplinen hinweg variieren Aufgabe UND Modell, also darf
keine Ursache zugeschrieben werden). Deterministische Checks je Disziplin liegen als
`<task>.checks.json` neben der Task-Datei.

### Mitgelieferte Olympiade: Kantische Vernunft

[`olympiads/kantische-vernunft/`](olympiads/kantische-vernunft/) macht aus den sieben
Dimensionen des *kantischen Tests für LLMs* — plus *Distributional Rationality* aus
dem Erweiterungsteil — die erste ausführbare Testbatterie dieses Rahmenwerks. Das
Disziplinen-Design, der methodische Vorbehalt (gemessen wird
Strukturbedingungen-*Verhalten*, nie Vernunft selbst) und die Regel „zählen, nicht
schließen" stammen aus dem zugrunde liegenden Forschungspaper, das diese Form von
Olympiade operationalisiert:

> Geiger, L. (2026). *Der Mensch in der Maschine: Sind LLMs vernünftige Wesen im
> kantischen Sinne?* (v9.0). Zenodo.
> [doi:10.5281/zenodo.21899816](https://doi.org/10.5281/zenodo.21899816)
> (alle Versionen: [doi:10.5281/zenodo.18642673](https://doi.org/10.5281/zenodo.18642673))

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
