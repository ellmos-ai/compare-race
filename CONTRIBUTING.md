# Contributing to compare-race / Mitwirken an compare-race

Welcome! We welcome contributions to `compare-race`. To maintain benchmark determinism, reproducible model timing, evidence-grounded judging, and compliance across multi-host environments, all contributions must adhere to the quality standards and operational invariants defined below.

---

## English

### 1. General Principles & Quality Gates
1. **Local-First & Air-Gapped (`INV-LOCAL-01`)**: All core library and CLI logic must operate strictly offline by default. Never introduce hidden telemetry, outbound analytics sockets, or background data transmission.
2. **User-Mode Non-Elevation (`INV-SEC-02` / `RunAsInvoker`)**: Core benchmarking, token hashing, process timing, and starter-judge evaluation must execute without administrative elevation or UAC prompts.
3. **Six-Axis Attribution Discipline (`INV-AXIS-03`)**: Runs are identified by the canonical identity tuple `time · prompt · system · model · run · variant`. Attributes must only vary on intended dimensions.
4. **Evidence-Aware Fail-Closed Judge (`INV-JUDGE-04`)**: The starter judge only evaluates lanes backed by live-executed or model-manually recorded evidence (`ok: true`, valid provenance). Unverified or simulated lanes must result in an explicit refusal.
5. **Version Freeze Discipline (`T-20260920-167562623`)**: Version 0.7.2 is strictly frozen across all manifests. Do not bump the version string. Document all advancements under `## [Unreleased]` in `CHANGELOG.md`.
6. **Clean Code & Regression Testing**: Every feature or fix must include regression tests in `tests/`. Keep test coverage at 100% pass rate.
7. **Bilingual Parity**: Maintain synchronized structural and navigational parity across `README.md` and `README_de.md` (18-point dual anchors `sec-01` through `sec-18`).

### 2. Local Development Workflow
```bash
# Install package with development dependencies
python -m pip install -e ".[test]"

# Run comprehensive test suite
python -X utf8 -m pytest -ra -v

# Run linter
python -m ruff check .

# Check bytecode compilation
python -m compileall -q .

# Check whitespace and git diff cleanliness
git diff --check
```

### 3. Submission Protocol
- Open an issue for behavioral discussions before large refactoring.
- Keep provider API keys, bearer tokens, and private credentials strictly outside the repository.
- Ensure all 10 governance invariants (`INV-LOCAL-01` to `INV-SLA-10`) remain VERIFIED.

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore
1. **Local-First & Zero-Egress (`INV-LOCAL-01`)**: Sämtliche Kernbibliotheken und CLI-Abläufe arbeiten standardmäßig zu 100% offline ohne Telemetrie, Sockets oder externe Datenübertragung.
2. **User-Mode Non-Elevation (`INV-SEC-02` / `RunAsInvoker`)**: Benchmarking, Token-Hashing, Zeitmessung und Starter-Judge-Evaluation laufen strikt im unprivilegierten Standard-Benutzerkontext ohne UAC-Elevation.
3. **Sechs-Achsen-Attributionsdisziplin (`INV-AXIS-03`)**: Läufe werden über das kanonische Identitätstupel `Zeit · Prompt · System · Modell · Lauf · Variante` abgebildet.
4. **Beweisbasierter Fail-Closed Judge (`INV-JUDGE-04`)**: Der Starter-Judge wertet nur Bahnen mit nachgewiesener Live-Ausführung oder manueller Erfassung aus. Unbewiesene oder simulierte Bahnen führen zu einer expliziten Verweigerung.
5. **Strikte Versions-Freeze-Disziplin (`T-20260920-167562623`)**: Version 0.7.2 bleibt in allen Manifesten eingefroren. Keine Versionserhöhung vornehmen; alle Änderungen unter `## [Unreleased]` in `CHANGELOG.md` festhalten.
6. **Testabdeckung & Regressionstests**: Für jede Verhaltensänderung ist ein Vertragstest in `tests/` zu ergänzen. Die Testsuite muss zu 100% grün bleiben.
7. **Zweisprachige Dokumentationsparität**: `README.md` und `README_de.md` müssen strukturgleich und mit synchronen 18-Punkte-HTML-Ankern (`sec-01` bis `sec-18`) gepflegt werden.

### 2. Lokaler Entwicklungsablauf
```bash
# Entwicklungsumgebung einrichten
python -m pip install -e ".[test]"

# Vollständige Testsuite ausführen
python -X utf8 -m pytest -ra -v

# Linter-Prüfung
python -m ruff check .

# Bytecode-Kompilierung
python -m compileall -q .

# Diff- und Whitespace-Prüfung
git diff --check
```

### 3. Einreichung
- Vor größeren Eingriffen ein Issue zur Abstimmung anlegen.
- LLM-API-Schlüssel, Zugriffstoken und temporäre Renn-Ergebnisse niemals ins Repository committen.
- Alle 10 Invarianten (`INV-LOCAL-01` bis `INV-SLA-10`) müssen erfüllt bleiben.
