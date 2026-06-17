# ribbon-draw — Technical Documentation

## Overview

ribbon-draw is a CLI tool for managing mixed-pair volleyball ribbon tournaments. It handles two steps: drawing pairs from signups, and generating a randomized match schedule across courts and rounds.

## Technology Stack

| Component       | Technology                                  |
|-----------------|---------------------------------------------|
| Language        | Python 3.8+                                 |
| Dependencies    | None — standard library only                |
| CSV parsing     | `csv` (stdlib)                              |
| Configuration   | `configparser` (stdlib, INI format)         |
| Localization    | Custom JSON-based i18n (`json` stdlib)      |
| Randomization   | `random` (stdlib)                           |
| File I/O        | `pathlib` (stdlib)                          |

No external packages are required. The tool runs on any system with a standard Python 3.8+ installation.

## Project Structure

```
ribbon-draw/
├── main.py                  # Entry point, CLI menu, language/tournament selection
├── config.ini               # Tournament configuration (courts, rounds, etc.)
├── src/
│   ├── config.py            # Reads config.ini, exposes COURTS / PAIRS_PER_COURT / ROUNDS / PAIRS
│   ├── draw.py              # Pair draw logic
│   ├── schedule.py          # Schedule generation logic
│   └── i18n.py              # Localization module
├── locales/
│   ├── de.json              # German strings
│   ├── en.json              # English strings
│   └── fr.json              # French strings
├── signups/
│   ├── pair_names.txt       # Shared couple names (used across all tournaments)
│   └── <tournament>/
│       ├── input/
│       │   └── signups.csv
│       └── output/
│           ├── pairs.csv
│           ├── unlucky.csv
│           └── schedule.csv
└── docs/
    ├── TECHNICAL.md         # This file
    └── guide/
        ├── de.md
        ├── en.md
        └── fr.md
```

## Architecture

### Startup flow

1. Language selection (`main._select_language`) — loads the chosen locale via `i18n.load()`
2. Tournament selection (`main._select_tournament`) — lists subdirectories of `signups/`
3. Main menu loop — dispatches to `draw.run()` or `schedule.run()`

### Localization (`src/i18n.py`)

A thin module with two public functions:

- `load(lang)` — reads `locales/<lang>.json` into an in-memory dict
- `t(key, **kwargs)` — returns the translated string, with `str.format()` interpolation for placeholders

All user-facing strings (console output, CSV column headers, gender labels) go through `t()`. Internal CSV column names (e.g. `pair_name`) are kept in English as stable identifiers read back by the program.

### Pair draw (`src/draw.py`)

1. Reads and deduplicates `signups.csv` (custom double-quoted CSV format from the signup form)
2. Splits players into women/men dicts keyed by team
3. Selects players via round-robin across teams for even distribution (`_select_equally`)
4. Pairs each woman with a man, preferring cross-team matches (`_create_pairs`)
5. If signups fall short of the configured court count, prompts the user to reduce courts by one and retries
6. Outputs `pairs.csv` (sorted A→Z by pair name) and `unlucky.csv` (sorted by team → gender → name)

### Schedule generation (`src/schedule.py`)

- Round 1: pairs assigned in sorted order (pairs 1–6 → court 1, 7–12 → court 2, …)
- Rounds 2+: pairs shuffled randomly before assignment
- Output is a semicolon-delimited CSV readable directly in Excel

### Configuration (`src/config.py`)

Reads `config.ini` at import time and exposes module-level constants. Falls back to built-in defaults if the file is missing.

```ini
[Turnier]
courts = 9
pairs_per_court = 6
rounds = 5
```

`PAIRS` is always derived as `courts × pairs_per_court` and never set directly.

## Signups CSV Format

The signup form exports a non-standard CSV where each row is a single outer-quoted field containing inner CSV data:

```
"Name,""Frau"",""Team Name"",""2025-07-05T08:00:00+00:00"""
```

The parser reads the outer field, then re-parses the inner value to extract name, gender, team, and timestamp (timestamp is ignored). Duplicate rows (same name + gender + team) and a trailing template row (`your-name,...`) are filtered automatically.

## Roadmap

### i18n — additional languages

The localization system is intentionally minimal and easy to extend. Adding a new language requires:

1. Creating `locales/<code>.json` with all required keys (copy `en.json` as a template)
2. Adding an entry to `LANGUAGES` in `src/i18n.py`

Planned languages:

| Code | Language    |
|------|-------------|
| `es` | Español     |
| `pt` | Português   |
| `it` | Italiano    |
| `nl` | Nederlands  |
| `pl` | Polski      |

### Other planned improvements

- **Persistent language preference** — remember the last chosen language between sessions (e.g. in `config.ini`)
- **Web frontend** — optional Streamlit UI as an alternative to the CLI, for less technical users
- **Schedule fairness** — track which pairs have played each other and minimize repeat matchups across rounds
- **Export formats** — PDF or formatted Excel output for printing the schedule on-site
