# Security Policy / Sicherheitsrichtlinie

## Supported Versions / Unterstützte Versionen

| Version | Supported / Unterstützt |
| ------- | ----------------------- |
| 0.6.x   | :white_check_mark:      |
| < 0.6   | :x:                     |

---

## English Security Policy

### Core Security & Process Isolation Principles

`compare-race` executes benchmark and arbitration prompts across multiple language model backends. It is built with rigorous process isolation and local execution standards:

1. **Local Execution & Naivety Guard:**
   - Prompt races run locally or against configured user endpoints without third-party telemetry, tracking, or unexpected background network egress.
   - When configured with `lane_workdir`, spawned CLI lane subprocesses are strictly isolated into a designated working directory to prevent leaking repository hooks, instructions, or evaluation criteria into the model's runtime context.

2. **Credential & Secret Protection:**
   - Model API keys and credentials are read exclusively from user environment variables or local ignored config files (`compare-race.config.json`).
   - Secrets and session tokens are never committed to version control and are explicitly listed in `.gitignore`.

3. **Deterministic Evaluation:**
   - Mechanical format checks and evaluation rubrics operate deterministically on local output artifacts.

### Reporting a Vulnerability

If you discover a security vulnerability in `compare-race`, please report it privately:

1. **GitHub Security Advisory (Preferred):** Open a private advisory at [ellmos-ai/compare-race Security Advisories](https://github.com/ellmos-ai/compare-race/security/advisories).
2. **Email Contacts:** Send details to `security@open-bricks.org` and `security@ellmos.ai` (CC: `lukas@open-bricks.org`, `support@lukasgeiger.com`).

**Service Level Agreement (SLA):**
- **Acknowledgment:** Within 48 hours.
- **Triage & Status Assessment:** Within 5 business days.
- **Remediation & Release Coordination:** As rapidly as verified testing permits.

Please do not disclose potential vulnerabilities publicly in issues or pull requests.

---

## Deutsche Sicherheitsrichtlinie (German)

### Sicherheits- und Prozessisolationsgrundsätze

`compare-race` führt Benchmark- und Schiedsrichter-Prompts über mehrere Sprachmodell-Spuren aus. Das Modul folgt strikten Grundsätzen der Prozessisolation und des Datenschutzes:

1. **Lokale Ausführung & Naivitäts-Schutz:**
   - Prompts werden lokal oder über direkt vom Nutzer konfigurierte Endpunkte abgewickelt, ohne Drittanbieter-Telemetrie oder unautorisierte Netzwerkabflüsse.
   - Durch das `lane_workdir`-System können gespawnte CLI-Kindprozesse in neutrale Arbeitsverzeichnisse isoliert werden, um ein Auslesen von Projekt-Hooks oder Testrubriken zuverlässig zu verhindern.

2. **Schutz von Anmeldedaten und Schlüsseln:**
   - API-Schlüssel werden ausschließlich aus lokalen Umgebungsvariablen oder lokalen Konfigurationsdateien (`compare-race.config.json`) geladen.
   - Vertrauliche Dateien und Umgebungsvariablen sind durch `.gitignore` vor unbeabsichtigtem Commit geschützt.

3. **Deterministische Artefaktauswertung:**
   - Mechanische Formatprüfungen und Auswertungen erfolgen direkt und deterministisch auf den gespeicherten Textartefakten.

### Sicherheitslücke melden

Wenn Sie eine Sicherheitslücke entdecken, melden Sie diese bitte vertraulich:

1. **GitHub Security Advisory (Bevorzugt):** Erstellen Sie einen privaten Bericht unter [ellmos-ai/compare-race Security Advisories](https://github.com/ellmos-ai/compare-race/security/advisories).
2. **E-Mail-Kontakt:** Senden Sie Ihren Bericht an `security@open-bricks.org` und `security@ellmos.ai` (CC: `lukas@open-bricks.org`, `support@lukasgeiger.com`).

**Verbindliche Reaktionsfristen:**
- **Eingangsbestätigung:** Innerhalb von 48 Stunden.
- **Ersteinschätzung (Triage):** Innerhalb von 5 Werktagen.
- **Behebung:** Nach erfolgreicher Verifikation in der Testsuite.
