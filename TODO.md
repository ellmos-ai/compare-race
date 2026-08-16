# TODO — compare-race

## STATUS

| Category | Status |
|---|---|
| Tests / Lint | 9 passed, ruff sauber |
| Sprachstufe (P-006) | Core: README + Rollen-Prompt je DE/EN; Judge-Rubrik im generierten Bericht DE |
| Abhängigkeiten | system-auditor (hart, via GitHub) · coma (erkannt, optional) |
| Bewusste Entscheidung | Judge-Default = Starter-Modell (User 2026-08-16); CHANGELOG/TODO deutsch (internes Arbeitsjournal) |

Stand: 2026-08-16 · Version 0.1.0

## Erledigt beim Fertigbau (2026-08-16)

- [x] **Smoke-Race** codex (82.7s) + gemini/agy (76.1s), sequential, beide grün;
      Judge-Urteil modellmanuell gefällt — fand sofort den COMA-API-Fehler (Fix 00e11f1).
- [x] Bundle-Anmeldung im agent-orchestration-bundle (optional, declared-component)
      + Registry-Binding; Quell-Commit 0baeb7f, Projektion byte-verifiziert.
- [x] Pointer-Skill DE+EN in der Skill-Bibliothek (Quality 4.8/5), deployed.
- [x] OneDrive-Spiegel + Katalog (55 Module) + Remote/Publish: Final Gate 10/10,
      https://github.com/ellmos-ai/compare-race (public, Tag v0.1.0).

## Offen — Anschlüsse (Nutzerideen 2026-08-16)

- [ ] **prompt-listener als Auswertungs-Nachbar** (`.RESEARCH/.LAB/_AI-LAB/prompt-listener`):
      Race-Artefakte → JSONL-Export (`compare-race export --format prompt-listener`),
      dessen Klassifikations-Pipeline (Typ/Zweck/Methode) über die Varianten-Prompts,
      Join mit Judge-Urteil/Checks → Techniken-Wirkungs-Tabelle. Stärkster Fall:
      Twin-Modus (WARUM gewinnt eine Variante — nicht nur WELCHE). Transferbericht
      im Donor-Projekt: `_transfer/TRANSFERBERICHT_COMPARE_RACE_ANSCHLUSS_2026-08-16.md`.
      **Kopplung überholt (Nutzer-Revision, gleicher Tag):** prompt-listener wurde
      als Fork-Master-Template bereits ausgekapselt (github.com/ellmos-ai/prompt-listener);
      der Adapter zielt jetzt auf das veröffentlichte Repo.
- [x] **Kant-Olympiade GEBAUT** (`olympiads/kantische-vernunft/`, 2026-08-16): 8
      Disziplinen (D1–D7 = die sieben Dimensionen des kantischen Tests aus „Mensch
      in der Maschine" v9, D8 = Distributional Rationality aus dem Erweiterungsteil).
      Entwurf via agy (`ENTWURF-AGY.md`; Codex-Route 3× an Infrastruktur gescheitert:
      2× CCC-Watchdog-Reap T-20260816-50, 1× defekter Codex-Sandbox-Runner
      T-20260816-51). `tasks/D*.md` + per-discipline `D*.checks.json` (CLI-Feature
      0.5.0) + `JUDGE-RUBRIK.md` + README mit methodischem Vorbehalt.
      **START steht aus — nur nach Nutzerfreigabe (Kontingente):**
      `compare-race olympiade olympiads/kantische-vernunft/tasks --mode sequential`

## Offen — vor Produktivnutzung

- [ ] Kosten je Spur erfassen (clutch getriebe.json anbinden) — bislang nur Latenz.
- [ ] Größeres Rennen mit repeats > 1 (Varianzachse) — auf Nutzerfreigabe (Kontingente).

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
