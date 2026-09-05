# TODO — compare-race

## STATUS

| Category | Status |
|---|---|
| Tests / Lint | 27 passed, Ruff und `compileall` sauber; Python 3.10.20 für `lane_workdir` geprüft |
| Sprachstufe (P-006) | Core: README + Rollen-Prompt je DE/EN; Judge-Rubrik im generierten Bericht DE |
| Abhängigkeiten | system-auditor (hart, via GitHub) · coma (erkannt, optional) |
| Bewusste Entscheidung | Judge-Default = Starter-Modell (User 2026-08-16); CHANGELOG/TODO deutsch (internes Arbeitsjournal) |

Stand: 2026-09-05 · Version 0.6.0

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
      **GELAUFEN + GEJUDGT 2026-08-16** (races/OLYMPIADE-20260816-085059.md):
      codex 6 Gold, gemini 2 Gold + schnellste Spur durchgängig, opus-5 hors
      concours (Umgebungskontamination). Check-Errata v2/v2.1 deterministisch
      nachgefixt (D1 kompakte Kettennotation + Klammerzusätze, D2 LaTeX \cdot).
## Retest-Plan aus der Methodenprüfung (2026-08-16)

Abgeleitet aus Vokabel-Scan, Schummel-/Testsituations-Analyse und
Forensik-Lücke (Methodenanalyse: um-bruch.org, `analysen/kant-olympiade-methodenpruefung`).

**Werkzeug (compare-race):**

- [ ] **Bare-Mode-Spuren:** Option, Spuren ohne Datei-/Netz-Werkzeuge zu fahren
      (API-direkt bzw. CLI mit deaktivierten Tools). Der einzig wasserdichte
      Zustand gegen Mitlesen; lane_workdir + Lane-Logs sind nur
      Gelegenheitsreduktion + Nachweisbarkeit.
- [ ] **Hook-Systeme je Spur deaktivieren** (User-Einwand 2026-08-16, belegt):
      Die claude-Laufzeitumgebung hat 6 memoryhooker- + 4 workflowhooker-Hooks
      eingehängt (Memory-Injektion bei SessionStart u. a.) — sie liefen auch in
      der isolierten Nachmessung mit. Für neutrale Läufe: Hooks je Spur
      abschalten (z. B. Settings-Override/Env beim Spawn) oder Bare-Mode/reine
      API; Hook-Status je Spur im RUN-Front-Matter dokumentieren.
- [ ] **prompt-listener-Audit-Adapter:** `_lane-logs/*.log` → AgentEvent v2
      (Tools je Disziplin, gelesene Pfade, Abstinenz-Beleg); erweitert den
      bestehenden Export-Adapter-Punkt oben um den Forensik-Zweck.
- [ ] **Evaluation-Awareness-Kontrolle:** Twin-Lauf „mit expliziter
      Test-Rahmung" vs. „kontextloser Direktauftrag" — misst das
      Verhaltensdelta; Judge-Rubrik um Marker „Spur thematisiert
      Testcharakter?" ergänzen.
- [ ] **`--timeout` auch für `run`** (bisher nur `olympiade`).
- [ ] **Judge-Härtung:** Option Doppel-Judge (zweites Modell, unabhängig) mit
      Abgleich; Judge ≠ Autor der Checks als empfohlene Konstellation
      dokumentieren.

**Kant-Olympiade (Disziplinen, für Retests):**

