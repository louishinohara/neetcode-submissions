#!/usr/bin/env python3
"""Regenerate dashboards/progress.md from problems.json + neetcode_map.json.

Exposes regenerate_dashboard() so add_problem.py can refresh the dashboard
after every log without spawning a subprocess.
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date
from pathlib import Path

# Allow `python scripts/dashboard.py` AND `from dashboard import ...`.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    DASHBOARDS_DIR,
    PROGRESS_FILE,
    load_activity,
    load_neetcode_map,
    load_problems,
    today,
)
from daily import (  # noqa: E402
    current_streak,
    group_by_date,
    longest_streak,
    recent_rows,
)


def render_table(rows: list[tuple[str, str]]) -> str:
    """Render a two-column markdown table; return a placeholder when empty."""
    if not rows:
        return "_(no data yet)_\n"
    header = "| Topic | Progress |\n| --- | --- |\n"
    body = "\n".join(f"| {topic} | {value} |" for topic, value in rows)
    return header + body + "\n"


def render_activity_table(rows: list[tuple[str, int, str]]) -> str:
    """Render the recent-activity table with a Date | # | Problems shape."""
    if not rows:
        return "_(no activity yet)_\n"
    header = "| Date | # | Problems |\n| --- | --- | --- |\n"
    body_lines = []
    for label, count, summary in rows:
        # Pipes inside problem titles would break the table; escape them.
        safe = summary.replace("|", "\\|")
        body_lines.append(f"| {label} | {count} | {safe} |")
    return header + "\n".join(body_lines) + "\n"


def progress_bar(done: int, total: int, width: int = 12) -> str:
    """Unicode progress bar like `████░░░░░░░░` 4/12 (33%)."""
    if total <= 0:
        return "—"
    pct = done / total
    filled = round(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"`{bar}` {done}/{total} ({pct * 100:.0f}%)"


def regenerate_dashboard() -> Path:
    """Rewrite dashboards/progress.md and return its path."""
    DASHBOARDS_DIR.mkdir(parents=True, exist_ok=True)
    problems = load_problems()
    nc_map = load_neetcode_map()

    done_ids = {p["id"] for p in problems if p.get("status") == "done"}
    total_logged = len(problems)
    total_done = len(done_ids)
    by_diff = Counter(
        p["difficulty"] for p in problems if p.get("status") == "done"
    )

    # NeetCode universe: every id listed in neetcode_map.json (deduped).
    nc_universe = {pid for pids in nc_map.values() for pid in pids}
    nc_done = len(done_ids & nc_universe)
    nc_total = len(nc_universe)
    nc_pct = (nc_done / nc_total * 100) if nc_total else 0.0

    # Per-roadmap-bucket progress for the headline table.
    nc_rows: list[tuple[str, str]] = []
    for topic, pids in sorted(nc_map.items()):
        d = sum(1 for pid in pids if pid in done_ids)
        nc_rows.append((topic, progress_bar(d, len(pids))))

    # Topics the user has actually logged solves under.
    own_topics = Counter(
        p["topic"] for p in problems if p.get("status") == "done"
    )
    logged_rows = [
        (topic, str(count))
        for topic, count in sorted(own_topics.items(), key=lambda kv: -kv[1])
    ]

    # Activity log: streaks + last-14-days table.
    events = load_activity()
    by_date = group_by_date(events)
    active = set(by_date.keys())
    today_d = date.today()
    cur_streak = current_streak(active, today_d)
    long_streak = longest_streak(active)
    rows_recent = recent_rows(by_date, problems, days=14, end=today_d)

    parts: list[str] = []
    parts.append("# DSA Progress\n")
    parts.append(f"_Last updated: {today()}_\n")
    parts.append("## Summary\n")
    parts.append(f"- Logged problems: **{total_logged}**")
    parts.append(f"- Solved: **{total_done}**")
    parts.append(
        "- Easy / Medium / Hard solved: "
        f"**{by_diff.get('easy', 0)} / "
        f"{by_diff.get('medium', 0)} / "
        f"{by_diff.get('hard', 0)}**"
    )
    parts.append(
        f"- NeetCode completion: **{nc_done}/{nc_total} ({nc_pct:.1f}%)**"
    )
    parts.append(
        f"- Current streak: **{cur_streak}** day{'s' if cur_streak != 1 else ''}"
    )
    parts.append(
        f"- Longest streak: **{long_streak}** day{'s' if long_streak != 1 else ''}"
    )
    parts.append(f"- Active days: **{len(active)}**\n")
    parts.append("## NeetCode roadmap\n")
    parts.append(render_table(nc_rows))
    parts.append("## Recent activity (last 14 days)\n")
    parts.append(render_activity_table(rows_recent))
    parts.append("## Logged solves by topic\n")
    parts.append(render_table(logged_rows))

    PROGRESS_FILE.write_text("\n".join(parts), encoding="utf-8")
    return PROGRESS_FILE


def main() -> None:
    path = regenerate_dashboard()
    print(f"wrote {path.relative_to(path.parent.parent)}")


if __name__ == "__main__":
    main()
