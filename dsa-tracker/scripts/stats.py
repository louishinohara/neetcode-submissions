#!/usr/bin/env python3
"""Print progress stats for the DSA tracker.

Reads data/problems.json plus data/neetcode_map.json (used as the
canonical denominator for NeetCode completion %) and prints a summary.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import load_neetcode_map, load_problems  # noqa: E402


def topic_completion(
    problems: list[dict], neetcode_map: dict[str, list[str]]
) -> dict[str, tuple[int, int]]:
    """Return {map_topic: (done_count, total_count)} keyed by roadmap bucket."""
    done_ids = {p["id"] for p in problems if p.get("status") == "done"}
    return {
        topic: (sum(1 for pid in pids if pid in done_ids), len(pids))
        for topic, pids in neetcode_map.items()
    }


def main() -> None:
    problems = load_problems()
    nc_map = load_neetcode_map()

    total = len(problems)
    done = sum(1 for p in problems if p.get("status") == "done")
    by_topic = Counter(p["topic"] for p in problems)
    by_difficulty = Counter(p["difficulty"] for p in problems)
    by_status = Counter(p["status"] for p in problems)

    nc_universe = {pid for pids in nc_map.values() for pid in pids}
    nc_done_ids = {
        p["id"]
        for p in problems
        if p.get("status") == "done" and p["id"] in nc_universe
    }
    nc_pct = (len(nc_done_ids) / len(nc_universe) * 100) if nc_universe else 0.0

    print("=== DSA Tracker stats ===")
    print(f"Logged problems    : {total}")
    print(f"Solved (done)      : {done}")
    print(f"By status          : {dict(by_status)}")
    print(f"By difficulty      : {dict(by_difficulty)}")
    print(
        "NeetCode completion: "
        f"{len(nc_done_ids)}/{len(nc_universe)} ({nc_pct:.1f}%)"
    )

    print("\nBy topic (logged):")
    for topic, count in sorted(by_topic.items(), key=lambda kv: -kv[1]):
        print(f"  {topic:25s} {count}")

    if nc_map:
        completion = topic_completion(problems, nc_map)
        # Weakest = lowest done/total ratio. Tie-break by largest bucket so
        # the gap that costs the most points wins.
        weakest = min(
            completion.items(),
            key=lambda kv: (
                (kv[1][0] / kv[1][1]) if kv[1][1] else 1.0,
                -kv[1][1],
            ),
        )
        topic, (d, t) = weakest
        ratio = (d / t * 100) if t else 0.0
        print(f"\nWeakest NeetCode topic: {topic} ({d}/{t} = {ratio:.0f}%)")


if __name__ == "__main__":
    main()
