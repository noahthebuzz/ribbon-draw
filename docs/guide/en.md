# ribbon-draw — User Guide

## Requirements

- Python 3.8 or higher ([python.org](https://www.python.org))
- No additional packages required

## Starting the program

**Windows:** Double-click `start.bat`

**Mac / Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Or directly:**
```bash
python3 main.py
```

## Setting up your first tournament

1. Create a subfolder inside `signups/` with the name of your tournament (any name)
2. Create an `input/` folder inside it
3. Place your signups file as `signups.csv` in that `input/` folder

```
signups/
  my-tournament/
    input/
      signups.csv      ← place file here
    output/            ← created automatically
```

## Workflow

On startup the program first asks for a language, then for a tournament.

### Step 1 — Pair Draw

Reads the signups and draws mixed pairs (one woman + one man), distributed evenly across teams. Players who don't get a spot are listed as unlucky.

If there are not enough signups for the configured number of courts, the program asks whether to abort or continue with one fewer court.

**Output:**
- `output/pairs.csv` — drawn pairs (sorted A→Z by pair name)
- `output/unlucky.csv` — players without a spot (sorted by team, gender, name)

### Step 2 — Schedule

Generates a match schedule across all courts and rounds.

- **Round 1:** Pairs are assigned in sorted order (pairs 1–6 → court 1, 7–12 → court 2, …)
- **Round 2+:** Pairs are assigned randomly

**Output:**
- `output/schedule.csv` — full match schedule, opens directly in Excel

## Configuration

Edit `config.ini` in the main folder:

```ini
[Turnier]
courts = 9           # number of courts
pairs_per_court = 6  # pairs per court
rounds = 5           # number of rounds
```

## Pair names

`signups/pair_names.txt` contains the couple names (one per line, e.g. `Romeo & Juliet`). This file is shared across all tournaments and can be freely edited.

## Signups file format

Each row contains one entry in the following format:

```
"Name,""Female"",""Team Name"",""2025-07-05T08:00:00+00:00"""
```

| Position | Content                 |
|----------|-------------------------|
| 1        | Full name               |
| 2        | `Frau` or `Mann`        |
| 3        | Team name               |
| 4        | Timestamp (ignored)     |

Duplicate entries (same name + gender + team) are removed automatically.
