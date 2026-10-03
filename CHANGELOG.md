# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

## [Unreleased]

Pfad B Discoverability, 4-View ASCII Architekturtopologie, Level 1 SBOM Re-Audit & Vertragstest-Erweiterung (Stand 2026-10-04; Version 0.7.2 strikt eingefroren per T-20260920-167562623); Vorläufer Pfad A Hygiene (2026-10-01), Pfad B Discoverability (2026-09-29) und Pfad A (2026-09-23).

### Hinzugefügt

- **4-View ASCII Architekturtopologie & Discoverability (Pfad B 2026-10-04)** (`README.md`, `README_de.md`):
  - Bilinguale 4-View Architekturprojektion in beiden READMEs mit den Schichten CLI & Planning (View 1), Adapters & Sandboxing (View 2), Evidence & Front-Matter (View 3) und Starter-Judge & Olympiad (View 4).
  - Direkte Einbettung und Abbildung aller 10 kanonischen Invarianten (`INV-LOCAL-01` bis `INV-SLA-10`) in den Topologie-Block.
  - Synchronisation von Verified-Badges (`2026-10-04`), Testabdeckungs-Badges (`69 passed | 100% green`), Level 1 SBOM Audit-Aktualität (`2026-10-04` in `THIRD_PARTY_LICENSES.md` und `THIRD_PARTY_LICENSES.txt`) und `llms.txt`.
- **Erweiterte Vertragstest-Suite** (`tests/test_metadata.py`):
  - Neuer Contract-Test `test_ascii_topology_projection_present` zur Prüfung der 4-View ASCII Topologie und Invarianten-Abdeckung in beiden READMEs.
  - Neuer Contract-Test `test_marketing_log_section_13` zur Bestätigung der Pfad-B-Dokumentation in `MARKETING-LOG.txt`.
  - Aktualisierte Aktualitätsprüfungen für Verified-Badge, Level 1 SBOM Re-Audit und `llms.txt` (2026-10-04).


- **CI-Lifecycle-Workflows & Labels** (`.github/workflows/`, `.github/labels.yml`):
  - `.github/workflows/auto-assign.yml`: Automatischer Reviewer-/Assignee-Zuweisungsworkflow (`actions/github-script@v7`) für neue Pull Requests mit Least-Privilege Berechtigungen (`pull-requests: write`, `issues: write`), Concurrency `cancel-in-progress: true` und 5-Minuten-Timeout.
  - `.github/workflows/label-sync.yml`: Automatisierter Workflow zur Synchronisation von Repository-Labels (`EndBug/label-sync@v2`) mit Least-Privilege Berechtigungen (`issues: write`), Concurrency und 5-Minuten-Timeout.
  - `.github/labels.yml`: Kanonischer Label-Katalog mit 11 Standard-Labels gemäß GOVERNANCE.md §4.2 (`bug`, `enhancement`, `good first issue`, `help wanted`, `documentation`, `duplicate`, `wontfix`, `priority: high`, `priority: low`, `needs-triage`, `stale`, `security`, `dependencies`).
- **Bilinguale Contributing-Richtlinien** (`CONTRIBUTING.md`):
  - Umfassende zweisprachige (EN/DE) Richtlinien mit Entwicklungs-Workflow, Quality Gates, unprivilegierter RunAsInvoker Non-Elevation Garantie (`INV-SEC-02`), Version-Freeze-Disziplin (`T-20260920-167562623`) und allen 10 Invarianten `INV-LOCAL-01` bis `INV-SLA-10`.
- **Level 1 SBOM Plain-Text Companion** (`THIRD_PARTY_LICENSES.txt`):
  - Kanonische Reintext-Begleitdatei zur softwaretechnischen Lizenztransparenz mit Bestätigung aller 10 Governance- und Laufzeitinvarianten `INV-LOCAL-01` bis `INV-SLA-10`, 0% Copyleft / AGPL / GPL Isolation und Volltextlizenzen (MIT, PSFL 2.0, Apache-2.0).