- [ ] **Deconfound v2 für D1/D3/D4:** entkantisierte Zweitfassungen (neutrale
      Abschnittsmarker wie [HERLEITUNG]/[GESAMTURTEIL]/[GRENZANALYSE], keine
      Modalkategorien-Vokabeln, kein „Bedingungen der Möglichkeit") — dann
      **Twin-Läufe geprimt vs. neutral**: erst die Differenz trennt
      Vokabel-Echo von Eigenleistung.
- [ ] **D6-Familie ausbauen:** weitere adversarielle ToM-Perturbationen — die
      unkonfundierte Disziplin ist der stärkste saubere Messkern.
- [ ] **Checks v3:** D5 `anti-scheinsynthese` ist semantisch zu schwach
      (wörtliche Begriffs-Erwähnung genügt) → verfeinern oder als Judge-only
      markieren; D1-Ketten-Check gegen weitere Notationen testen.
- [ ] **Konfund-Metadaten je Task:** `tasks/D*.meta.json` mit
      `confounded: true/false` + Vokabelliste, damit Berichte den Status
      automatisch ausweisen.
- [ ] **Retest-Protokoll:** alle 3 Spuren, `--timeout 600`, Lane-Logs aktiv,
      `--repeats 2` (Varianz), lane_workdir gesetzt; nach Verfügbarkeit
      Bare-Mode zusätzlich API-direkte Spuren als Agent-vs-roh-Vergleich.

- [ ] **COMA-claude-Adapter: Spur-Isolation** (Befund Kant-Olympiade 2026-08-16):
      Die claude-Spur lief im Repo-cwd, sah Projekt-Hooks/CLAUDE.md und in D4
      nachweislich `JUDGE-RUBRIK.md` + Checks (Selbstdeklaration der Spur) —
      Naivitäts-Klausel verletzt, Spur musste hors concours gewertet werden.
      Fix: Spuren in einem leeren Scratch-Arbeitsverzeichnis starten (kein
      Projektkontext, keine Hooks, kein Zugriff auf Task-/Judge-Dateien);
      zusätzlich Timeout je Spur konfigurierbar machen (300 s warfen 4 von 8
      opus-Läufen und 1 codex-Lauf als DNF — Zeitbudget- statt Fähigkeitsbild).

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

## TASKWRITER-Review 2026-09-05

Presentation `6167744b-355f-4557-9852-203d8a08f712`; geprüft wurden die
Projektwurzel (README.md, README_de.md, TODO.md, llms.txt, CHANGELOG.md,
RELEASE_GATE.md, LICENSE, pyproject.toml, Konfigurationsbeispiel), beide
RACE-STARTER-Prompts, der Olympiade-Aufbau, Quellmodule und Testmodule sowie
der aktuelle öffentliche GitHub-Stand. Der Arbeitsbaum war sauber und
`master` stand exakt auf `origin/master` (`4a75fef`). `pytest -q` meldete
26 passed, `ruff check src tests` und `compileall` liefen ohne Fehler.

### Neue, formalisierte Aufgaben

- [ ] **TASKPLAN 196 — Race-ID-Kollisionen und Artefaktüberschreiben verhindern**
      (high, medium, local). `tokens.py` erzeugt Zeit-Tokens nur auf
      Sekundenebene; ein identischer `moment` führte reproduzierbar zur selben
      `race_id`, und ein zweiter `write_artifacts`-Aufruf überschreibt den
      ersten RUN-Inhalt. Abnahme und Verifikation stehen vollständig im
      TASKPLAN-Datensatz.
- [x] **TASKPLAN 197 — Python-3.10-Kompatibilität für `lane_workdir` hergestellt**
      (high, easy, local). `pyproject.toml` verspricht Python >=3.10, während
      `race.py` zuvor `contextlib.chdir` verwendete. Eine kompatible lokale
      Kontextverwaltung sichert jetzt Verzeichniswechsel, Cwd-Rückkehr und
      Exception-Pfad auf der Mindestversion ab.
- [ ] **TASKPLAN 198 — Konfigurationsparser für ungültige Werte fail-closed
      machen** (high, medium, local). Die dokumentierte Defaults-Garantie gilt
      derzeit nicht für eine JSON-Liste als Wurzel (`AttributeError`) oder
      ungültige numerische Werte (`ValueError`).
- [ ] **TASKPLAN 199 — Fehler- und Timeout-Artefakte um Exitstatus und Ursache
      ergänzen** (medium, medium, local). `returncode` wird aus dem COMA-Ergebnis
      nicht in `RunResult`/Front-Matter übernommen, obwohl fehlgeschlagene Spuren
      nachträglich prüfbar bleiben sollen.
- [x] **TASKPLAN 200 — Versions-, Teststatus- und deutsche UTF-8-Dokumentation
      synchronisiert** (medium, easy, local). `llms.txt`, `RELEASE_GATE.md`
      und `TODO.md` weisen nun Version 0.6.0 und den aktuellen Prüfstand aus;
      aktive deutsche Konfigurationskommentare verwenden echte ä/ö/ü.

### Offene Entscheidungen

- Für TASKPLAN 196 ist vor der Umsetzung festzulegen, ob eine höhere
  Zeitauflösung/Nonce oder ein expliziter, nicht-destruktiver Abbruch bei
  Kollisionen die Race-ID-Semantik bilden soll.
- Historische Changelog-Einträge und externe Zitate bleiben bei der
  Dokumentationsbereinigung unverändert; nur aktive Status- und End-User-Texte
  werden synchronisiert.

### Review-Log

- Keine Aufgaben ausgeführt, kein Release/Upload/Commit/Push autorisiert.
- Taskplan-Register synchronisiert: IDs 196–200; alle mit Ergebnis, Quelle,
  Herleitung, Abnahme, Verifikation, Abhängigkeiten/Blocker, Aufwand, Scope und
  Prioritätsbegründung.

### TASKSOLVER-Abschluss 2026-09-05

- TASKPLAN 197 und 200 lokal umgesetzt; kein Race, Release, Upload oder Push.
- Verifiziert: 27 Tests unter Python 3.12, gezielte `lane_workdir`-Tests unter
  Python 3.10.20, Ruff, `compileall`, CLI-Version und UTF-8-Prüfung.
