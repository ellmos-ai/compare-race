# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

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