- **Multi-Host-, Cache- & Lock-Schutz** (`.gitignore`):
  - Härtung gegen Ideapad-Sync-Artefakte (`*-IDEAPAD*`, `*-IDEAPAD-GEI*`), Workstation-Dateien (`*-WORKSTATION.*`, `*-WORKSTATION-LG.*`), Systemdateien (`Desktop.ini`, `ehthumbs.db`), Taskplan-Notizen (`TASKPLAN_*.md`) und Multi-Agent-Sperren (`LOCK.dev.*`, `LOCK.antigravity.*`, `LOCK.bugsearch.*`).
- **PEP 621 Metadaten & Pytest-Härtung** (`pyproject.toml`):
  - `license-files` Whitelist um `THIRD_PARTY_LICENSES.txt` erweitert.
  - URLs `Contributing`, `Third-Party Licenses (Text)` und `Plain-Text License` unter `[project.urls]` registriert.
  - Pytest `norecursedirs` um `.pytest_tmp*`, `.tox`, `.hypothesis`, `.turbo` gehärtet.
- **Erweiterte Vertragstest-Suite** (`tests/test_metadata.py`):
  - Neue Contract-Tests zur Validierung der auto-assign/label-sync Workflows, labels.yml, CONTRIBUTING.md, THIRD_PARTY_LICENSES.txt, erweiterten .gitignore Multi-Host-Tokens und PEP 621 URLs/license-files.

- **20-Topic- & Keyword-Sättigung** (`pyproject.toml`):
  - Synchronisation aller 20 offiziellen GitHub-Repository-Topics (`ai-benchmarking`, `benchmark`, `cli`, `ellmos-ai`, `evaluation`, `kantian-reason`, `llm`, `local-first`, `model-comparison`, `model-evaluation`, `multi-agent`, `olympiad`, `open-bricks`, `prompt-engineering`, `python`, `race`, `starter-judge`, `stopwatch`, `twin-mode`, `zero-egress`) als kanonische PEP 621 Keywords.
- **Badges & Attribution-Verankerung** (`README.md`, `README_de.md`):
  - Formelle `Attribution: NOTICE`- und `Verified: 2026-09-29`-Badges verankert.
  - Testabdeckungs-Badge auf 61 passed (100% grün) synchronisiert.
- **Level 1 SBOM Re-Audit** (`THIRD_PARTY_LICENSES.md`):
  - Formeller Re-Audit Stand 2026-09-29 mit 10-Invarianten-Kreuzreferenzmatrix (`INV-LOCAL-01` bis `INV-SLA-10`), `RunAsInvoker`-Nicht-Eskalationsnachweis und Zero-Copyleft-Garantie.
- **LLM-Kontext & Discovery-Index** (`llms.txt`):
  - Aktualisierung des Prüfstands auf 2026-09-29 und 61 Vertragstests.
- **Erweiterte Vertragstest-Suite** (`tests/test_metadata.py`):
  - Neue Contract-Tests zur Validierung der 20-Topic-Keywords, Marketing-Log-Abschnitt 11, README Attribution/Verified-Badges und Re-Audit-Aktualität 2026-09-29.
- **CI-Lifecycle-Workflows** (`.github/workflows/`):
  - `stale.yml`: Concurrency-Gruppe mit `cancel-in-progress: true` und `timeout-minutes: 10` Guardrail gegen hängende Jobs.
  - `welcome.yml`: Automatische Erstbegrüßung für Issues und Pull Requests (`actions/first-interaction@v3`) mit Least-Privilege Berechtigungen (`issues: write`, `pull-requests: write`), Concurrency und 5-Minuten-Timeout.
