"""Shared utilities for DSA tracker scripts.

Centralizes filesystem paths, JSON IO, and the solution/notes templates so
the per-command scripts (add_problem, stats, filter, dashboard) stay small.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

# Anchor every path to the project root so scripts work from any cwd.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROBLEMS_DIR = PROJECT_ROOT / "problems"
DASHBOARDS_DIR = PROJECT_ROOT / "dashboards"

PROBLEMS_FILE = DATA_DIR / "problems.json"
NEETCODE_MAP_FILE = DATA_DIR / "neetcode_map.json"
ACTIVITY_FILE = DATA_DIR / "activity.json"
PROGRESS_FILE = DASHBOARDS_DIR / "progress.md"

VALID_DIFFICULTIES: tuple[str, ...] = ("easy", "medium", "hard")
VALID_STATUSES: tuple[str, ...] = ("todo", "in-progress", "done")


NOTES_TEMPLATE = """# {title}

## Pattern
-

## Key Insight
-

## Mistake
-

## Optimal Solution
-

## Time / Space Complexity
-

## Revisit
-
"""


SOLUTION_TEMPLATE = '''"""
{title}
Difficulty: {difficulty}
Topic: {topic}
Pattern(s): {patterns}

See notes.md in this directory for analysis.
"""


class Solution:
    # TODO: implement
    pass
'''


def slugify(text: str) -> str:
    """Convert a problem title to a filesystem- and JSON-safe id."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def today() -> str:
    """ISO-formatted today, used for the last_reviewed timestamp."""
    return date.today().isoformat()


def load_problems() -> list[dict[str, Any]]:
    """Read problems.json, returning [] if it does not yet exist."""
    if not PROBLEMS_FILE.exists():
        return []
    with PROBLEMS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_problems(problems: list[dict[str, Any]]) -> None:
    """Write problems.json with stable indentation."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with PROBLEMS_FILE.open("w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2)
        f.write("\n")


def load_neetcode_map() -> dict[str, list[str]]:
    """Read neetcode_map.json, returning {} if it does not yet exist."""
    if not NEETCODE_MAP_FILE.exists():
        return {}
    with NEETCODE_MAP_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_problem(
    problems: list[dict[str, Any]], pid: str
) -> dict[str, Any] | None:
    """Return the first record with matching id, or None."""
    for p in problems:
        if p.get("id") == pid:
            return p
    return None


def load_activity() -> list[dict[str, Any]]:
    """Read activity.json (the daily log), returning [] if missing."""
    if not ACTIVITY_FILE.exists():
        return []
    with ACTIVITY_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_activity(events: list[dict[str, Any]]) -> None:
    """Write activity.json with stable indentation."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with ACTIVITY_FILE.open("w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
        f.write("\n")


def append_activity(event: dict[str, Any]) -> None:
    """Append a single event to the daily log (kept append-only)."""
    events = load_activity()
    events.append(event)
    save_activity(events)
