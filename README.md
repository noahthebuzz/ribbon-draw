# ribbon-draw

Schedule generator for mixed-pair volleyball ribbon tournaments — randomly draws teams into pairs each round, balancing winners and losers across courts.

## Requirements

- Python 3.8 or higher (download at [python.org](https://www.python.org))
- No additional packages required

## Setup

1. Download or clone this repository
2. Place your signups file as `input/signups.csv` (see format below)

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

## Workflow

The program has two steps:

### Step 1 – Pair Draw (Auslosung)

Reads `input/signups.csv` and draws mixed pairs (one woman + one man), distributed evenly across teams. Players who don't get a spot are listed as unlucky.

**Output:**
- `output/pairs.csv` — the drawn pairs with their couple name
- `output/unlucky.csv` — players without a spot

### Step 2 – Schedule (Spielplan)

Reads the pairs from `output/pairs.csv` and generates a randomized match schedule across courts and rounds.

**Output:**
- `output/schedule.csv` — the full match schedule, readable in Excel

## Input file format

### `input/signups.csv`

```
name,gender,team
Anna Schmidt,Frau,SV Mensfelden
Thomas Müller,Mann,SV Mensfelden
Lisa Weber,Frau,TSV Lindheim
```

| Column   | Values               |
|----------|----------------------|
| `name`   | Full name            |
| `gender` | `Frau` or `Mann`     |
| `team`   | Team name            |

See `input/signups_example.csv` for a full example.

### `input/pair_names.txt`

One couple name per line (e.g. `Romeo & Julia`). A list of 60 names is included. You can add or remove names as you like.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).
