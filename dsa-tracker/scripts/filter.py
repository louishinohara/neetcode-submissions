#!/usr/bin/env python3
"""Filter logged problems by status, topic, pattern, difficulty, or neetcode.

Examples:
    python scripts/filter.py --unsolved
    python scripts/filter.py --topic graphs
    python scripts/filter.py --pattern hashing
    python scripts/filter.py --difficulty hard --status done
    python scripts/filter.py --neetcode y --status todo
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import VALID_DIFFICULTIES, VALID_STATUSES, load_problems  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Filter DSA problems.")
    p.add_argument("--status", choices=VALID_STATUSES)
    p.add_argument("--topic", help="Exact topic match (e.g. arrays)")
    p.add_argument("--pattern", help="Match if listed in a problem's pattern[]")
    p.add_argument("--difficulty", choices=VALID_DIFFICULTIES)
    p.add_argument(
        "--unsolved",
        action="store_true",
        help="Shortcut: show anything not in 'done' status",
    )
    p.add_argument(
        "--neetcode",
        choices=("y", "n"),
        help="Filter by NeetCode flag",
    )
    return p


def matches(problem: dict, args: argparse.Namespace) -> bool:
    """Return True iff `problem` satisfies every flag the user passed."""
    if args.unsolved and problem.get("status") == "done":
        return False
    if args.status and problem.get("status") != args.status:
        return False
    if args.topic and problem.get("topic") != args.topic:
        return False
    if args.difficulty and problem.get("difficulty") != args.difficulty:
        return False
    if args.pattern and args.pattern not in (problem.get("pattern") or []):
        return False
    if args.neetcode is not None:
        want = args.neetcode == "y"
        if bool(problem.get("neetcode")) != want:
            return False
    return True


def main() -> None:
    args = build_parser().parse_args()
    problems = load_problems()
    matching = [p for p in problems if matches(p, args)]

    if not matching:
        print("(no matches)")
        return

    print(f"{len(matching)} problem(s):\n")
    for p in matching:
        patt = ",".join(p.get("pattern") or []) or "-"
        nc = "NC" if p.get("neetcode") else "  "
        print(
            f"  [{p['status']:<11}] {nc} {p['difficulty']:<6} "
            f"{p['topic']:<15} {p['title']}  ({patt})"
        )


if __name__ == "__main__":
    main()
