# ribbon-draw

Schedule generator for mixed-pair volleyball ribbon tournaments — randomly draws teams into pairs each round, balancing winners and losers across courts.

## Requirements

- Python 3.8 or higher (download at [python.org](https://www.python.org))
- No additional packages required

## Setup

1. Download or clone this repository
2. For each tournament, create a folder under `signups/` and place your signups file there (see structure below)

## Folder structure

```
signups/
  pair_names.txt         ← shared across all tournaments, can be customized
  mein-turnier/          ← create this folder (any name)
    input/               ← create this folder
      signups.csv        ← place your signups file here
    output/              ← created automatically by the program
      pairs.csv
      unlucky.csv
      schedule.csv
config.ini               ← tournament settings (courts, rounds, etc.)
```

## Running the program

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

On startup the program lists all available tournaments in `signups/` and asks you to select one.

## Workflow

### Step 1 – Pair Draw (Auslosung)

Reads `signups/<turnier>/input/signups.csv` and draws mixed pairs (one woman + one man), distributed evenly across teams. Players who don't get a spot are listed as unlucky.

If there are not enough signups for the configured number of courts, the program asks whether to abort or continue with one fewer court.

**Output:**
- `signups/<turnier>/output/pairs.csv` — the drawn pairs with their couple name
- `signups/<turnier>/output/unlucky.csv` — players without a spot

### Step 2 – Schedule (Spielplan)

Reads the pairs from the tournament's output folder and generates a randomized match schedule across courts and rounds.

**Output:**
- `signups/<turnier>/output/schedule.csv` — the full match schedule, readable in Excel

## Input file format

### `signups/<turnier>/input/signups.csv`

Each row is a single outer-quoted field containing name, gender, team, and timestamp:

```
"Anna Schmidt,""Frau"",""SV Mensfelden"",""2025-07-05T08:00:00+00:00"""
"Thomas Müller,""Mann"",""SV Mensfelden"",""2025-07-05T08:01:00+00:00"""
```

| Position | Values               |
|----------|----------------------|
| 1        | Full name            |
| 2        | `Frau` or `Mann`     |
| 3        | Team name            |
| 4        | Timestamp (ignored)  |

Duplicate entries (same name + gender + team) are removed automatically. A trailing template row (`your-name,...`) is skipped.

### `signups/pair_names.txt`

One couple name per line (e.g. `Romeo & Julia`). A list of 60 names is included and is shared across all tournaments. You can add or remove names as you like.

## Configuration

Edit `config.ini` to adjust tournament settings:

```ini
[Turnier]
courts = 9           # number of courts
pairs_per_court = 6  # pairs per court (total pairs = courts × pairs_per_court)
rounds = 5           # number of rounds played
```

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).