- **Multi-Host-, Cache- & Lock-Schutz** (`.gitignore`):
  - Umfassende Ausschlussmuster für Multi-Device-Betrieb (`*-WORKSTATION-LG*`, `*-ASUS-GEI*`, `*-LAPTOP*`, `*-Mac Studio*`, `*-MacBook*`).
  - Schutz vor verwaisten Lock-Token (`LOCK.user.*`, `LOCK.until.*`, `LOCK.condition.*`, `LOCK.permissions.json`, `uv.lock`, `!package-lock.json`).
  - Ausschluss flüchtiger Test-Caches (`.pytest_temp/`, `.hypothesis/`, `.turbo/`, `.nyc_output/`).
- **PEP 621 Metadaten & Pytest-Konfiguration** (`pyproject.toml`):
  - Offizielle `Notice` URL unter `[project.urls]`.
  - Pytest-Härtung mit `minversion = "7.0"` und `norecursedirs` Ausschluss von Versionskontroll- und Cache-Verzeichnissen.

### Geändert

- **Marketing- & Audit-Register** (`MARKETING-LOG.txt`):
  - Abschnitt 11 mit Pfad B Discoverability- und Metadaten-Audit Stand 2026-09-29 ergänzt.
  - Abschnitt 10 mit Turnus-Hygiene-Prüfung (Pfad A) Stand 2026-09-23 dokumentiert.

## [0.7.2] - 2026-09-20

Discoverability-, Marketing- und Design-Parität (Pfad B), 18-Punkte-Bilinguale Navigation, Level 1 SBOM mit Invarianten-Matrix, formelle NOTICE-Akkreditierung und § 521 BGB Haftungsbegrenzung.

### Hinzugefügt

- **18-Punkte-Bilinguale Schnellnavigation**: Vollständige Synchronisation zwischen `README.md` und `README_de.md` mit reziproken dualen HTML-Ankern (`<a id="..."></a>`) und rückwärtskompatiblen Sprungmarken.
- **Zielgruppen & SEO-Suchanfragen (Abschnitt 4)**: Detaillierte Entwickler- und Forscher-Personas (`[PERSONA-01]` bis `[PERSONA-04]`) mit zweisprachigen High-Intent-Suchbegriffen direkt in beiden READMEs verankert.
- **10-Dimensionen-Vergleichsmatrix (Abschnitt 5)**: Umfassende Gegenüberstellung von `compare-race` vs. LMSYS Chatbot Arena, lm-evaluation-harness und Ad-Hoc Python-Skripten, abgebildet auf die System-Invarianten `INV-LOCAL-01` bis `INV-SLA-10`.
- **Level 1 SBOM & Invarianten-Kreuzreferenz** (`THIRD_PARTY_LICENSES.md`): Stand 2026-09-20 mit Invariant Cross-Reference Matrix, RunAsInvoker-Zertifizierung und Zero-Copyleft-Isolationsgarantie.
- **Formelle Urheberrechts- und Projekt-Notice** (`NOTICE`): Eindeutige Kennzeichnung der `ellmos-ai`-Zugehörigkeit und der Dachorganisation `open-bricks`.
- **Gesetzlicher Haftungsausschluss (§ 521 BGB Gefälligkeitsrecht)**: Klare Absicherung der unentgeltlichen Schenkung mit Haftungsbeschränkung auf Vorsatz und grobe Fahrlässigkeit in Abschnitt 18 beider Dokumentationen.
- **Erweiterte Vertragstest-Suite** (`tests/test_metadata.py`): Umfassende Überprüfung von 18 Navigationspunkten, dualen HTML-Ankern, semikolonfreier Mermaid-Syntax, Personas, Vergleichsmatrix, Level 1 SBOM, NOTICE und § 521 BGB.

### Geändert

- **PEP 621 Metadaten & Themen**: `pyproject.toml` auf Version 0.7.2 aktualisiert, `license-files` mit `NOTICE` und `THIRD_PARTY_LICENSES.md` verknüpft, Repository-Keywords erweitert und GitHub-Topics synchronisiert.
- **LLM-Kontextdatei (`llms.txt`)**: Audit-Stempel auf 2026-09-20 und Version 0.7.2 aktualisiert, 18-Punkte-Navigationsreferenz und Level 1 SBOM-Verweise hinterlegt.

