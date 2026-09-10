# Release Gate: compare-race

## Status

```
+------------------------------------------+
|                                          |
|          STATUS: UNLOCKED                |
|                                          |
+------------------------------------------+
```

> **LOCKED** = Repository must remain private.
> **UNLOCKED** = Repository may be set to public.

---

## Current local verification — 2026-09-05

- Package and CLI version: **0.6.0**.
- Test suite: **27 passed**; Ruff and `compileall` clean.
- The `lane_workdir` compatibility path and cwd restoration were verified with
  **Python 3.10.20**, including restoration after an exception.
- Version 0.6 includes twin/clone variants and persisted raw lane logs. This
  verification updates the repository record; it is not a new release or publication.

---

## Gate run 2026-08-16

`final_gate_check.py --repo-path .` → **10 PASS, 0 FAIL, 0 WARN — exit 0**
(process `MODULES/RELEASE_PROCESS.md` v1.0)

| # | Check | Result |
|---|-------|--------|
| 1 | `.gitignore` minimum entries | PASS |
| 2 | `README.md` present, English | PASS |
| 3 | `LICENSE` (MIT) | PASS |
| 4 | No `.db` tracked | PASS |
| 5 | No `.env` tracked | PASS |
| 6 | No secret patterns | PASS |
| 7 | No hardcoded personal paths | PASS |
| 8 | No PII patterns | PASS |
| 9 | No BACH-internal documents | PASS |
| 10 | `TODO.md` with STATUS table | PASS |

## Notes

- Language decision (binding rule 4): core docs bilingual DE/EN (README, role
  prompt); CHANGELOG/TODO deliberately German as internal work journal —
  recorded in `TODO.md` STATUS table.
- Hard dependency `system-auditor` is public (github.com/ellmos-ai/system-auditor);
  COMA is detected, never assumed.
- Verified by a real race before release: codex + gemini (agy), sequential,
  both lanes green, model-manual verdict filed.
- Historical test suite at gate time: 9 passed · ruff clean.
- Reviewed by: Claude Code (fable-5), 2026-08-16 — identity corrected same day: the session ran as Fable 5, the earlier opus-5 signature came from a stale self-description
