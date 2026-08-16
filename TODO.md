# TODO — compare-race

## STATUS

| Category | Status |
|---|---|
| Tests / Lint | 9 passed, ruff sauber |
| Sprachstufe (P-006) | Core: README + Rollen-Prompt je DE/EN; Judge-Rubrik im generierten Bericht DE |
| Abhängigkeiten | system-auditor (hart, via GitHub) · coma (erkannt, optional) |
| Bewusste Entscheidung | Judge-Default = Starter-Modell (User 2026-08-16); CHANGELOG/TODO deutsch (internes Arbeitsjournal) |

Stand: 2026-08-16 · Version 0.1.0

## Offen — vor Produktivnutzung

- [ ] **Smoke-Race** mit echten Spuren (codex+agy) — Praxistest des COMA-Pfads.
- [ ] Kosten je Spur erfassen (clutch getriebe.json anbinden) — bislang nur Latenz.
- [ ] Bundle-Rolle `output-arbitration` im agent-orchestration-bundle anmelden
      (Quell-Repo bundle-recipes-v1, Hash-Kaskade, Projektion — Verfahren geübt).
- [ ] Pointer-Skill `compare-race` in der Skill-Bibliothek (type: pointer).
- [ ] OneDrive-Spiegel (.MODULES/.ORCHESTRATION/compare-race) + Katalog + Remote/Publish
      (Final Gate wie system-auditor).

## Offen — Ausbau

- [ ] Serien über Races desselben prompt_token (Modell-Drift über Zeit) — Klassifikation
      via system_auditor.timeseries als Kontrolle.
- [ ] Varianz-Kennzahlen je Modell bei repeats > 1 (Länge/Latenz-Streuung) im Gerüst.
- [ ] `parallel` über echte COMA-Handles (start/wait_all) statt ThreadPool um run().

## Bewusst nicht gebaut

- **Judge als Code** — das Urteil ist modellmanuell (Starter füllt die Rubrik);
  die mechanische Vorstufe sagt ehrlich, wann sie nichts taugt (Freitext).
- **Eigener Fanout-Unterbau** — COMA macht Spawn/Polling/Dateiprotokoll.
- **Eigener Front-Matter-Parser** — system-auditor wird importiert, nicht kopiert.