## [0.7.1] - 2026-09-13

Pfad A Technische Hygiene, CI-Härtung (Timeout Guardrail & Python 3.13 Matrix), Multi-Host-Synchronisationsabwehr und Vertragstest-Erweiterung.

### Hinzugefügt

- **CI-Timeout-Guardrail & Python 3.13 Matrix** (`.github/workflows/ci.yml`): `timeout-minutes: 15` Schutz vor hängenden Runnern und Erweiterung der Test-Matrix um Python 3.13.
- **Multi-Host-Sync-Härtung** (`.gitignore`): Ergänzung kanonischer Ausschlussmuster gegen OneDrive- und Rechner-Konfliktdateien (`*conflicted copy*`, `*(kopie)*`, `*-WORKSTATION-*`, `*-ASUS-*`).
- **PEP 621 Metadaten-Erweiterung** (`pyproject.toml`): Python 3.13 Classifier und "LLM Context" URL für maschinenlesbare Auffindbarkeit via `llms.txt`.
- **Vertragstest-Erweiterung** (`tests/test_metadata.py`): Neue Contract-Tests für CI-Timeout, Python 3.13 Classifier, Multi-Host Sync-Muster, PEP 621 URLs, CHANGELOG [0.7.1] und llms.txt Konsistenz (45 Tests, 100% grün).

### Geändert

- **Versions- und Status-Harmonisierung**: Anhebung auf Version 0.7.1 über `src/compare_race/__init__.py`, `pyproject.toml`, `README.md`, `README_de.md`, `llms.txt` und `MARKETING-LOG.txt`.

## [0.7.0] - 2026-09-11

Eigenständige, gekapselte Rückführung der portablen SentinelFleet-Race-Judge-
Konzepte (keine Übernahme von AGPL-Quellcode) sowie vollständige Pfad B
Discoverability-, Visual-Architecture- und Compliance-Erweiterung.

### Hinzugefügt

- **Visual Architecture & Dual Mermaid**: Umfassende Mermaid-Diagramme (`flowchart TD` für Systemarchitektur und `sequenceDiagram` für den End-to-End Renn- & Judge-Lebenszyklus) in `README.md` und `README_de.md`.
- **15-Punkte-Schnellnavigation**: Strukturierte Schnellnavigation mit 100% mutualer Ankerparität zwischen englischer und deutscher Dokumentation.
- **Governance- & Laufzeit-Invarianten (INV-LOCAL-01 bis INV-SLA-10)**: Verbindliche Architektur- und Sicherheitsregeln (Local-First, Zero-Egress, User-Mode, 6-Achsen-Attribution, Fail-Closed Judge, Prozessisolation, transparente Spur-Abrechnung, deskriptive Olympiaden-Trennung, permissive Lizenzen, 48h SLA).
- **Drittanbieter-Transparenz** (`THIRD_PARTY_LICENSES.md`): Vollständiges Lizenz-Audit aller Laufzeit- (`system-auditor` MIT, Python stdlib PSFL-2.0), optionalen (`coma` MIT) und Entwicklungs-Abhängigkeiten (`pytest` MIT, `ruff` MIT/Apache-2.0, `setuptools` MIT) mit 100% permissiver Garantie und Ausschluss von Copyleft/AGPL.
- **Marketing- & Discoverability-Register** (`MARKETING-LOG.txt`): Dokumentation von 4 Ziel-Personas, zweisprachigen Suchbegriffen, Wettbewerbsdifferenzierungs-Matrix und Governance-Zielen.
- **Geschwister-Ökosystem-Matrix**: Übersicht der Integration mit `ellmos-ai`, `dev-bricks`, `file-bricks`, `doc-bricks` und `open-bricks`.
- **Erweiterte Vertragstest-Suite** (`tests/test_metadata.py`): Neue Contract-Tests für Navigationsanker-Parität, kanonische Invarianten-IDs, Drittanbieter-Lizenzinventar und Personas im Marketing-Log.
- Global stabile `lane_id` je Modell × Variante × Wiederholung; doppelte
  Modellnamen werden zugunsten von `repeats` abgewiesen.
