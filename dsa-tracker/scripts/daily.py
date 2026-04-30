#!/usr/bin/env python3
"""Daily activity log: which problems were worked on each day, plus streaks.

Reads data/activity.json (an append-only event log written by add_problem.py)
and prints a recent-days view + current/longest streak so you can spot
inconsistency at a glance.

Examples:
    python scripts/daily.py
    python scripts/daily.py --days 30
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import load_activity, load_problems  # noqa: E402


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def group_by_date(events: list[dict]) -> dict[date, list[dict]]:
    """Bucket events by their date field."""
    by_date: dict[date, list[dict]] = defaultdict(list)
    for ev in events:
        by_date[parse_date(ev["date"])].append(ev)
    return by_date


def longest_streak(active: set[date]) -> int:
    """Length of the longest run of consecutive active days."""
    if not active:
        return 0
    sorted_days = sorted(active)
    longest = run = 1
    for prev, cur in zip(sorted_days, sorted_days[1:]):
        if (cur - prev).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    return longest


def current_streak(active: set[date], anchor: date) -> int:
    """Streak ending on `anchor`. If `anchor` is empty but the day before
    is active, the streak is still considered alive (so logging early in
    the day before you have practiced doesn't show 0)."""
    if not active:
        return 0
    d = anchor
    if d not in active:
        d -= timedelta(days=1)
        if d not in active:
            return 0
    streak = 0
    while d in active:
        streak += 1
        d -= timedelta(days=1)
    return streak


def recent_rows(
    by_date: dict[date, list[dict]],
    problems: list[dict],
    days: int,
    end: date,
) -> list[tuple[str, int, str]]:
    """Build per-day rows for the last `days` ending on `end` (inclusive).

    Returns [(date_label, problem_count, summary_str), ...] newest-first.
    Multiple events for the same problem on the same day collapse into one
    entry (the last one wins, which is what we want for status updates).
    """
    pid_to_title = {p["id"]: p.get("title", p["id"]) for p in problems}
    rows: list[tuple[str, int, str]] = []
    for i in range(days):
        d = end - timedelta(days=i)
        label = f"{d.isoformat()} ({d.strftime('%a')})"
        events = by_date.get(d, [])
        if not events:
            rows.append((label, 0, "—"))
            continue
        seen: dict[str, dict] = {}
        for ev in events:
            seen[ev["id"]] = ev
        parts = [
            f"{pid_to_title.get(pid, pid)} ({ev.get('status', '?')})"
            for pid, ev in seen.items()
        ]
        rows.append((label, len(seen), ", ".join(parts)))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily DSA activity log.")
    parser.add_argument(
        "--days", type=int, default=14, help="How many days of history to show"
    )
    args = parser.parse_args()

    events = load_activity()
    problems = load_problems()
    by_date = group_by_date(events)
    active = set(by_date.keys())
    today_d = date.today()

    cur = current_streak(active, today_d)
    longest = longest_streak(active)

    print("=== Daily activity ===")
    print(f"Current streak     : {cur} day{'s' if cur != 1 else ''}")
    print(f"Longest streak     : {longest} day{'s' if longest != 1 else ''}")
    print(f"Total active days  : {len(active)}")
    print(f"Total log entries  : {len(events)}")
    print()
    print(f"Last {args.days} days:")
    for label, count, summary in recent_rows(by_date, problems, args.days, today_d):
        mark = "●" if count else "·"
        if count:
            print(f"  {label}  {mark}  {count} problem{'s' if count != 1 else ''}  {summary}")
        else:
            print(f"  {label}  {mark}")


if __name__ == "__main__":
    main()
