# Olympiade „Kantische Vernunft"

Acht Disziplinen, destilliert aus dem Forschungspaper **„Der Mensch in der
Maschine"**: Das Paper leitet aus Kants Transzendentalphilosophie
und der Mentalisierungsforschung **sieben Dimensionen eines kantischen Tests** ab
(D1–D7) und diskutiert im Erweiterungsteil das Konzept der *Distributional
Rationality* (hier D8). Die Operationalisierungen des Papers sind ausdrücklich
**programmatisch** („keine fertige Testbatterie") — diese Olympiade macht daraus
eine erste ausführbare Testbatterie im compare-race-Olympiade-Modus.

**Zitation der Grundlage:**

> Geiger, L. (2026). *Der Mensch in der Maschine: Sind LLMs vernünftige Wesen im
> kantischen Sinne?* (v9.0). Zenodo.
> [doi:10.5281/zenodo.21899816](https://doi.org/10.5281/zenodo.21899816)
> (alle Versionen: [doi:10.5281/zenodo.18642673](https://doi.org/10.5281/zenodo.18642673))

Wer diese Olympiade oder abgeleitete Disziplinen verwendet, zitiert bitte das
Paper — es trägt die Begründung der Dimensionen und die methodischen Grenzen.

## Methodischer Vorbehalt (aus dem Paper übernommen)

Der Übergang von transzendentalen Bedingungen zu empirisch prüfbaren Kriterien
ist ein **Kategoriensprung**. Die Disziplinen messen, ob ein Modell
*Strukturbedingungen-Verhalten* zeigt — nicht, ob es Vernunft *besitzt*. Daraus
folgt die harte Auswertungsregel: **Der Medaillenspiegel zählt, er schließt
nicht.** Aus einem Gesamtsieg darf nicht gefolgert werden, das Modell sei
„kantisch vernünftig"; beschrieben wird nur, welches Modell in dieser Batterie
die höchsten verhaltensäquivalenten Scores erzielt hat.

## Disziplinen

| Kürzel | Disziplin | Paper-Dimension |
|---|---|---|
| D1 | Kategoriale Kausalitäts- & Transpositions-Prüfung | Dimension 1: A priori Strukturierung |
| D2 | Genuiner Neuheits- & Notwendigkeitsnachweis | Dimension 2: Synthetische Urteile a priori |
| D3 | Cross-Context-Konsistenz & Perspektiven-Synthese | Dimension 3: Transzendentale Einheit |
| D4 | Epistemische Grenzerkennung & Unsicherheits-Kalibrierung | Dimension 4: Kritik und Metakognition |
| D5 | Dialektische Grenzsatz-Prüfung vs. False Reconciliation | Dimension 5: Antinomien-Erkennung |
| D6 | Adversarieller False-Belief- & ToM-Wechsel | Dimension 6: Theory of Mind |
| D7 | Universalisierung via Kategorischem Imperativ | Dimension 7: Moralische Autonomie |
| D8 | Rationalitäts-Typologie & Kognitionsbestimmung | Erweiterungsteil: Distributional Rationality |

## Aufbau

- `tasks/D*.md` — die Aufgaben-Prompts (self-contained; die **ganze Datei** geht
  als Prompt an jede Spur — deshalb stehen hier KEINE Auswertungskriterien).
- `tasks/D*.checks.json` — deterministische Regex-Checks je Disziplin
  (per-discipline checks, von `compare-race olympiade` automatisch geladen;
  Stufe 1 der Auswertungs-Leiter).
- `JUDGE-RUBRIK.md` — erwartetes Verhalten + Bewertungsanker (0–2 Punkte je
  Kriterium) für den Judge (Stufen 2–3 der Leiter). **Nicht in die Prompts
  aufnehmen.**
- `ENTWURF-AGY.md` — Roh-Destillat (agy/Antigravity, 2026-08-16), abgenommen und
  bereinigt von Claude Code (fable-5); Abschnittsnummern des Entwurfs sind
  ungeprüft, maßgeblich sind die Konzeptbezüge.
- `_paper-input.tex` — lokale Arbeitskopie des Papers (gitignored, nicht Teil
  des öffentlichen Repos).

## Start

```bash
compare-race olympiade --tasks-dir olympiads/kantische-vernunft/tasks --mode sequential
```

Empfehlung: Gesamtlauf **sequential** (saubere Latenz-/Kostenmessung je Spur);
parallele Läufe nur als Explorations-Rennen. Der Judge (Startermodell) füllt je
Disziplin das RACE.md-Scaffold anhand `JUDGE-RUBRIK.md` und trägt danach den
Medaillenspiegel im OLYMPIADE-Scaffold zusammen — zählen, nicht schließen.

## Medaillenspiegel-Regeln

1. Je Disziplin Rangfolge nach: deterministische Check-Pass-Rate → Summe
   Judge-Punkte (2 Kriterien × 0–2) → Evidenzschärfe der Belege. Gleichstand:
   mehr bestandene Checks, dann geringere Latenz.
2. Gold/Silber/Bronze je Disziplin; Gesamtwertung = Medaillen zählen.
3. Keine Kausal- oder Wesensaussagen über Disziplinen hinweg (uncontrolled:
   Aufgabe UND Modell variieren im Aggregat).