- Explizite Evidenzklassen in jedem RUN-Artefakt (`live`, `manual`, `simulated`,
  `blocked`, `failed`, `unknown`).
- `compare_race.judge`: fail-closed Aufnahmeprüfung, injektionsbewusster Judge-
  Prompt, optionaler echter Judge-Aufruf und separates `JUDGE.md`-Artefakt.
- CLI-Opt-in `compare-race run --judge [--judge-model NAME]`; der zusätzliche
  Modellaufruf ist nie implizit.

### Geändert

- **PEP 621 Metadaten in `pyproject.toml`**: Zusätzliche URLs für Third-Party Licenses, Marketing Log, Documentation, Security, Parent Organization und Umbrella Ecosystem.
- **LLM-Kontextdatei (`llms.txt`)**: Vollständige Synchronisation auf Version 0.7.0, 39 bestandene Tests, Laufzeit-Invarianten und Evidenz-Judge-Dokumentation.

### Sicherheit

- Simulierte, blockierte oder provenienzunklare Spuren werden nicht bewertet.
  Der Judge protokolliert stattdessen eine nicht ausgewertete Verweigerung.
- 100% Offline / Zero-Egress und unprivilegierte User-Mode-Ausführung (`RunAsInvoker`).

## [0.6.1] - 2026-09-10

Repository-Hygiene, CI-Matrix-Härtung, PEP 621 Metadaten und Vertragstest-Erweiterung (Pfad A).

### Hinzugefuegt

- **GitHub Actions CI Matrix Workflow** (`.github/workflows/ci.yml`): Automatisierte
  Tests über Python 3.10, 3.11 und 3.12 mit Bytecode-Kompilierung (`compileall`),
  Ruff-Linting und Pytest-Matrix.
- **Stale Workflow** (`.github/workflows/stale.yml`): Automatische Issue- und PR-Verwaltung
  nach Ökosystem-Standard.
- **Bilinguale Sicherheitsrichtlinie** (`SECURITY.md`): Definierte Grundsätze zur
  Prozessisolation (`lane_workdir`), Geheimnisschutz, 48h-Reaktions-SLA und 5-Tage-Triage.
- **Vertragstest-Suite** (`tests/test_metadata.py`): 6 automatisierte Contract-Tests für
  `.gitignore`-Hygiene, PEP 621 Struktur & URLs, CI-Matrix-Gültigkeit, README-Parität,
  SECURITY.md SLA sowie vollständiges Front-Matter-Roundtrip durch `system-auditor`.

### Geaendert

- **PEP 621 Paketmetadaten in `pyproject.toml`**: Umfassende Metadaten (`classifiers`,
  `keywords`, `urls` für Repository, Issues, Changelog und optionale `test`-Dependencies)
  sowie `addopts = "-v"` für Pytest ergänzt.
- **.gitignore-Härtung**: Schutzmuster gegen Multi-Host-Synchronisationskonflikte
  (`*-conflict-*`, `*.sync-temp-*`), Agent-Locks (`LOCK.*`, `*.lock`), temporäre Caches
  und Wheel-Smoke-Dateien.
- **Dokumentations-Synchronisation**: `README.md`, `README_de.md` und `llms.txt` auf Version
  0.6.1, 33 bestandene Tests und Sicherheitsrichtlinie aktualisiert.

## [0.6.0] - 2026-08-16

Fairness- und Forensik-Ausbau nach dem Erstlauf der Kant-Olympiade.

### Hinzugefuegt

