#!/usr/bin/env python3
"""Interactive CLI to log a DSA problem.

Creates problems/<topic>/<id>/{solution.py,notes.md}, then upserts the
record in data/problems.json. Re-running on an existing id increments
attempts and refreshes last_reviewed/status. Refreshes the dashboard
automatically so progress.md never goes stale.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow sibling imports (`_common`, `dashboard`) when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    NOTES_TEMPLATE,
    PROBLEMS_DIR,
    PROJECT_ROOT,
    SOLUTION_TEMPLATE,
    VALID_DIFFICULTIES,
    VALID_STATUSES,
    append_activity,
    find_problem,
    load_problems,
    save_problems,
    slugify,
    today,
)
from dashboard import regenerate_dashboard  # noqa: E402


def prompt(
    question: str,
    default: str | None = None,
    choices: tuple[str, ...] | None = None,
) -> str:
    """Prompt with optional default and constrained choices; loop until valid."""
    suffix = ""
    if choices:
        suffix = f" ({'/'.join(choices)})"
    if default is not None:
        suffix += f" [{default}]"
    while True:
        raw = input(f"{question}{suffix}: ").strip()
        if not raw and default is not None:
            raw = default
        if not raw:
            print("  value required")
            continue
        if choices and raw not in choices:
            print(f"  must be one of: {', '.join(choices)}")
            continue
        return raw


def parse_bool(raw: str) -> bool:
    """Accept y/yes/true/1 (case-insensitive) as truthy."""
    return raw.lower() in ("y", "yes", "true", "1")


def add_problem() -> dict:
    """Run the interactive flow and persist the record. Returns the record."""
    title = prompt("Title")
    topic = prompt("Topic", default="arrays").lower()
    pattern_raw = prompt("Pattern (comma-separated, optional)", default="")
    difficulty = prompt(
        "Difficulty", default="medium", choices=VALID_DIFFICULTIES
    )
    neetcode = parse_bool(
        prompt("NeetCode?", default="y", choices=("y", "n"))
    )
    status = prompt("Status", default="done", choices=VALID_STATUSES)

    pid = slugify(title)
    patterns = [p.strip() for p in pattern_raw.split(",") if p.strip()]

    folder = PROBLEMS_DIR / topic / pid
    folder.mkdir(parents=True, exist_ok=True)

    solution_path = folder / "solution.py"
    notes_path = folder / "notes.md"

    # Don't clobber existing solution/notes when re-logging an attempt.
    if not solution_path.exists():
        solution_path.write_text(
            SOLUTION_TEMPLATE.format(
                title=title,
                difficulty=difficulty,
                topic=topic,
                patterns=", ".join(patterns) or "-",
            ),
            encoding="utf-8",
        )
    if not notes_path.exists():
        notes_path.write_text(
            NOTES_TEMPLATE.format(title=title), encoding="utf-8"
        )

    problems = load_problems()
    existing = find_problem(problems, pid)

    record = {
        "id": pid,
        "title": title,
        "topic": topic,
        "pattern": patterns,
        "difficulty": difficulty,
        "neetcode": neetcode,
        "status": status,
        "attempts": (existing["attempts"] + 1) if existing else 1,
        "last_reviewed": today(),
        "notes_path": notes_path.relative_to(PROJECT_ROOT).as_posix(),
        "solution_path": solution_path.relative_to(PROJECT_ROOT).as_posix(),
    }

    if existing:
        existing.update(record)
    else:
        problems.append(record)

    save_problems(problems)
    append_activity(
        {
            "date": today(),
            "id": pid,
            "status": status,
            "attempt": record["attempts"],
        }
    )
    regenerate_dashboard()

    action = "updated" if existing else "added"
    rel = folder.relative_to(PROJECT_ROOT).as_posix()
    print(f"\n  {action} {pid} ({topic}/{difficulty}) -> {rel}")
    return record


if __name__ == "__main__":
    try:
        add_problem()
    except (KeyboardInterrupt, EOFError):
        # Exit cleanly on Ctrl-C / Ctrl-D so partial state is not surprising.
        print("\naborted")
        sys.exit(130)
