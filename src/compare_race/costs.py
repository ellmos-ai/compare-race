"""Cost rates per lane -- from clutch's gear catalogue, detected not assumed.

clutch ships a declarative model catalogue (``getriebe.json``: per gear a
``model_id``, ``kosten_input_1k``/``kosten_output_1k`` in USD per 1k tokens).
compare-race looks a lane's model up there and carries the *rate* into the run
header and the race table.

**Honesty rule:** CLI backends do not report token counts, so an exact cost is
unknowable here. What we can state is the rate, and an **estimate** derived
from character counts (chars/4 ≈ tokens) -- always labelled ``est_``, never
presented as a measurement. Time is one dimension of the verdict; cost is
another -- both belong in the table, both with their honest error bars.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

#: chars per token, the usual rough English/German average. An estimate flag
#: travels with every number derived from this.
_CHARS_PER_TOKEN = 4

_CONVENTION_PATHS = (
    Path(r"C:\_Local_DEV\repos\clutch\clutch\config\getriebe.json"),
    Path.home() / "OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/clutch/clutch/config/getriebe.json",
)


@dataclass(frozen=True)
class CostRate:
    gear: str
    model_id: str
    usd_in_per_1k: float
    usd_out_per_1k: float

    def estimate_usd(self, prompt_chars: int, output_chars: int) -> float:
        tokens_in = prompt_chars / _CHARS_PER_TOKEN
        tokens_out = output_chars / _CHARS_PER_TOKEN
        return round(
            tokens_in / 1000 * self.usd_in_per_1k + tokens_out / 1000 * self.usd_out_per_1k, 6
        )


def find_catalogue(explicit: str | Path | None = None) -> Path | None:
    """clutch is a neighbour: detected, never assumed."""
    if explicit:
        candidate = Path(explicit)
        return candidate if candidate.is_file() else None
    env = os.environ.get("CLUTCH_GETRIEBE")
    if env and Path(env).is_file():
        return Path(env)
    for candidate in _CONVENTION_PATHS:
        if candidate.is_file():
            return candidate
    return None


def load_rates(path: str | Path | None = None) -> dict[str, CostRate]:
    """Gear catalogue -> rates, keyed by gear name AND model_id (lowercased)."""
    found = find_catalogue(path)
    if found is None:
        return {}
    try:
        raw = json.loads(found.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}
    rates: dict[str, CostRate] = {}
    for gear, entry in (raw.get("gaenge") or {}).items():
        if not isinstance(entry, dict):
            continue
        try:
            rate = CostRate(
                gear=gear,
                model_id=str(entry.get("model_id", "")),
                usd_in_per_1k=float(entry.get("kosten_input_1k", 0) or 0),
                usd_out_per_1k=float(entry.get("kosten_output_1k", 0) or 0),
            )
        except (TypeError, ValueError):
            continue
        rates[gear.lower()] = rate
        if rate.model_id:
            rates[rate.model_id.lower()] = rate
    return rates


def rate_for(rates: dict[str, CostRate], *candidates: str) -> CostRate | None:
    """Tolerant lookup: exact gear/model_id first, then substring -- a lane
    named 'gemini' should still find 'gemini-3.7-flash'."""
    keys = [c.lower() for c in candidates if c]
    for key in keys:
        if key in rates:
            return rates[key]
    for key in keys:
        for known, rate in rates.items():
            if key in known or known in key:
                return rate
    return None


__all__ = ["CostRate", "find_catalogue", "load_rates", "rate_for"]