- **lane_workdir** (Setting): run_race wechselt fuer die Dauer der Spawns in
  ein neutrales Verzeichnis -- gespawnte CLI-Spuren erben das cwd, ein
  Projekt-cwd leakte Hooks/Regeln/Judge-Dateien in eine Spur (Befund
  2026-08-16, Naivitaets-Klausel verletzt).
- **olympiade --timeout**: Spur-Timeout ueberschreibbar (der 300-s-Default
  warf Reasoning-Spuren als DNF; Nachmessung: 280/290/317 s fuer die drei
  tiefsten Antworten).
- **Lane-Logs** (`<races_dir>/_lane-logs/`): jeder Spur-Prozess schreibt
  stdout+stderr in eine eigene Log-Datei (COMA ``log_file``). Forensik-Basis:
  Ohne persistiertes Spur-Log ist post-hoc NICHT pruefbar, welche Werkzeuge
  eine Spur nutzte oder ob sie unerlaubt las -- die CLI-Agenten persistieren
  via COMA keine eigenen Transkripte (gemessen 2026-08-16). Rohmaterial fuer
  prompt-listener-artige Audits.

## [0.5.0] - 2026-08-16

Erste mitgelieferte Olympiade + per-Disziplin-Checks.

### Hinzugefuegt

- **Per-Disziplin-Checks im Olympiade-Modus:** `<stem>.checks.json` neben einer
  Task-Datei ersetzt die config-weiten Checks fuer genau diese Disziplin
  (gleiches Schema `[{"name","regex"}]`; kaputte Sidecars fallen mit Warnung
  auf die Config zurueck). Damit bekommt jede Disziplin ihre eigene
  deterministische Stufe der Auswertungs-Leiter.
- **Olympiade "Kantische Vernunft"** (`olympiads/kantische-vernunft/`): 8
  Disziplinen, destilliert aus dem Paper "Mensch in der Maschine" v9 (D1-D7 =
  die sieben Dimensionen des kantischen Tests, D8 = Distributional
  Rationality). Je Disziplin: self-contained Aufgaben-Prompt (`tasks/D*.md`),
  deterministische Regex-Checks (`tasks/D*.checks.json`, u. a.
  abschnittsgebundene ToM-Checks) und Judge-Anker (`JUDGE-RUBRIK.md`,
  bewusst getrennt von den Prompts). README uebernimmt den methodischen
  Vorbehalt des Papers: Kategoriensprung transzendental -> empirisch,
  Medaillenspiegel zaehlt und schliesst nicht.
- Tests: Sidecar-Vorrang/Fallback + Gold/Wrong-Antwortformen fuer die
  abschnittsgebundenen D6-Checks (25 Tests gesamt).

## [0.4.0] - 2026-08-16

Nutzerkonzept: drei Rennmodi entlang der Achsen.

### Hinzugefuegt

- **Sechste Achse `variant`** (wie die Aufgabe praesentiert wird: Wortlaut,
  Rolle, mitgegebene Skills, Umgebung) -- Task-Token bleibt die Strecke.
- **Twin/Clone-Modus** (`run --twin MODEL --variants-file v.json`): EIN Modell
  gegen sich selbst, nur die Variantenachse variiert -- der Einfluss von
  Prompt/Skills/Rolle wird kausal messbar; daraus lassen sich Regeln fuer
  gute Prompts und Skill-Mitgabe ableiten.
- **Olympiade** (`olympiade --tasks-dir ...`): mehrere Disziplinen (je
  Task-Datei ein Race, dort nur Modellachse = inferenziell), darueber ein
  DESKRIPTIVES Medaillenspiegel-Geruest (zaehlen, nicht schliessen -- dieselbe
  Abstufung wie die system-auditor-Aggregationsleiter).
- Achsen-Guard: Modelle UND Varianten zugleich -> uncontrolled-Warnung und
  Deskriptiv-Hinweis im Bericht.

