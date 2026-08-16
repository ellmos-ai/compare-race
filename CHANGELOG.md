# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

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
