"""Race configuration -- read for real, defaults with a stated reason.

Follows the system-auditor config discipline: comment keys are data, a broken
file yields defaults plus the reason, and the file never half-applies.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_FILENAME = "compare-race.config.json"
HOME_PLACEHOLDER = "<HOME>"

#: The judge default is the STARTER: the model that starts the race writes the
#: verdict (user decision 2026-08-16). A fixed judge model is a config choice.
JUDGE_STARTER = "starter"


@dataclass
class ModelEntry:
    """One lane of the race."""

    name: str  # identity token, e.g. "opus-5", "codex", "gemini-3.7-flash"
    backend: str  # coma adapter: claude | codex | agy | kimi
    model: str = ""  # per-call model override for the adapter, "" = adapter default
    #: COMA refuses unverified adapters (today: kimi) unless told otherwise --
    #: a per-lane, deliberate opt-in, never a global default.
    allow_unverified: bool = False


@dataclass
class RaceSettings:
    system: str = ""
    races_dir: str = ""
    mode: str = "sequential"  # stopwatch by default: clean per-model timing
    repeats: int = 1
    judge: str = JUDGE_STARTER
    max_parallel: int = 3
    timeout_seconds: int = 600
    #: clutch gear catalogue for cost rates -- detected, never assumed.
    getriebe_path: str = ""
    #: Deterministic format checks, evaluated mechanically per lane BEFORE any
    #: judge opinion: [{"name": ..., "regex": ...}]. A check passes when
    #: re.search matches the output. Reproducible by anyone from the artefacts.
    checks: list[dict] = field(default_factory=list)
    models: list[ModelEntry] = field(default_factory=list)
    source: str = "defaults"
    notes: list[str] = field(default_factory=list)

    def model_names(self) -> list[str]:
        return [entry.name for entry in self.models]


def find_config(explicit: str | Path | None = None) -> Path | None:
    if explicit:
        candidate = Path(explicit)
        return candidate if candidate.is_file() else None
    env = os.environ.get("COMPARE_RACE_CONFIG")
    if env and Path(env).is_file():
        return Path(env)
    for candidate in (
        Path.cwd() / DEFAULT_FILENAME,
        Path.cwd() / "config" / DEFAULT_FILENAME,
        Path.home() / ".compare-race" / DEFAULT_FILENAME,
    ):
        if candidate.is_file():
            return candidate
    return None


def load(path: str | Path | None = None, home: str | None = None) -> RaceSettings:
    resolved_home = home or str(Path.home()).replace("\\", "/")
    found = find_config(path)
    if found is None:
        return RaceSettings(notes=["no config file found -- running on defaults"])
    try:
        raw = json.loads(found.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return RaceSettings(
            source=str(found),
            notes=[f"config unreadable ({exc.__class__.__name__}) -- running on defaults"],
        )

    data = {k: v for k, v in raw.items() if not k.startswith("_comment")}
    notes: list[str] = []

    mode = str(data.get("mode", "sequential"))
    if mode not in ("sequential", "parallel"):
        notes.append(f"mode {mode!r} rejected -- using sequential (stopwatch)")
        mode = "sequential"

    models = [
        ModelEntry(
            name=str(entry.get("name", "")),
            backend=str(entry.get("backend", "")),
            model=str(entry.get("model", "")),
            allow_unverified=bool(entry.get("allow_unverified", False)),
        )
        for entry in data.get("models") or []
        if isinstance(entry, dict) and entry.get("name") and entry.get("backend")
    ]
    if not models:
        notes.append("no usable models[] -- plan/run need at least one lane")

    settings = RaceSettings(
        system=str(data.get("system", "")),
        races_dir=str(data.get("races_dir", "")).replace(HOME_PLACEHOLDER, resolved_home),
        mode=mode,
        repeats=max(1, int(data.get("repeats", 1) or 1)),
        judge=str(data.get("judge", JUDGE_STARTER)) or JUDGE_STARTER,
        max_parallel=max(1, int(data.get("max_parallel", 3) or 3)),
        timeout_seconds=max(1, int(data.get("timeout_seconds", 600) or 600)),
        getriebe_path=str(data.get("getriebe_path", "")).replace(HOME_PLACEHOLDER, resolved_home),
        checks=[
            entry for entry in data.get("checks") or []
            if isinstance(entry, dict) and entry.get("name") and entry.get("regex")
        ],
        models=models,
        source=str(found),
        notes=notes,
    )
    if settings.system in ("", "<HOSTNAME>"):
        settings.notes.append(
            "system is unset -- runs would carry an identity no other machine recognises"
        )
    if settings.races_dir and "onedrive" not in settings.races_dir.lower() and not any(
        hint in settings.races_dir.lower()
        for hint in ("dropbox", "nextcloud", "syncthing", "icloud", ".sync")
    ):
        settings.notes.append(
            "races_dir looks host-local -- cross-machine series need a shared folder "
            "(fine for single-host races)"
        )
    return settings


__all__ = ["JUDGE_STARTER", "ModelEntry", "RaceSettings", "find_config", "load"]
