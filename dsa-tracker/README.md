# DSA Tracker

A minimal, dependency-free CLI to log every LeetCode / NeetCode problem you
solve, store its solution + notes, and surface the topics you are weakest on.
The goal: logging a problem takes under 30 seconds.

## Layout

```
dsa-tracker/
├── data/
│   ├── problems.json          # source of truth for what you have logged
│   ├── neetcode_map.json      # canonical NeetCode roadmap buckets
│   └── activity.json          # append-only daily log (one event per add)
├── problems/
│   └── {topic}/{id}/
│       ├── solution.py
│       └── notes.md
├── scripts/
│   ├── _common.py             # shared paths / IO / templates
│   ├── add_problem.py         # interactive logging
│   ├── stats.py               # progress summary
│   ├── filter.py              # query logged problems
│   ├── daily.py               # daily activity log + streaks
│   └── dashboard.py           # regenerate dashboards/progress.md
├── dashboards/
│   └── progress.md
└── README.md
```

## Requirements

- Python 3.10+ (uses `list[int]` / `X | None` syntax)
- No third-party packages

## Usage

All scripts are anchored to the project root, so they work from any cwd.

### Log a problem (target: < 30s)

```bash
python scripts/add_problem.py
```

Prompts for title, topic, pattern(s), difficulty, NeetCode flag, status.
Each prompt has a sensible default — just press Enter to accept.

The script then:

1. Creates `problems/<topic>/<id>/{solution.py, notes.md}` from the templates.
2. Upserts the record in `data/problems.json`.
3. Regenerates `dashboards/progress.md`.

Re-running on an existing title increments `attempts` and refreshes
`last_reviewed` + `status` without overwriting your solution or notes.

### See where you stand

```bash
python scripts/stats.py
```

Prints total / by-status / by-difficulty / by-topic counts, NeetCode
completion %, and your weakest NeetCode roadmap bucket.

### Find what to work on next

```bash
python scripts/filter.py --unsolved
python scripts/filter.py --topic graphs
python scripts/filter.py --pattern hashing
python scripts/filter.py --difficulty hard --status done
python scripts/filter.py --neetcode y --status todo
```

### See your daily load + streak

```bash
python scripts/daily.py             # last 14 days
python scripts/daily.py --days 30   # last 30 days
```

Each `add_problem.py` run appends one event to `data/activity.json` (the
append-only daily log). `daily.py` reads it and prints current streak,
longest streak, total active days, plus a per-day list of what you
worked on. The same view is mirrored in `dashboards/progress.md`.

The current-streak rule is intentionally lenient: if you haven't logged
**today** but you logged **yesterday**, the streak is still alive. It
only resets after a full day of inactivity, so checking the dashboard
in the morning before practice doesn't show 0.

### Refresh the dashboard manually

```bash
python scripts/dashboard.py
```

Normally unnecessary — `add_problem.py` calls this for you on every log.

## Data model

Each entry in `data/problems.json` follows:

```json
{
  "id": "contains_duplicate",
  "title": "Contains Duplicate",
  "topic": "arrays",
  "pattern": ["hashing"],
  "difficulty": "easy",
  "neetcode": true,
  "status": "done",
  "attempts": 1,
  "last_reviewed": "YYYY-MM-DD",
  "notes_path": "problems/arrays/contains_duplicate/notes.md",
  "solution_path": "problems/arrays/contains_duplicate/solution.py"
}
```

Allowed values:

- `difficulty`: `easy` | `medium` | `hard`
- `status`: `todo` | `in-progress` | `done`
- `neetcode`: `true` | `false`
- `pattern`: array of free-form strings (e.g. `hashing`, `sliding_window`)

## Extending

- Add roadmap buckets / problem ids to `data/neetcode_map.json`. Both
  `stats.py` (NeetCode completion %, weakest topic) and `dashboard.py` (topic
  table) use this file as the denominator, so a richer map produces a more
  accurate picture.
- Edit `NOTES_TEMPLATE` / `SOLUTION_TEMPLATE` in `scripts/_common.py` to match
  your preferred review format. New problems pick up the change immediately;
  existing notes/solutions are never overwritten.