## [0.3.0] - 2026-08-16

Nutzerklaerung eingearbeitet: Fairness braucht exakt gleiche Prompts, naive
Starts und nachpruefbare, moeglichst deterministische Auswertung.

### Hinzugefuegt

- **Deterministische Format-Checks** (`checks[]` in der Config, z. B.
  {name, regex}): mechanisch je Spur ausgewertet, BEVOR ein Judge-Urteil
  existiert; Ergebnis wandert in Front-Matter (`checks_passed/failed`) und
  Messtabelle. Jeder kann sie aus den Artefakten reproduzieren.
- **Auswertungs-Leiter dokumentiert** (deterministisch > belegt > subjektiv)
  und **Naivitaets-Klausel**: Spuren starten als frische Prozesse ohne
  Sessionkontext (coma-Spawn) -- der Judge ist kontextbeladen; selbst ein
  gleichnamiges Modell ist deshalb nie "derselbe" Teilnehmer.

## [0.2.1] - 2026-08-16

### Behoben

- **Kosten-Lookup nahm den Backend-Fallback vor der model-id:** Im grossen
  Rennen wurde die opus-Spur ueber das Backend "claude" auf die
  claude-fable-Rate gemappt. Die konfigurierte model-id der Spur gewinnt jetzt
  den Lookup (Regressionstest). Gefunden vom Judge beim Urteilen -- die
  Kosten-Rangfolge stimmte, die Rate nicht.

## [0.2.0] - 2026-08-16

### Hinzugefuegt

- **Kostenraten aus clutchs Getriebe-Katalog** (`costs.py`): erkannt, nie
  vorausgesetzt (getriebe_path/ENV/Konventionspfade); toleranter Lookup
  (Spurname 'gemini' findet 'gemini-3.7-flash'). `est_cost_usd` ist per
  Konstruktion eine SCHAETZUNG (Zeichen/4) und wird so ausgewiesen -- Kosten
  sind eine weitere Urteilsdimension neben der Stoppuhr.
- **Varianz-Block je Modell** im Report-Geruest, nur bei repeats > 1 (n=1
  wuerde Praezision vortaeuschen): n, ok-Quote, Latenz min/Oe/max,
  Output-Laengen-Spanne -- Streuung innerhalb einer Zeile ist Modell-Varianz,
  der Vergleich zwischen Zeilen gehoert dem Judge.
- **Mehr als zwei Spuren ausdruecklich vorgesehen:** Beispiel-Config mit vier
  Spuren (claude, codex, agy, kimi); `allow_unverified` als bewusster
  Per-Spur-Opt-in fuer comas kimi-Geruest.

## [0.1.0] - 2026-08-16

Erstanlage nach Entwurf `_control-center/_DECISIONS/ENTWURF_compare-race_2026-08-16.md`
(Freigabe User 2026-08-16; Judge-Default = Starter-Modell).

### Hinzugefuegt

- Fuenf-Achsen-Identitaet (time, prompt, system, model, run) -- wiederverwendete
  system-auditor-Logik (harte Dependency, Parser-Kompatibilitaet testgesichert).
- Zwei Modi: sequential (Stoppuhr, saubere Einzelmessung) und parallel (echtes
  Rennen); Kreuzprodukt Modelle x Wiederholungen.
- Ausfuehrung via COMA (erkannt, nie vorausgesetzt); modellmanueller Fallback
  `compare-race record`. Abstuerzende Spur kippt das Rennen nicht (ok: false).
- Report-Geruest mit Messtabelle, ehrlicher mechanischer Vorstufe (nur kategoriale
  Kurzantworten) und eingebetteter Judge-Rubrik: Qualitaet, Korrektheit,
  Vollstaendigkeit, Anweisungstreue, Latenz -- Zeit ist nur eine Dimension.
- Rollen-Prompt RACE-STARTER (DE+EN, P-006 Core), CLI (config|plan|run|record|report).
