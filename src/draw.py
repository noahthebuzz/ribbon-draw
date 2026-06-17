import csv
import random
from collections import defaultdict
from pathlib import Path

from src import config

INPUT_PAIR_NAMES = Path("signups/pair_names.txt")

_FEMALE_GENDERS = {"frau", "f", "female", "w"}


def run(tournament: Path):
    print("=== Auslosung ===\n")

    input_signups = tournament / "input" / "signups.csv"
    output_pairs = tournament / "output" / "pairs.csv"
    output_unlucky = tournament / "output" / "unlucky.csv"

    if not input_signups.exists():
        print(f"Fehler: '{input_signups}' wurde nicht gefunden.")
        print(f"  Lege die Anmeldungsdatei unter 'signups/{tournament.name}/input/signups.csv' ab.\n")
        return
    if not INPUT_PAIR_NAMES.exists():
        print(f"Fehler: '{INPUT_PAIR_NAMES}' wurde nicht gefunden.\n")
        return

    women, men = _read_signups(input_signups)
    total_w = sum(len(v) for v in women.values())
    total_m = sum(len(v) for v in men.values())
    print(f"Anmeldungen geladen: {total_w} Frauen, {total_m} Männer ({total_w + total_m} gesamt)\n")

    courts = _resolve_courts(total_w, total_m)
    if courts is None:
        return

    n_pairs = courts * config.PAIRS_PER_COURT
    sit_out_w = total_w - n_pairs
    sit_out_m = total_m - n_pairs
    print(f"Es werden {n_pairs} Pärchen ausgelost.")
    if sit_out_w > 0 or sit_out_m > 0:
        print(f"  {sit_out_w} Frauen und {sit_out_m} Männer werden nicht berücksichtigt (Pechvögel).\n")

    selected_women, unlucky_women = _select_equally(women, n_pairs)
    selected_men, unlucky_men = _select_equally(men, n_pairs)

    pair_names = _read_pair_names()
    if len(pair_names) < n_pairs:
        print(
            f"Hinweis: Nur {len(pair_names)} Pärchennamen vorhanden, "
            f"{n_pairs} benötigt. Fehlende werden durchnummeriert."
        )

    pairs = _create_pairs(selected_women, selected_men, pair_names)

    (tournament / "output").mkdir(exist_ok=True)
    _write_pairs(pairs, output_pairs)
    _write_unlucky(unlucky_women, unlucky_men, output_unlucky)

    print(f"\n{len(pairs)} Pärchen wurden erfolgreich ausgelost.")
    print(f"  Pärchen    → {output_pairs}")
    print(f"  Pechvögel  → {output_unlucky}")
    if unlucky_women or unlucky_men:
        print(f"  ({len(unlucky_women)} Frauen und {len(unlucky_men)} Männer haben keinen Platz bekommen.)")
    print()


def _resolve_courts(total_w, total_m):
    """Returns the number of courts to use, asking the user to reduce if signups are insufficient.
    Returns None if the user aborts or no valid court count exists."""
    courts = config.COURTS
    while True:
        available = min(total_w, total_m)
        needed = courts * config.PAIRS_PER_COURT
        if available >= needed:
            return courts

        next_courts = courts - 1
        if next_courts == 0:
            print(
                f"Fehler: Nicht genug Anmeldungen für ein Turnier. "
                f"Mindestens {config.PAIRS_PER_COURT} Frauen und {config.PAIRS_PER_COURT} Männer benötigt.\n"
            )
            return None

        next_pairs = next_courts * config.PAIRS_PER_COURT
        print(
            f"Nicht genug Anmeldungen für {courts} Felder "
            f"({needed} Pärchen benötigt, nur {available} möglich)."
        )
        print(f"  1) Abbrechen")
        print(f"  2) Mit {next_courts} Feldern ({next_pairs} Pärchen) weitermachen")
        print()

        while True:
            try:
                choice = input("  > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nAuslosung abgebrochen.\n")
                return None
            if choice == "1":
                print("Auslosung abgebrochen.\n")
                return None
            if choice == "2":
                courts -= 1
                print()
                break
            print("Bitte 1 oder 2 eingeben.")


def _read_signups(path: Path):
    women = defaultdict(list)
    men = defaultdict(list)
    seen = set()
    duplicates = 0

    with open(path, newline="", encoding="utf-8-sig") as f:
        for outer_row in csv.reader(f):
            if not outer_row:
                continue
            # Each row is a single outer-quoted field containing inner CSV:
            # "Name,""Gender"",""Team"",""Timestamp"""
            inner = next(csv.reader([outer_row[0]]))
            if len(inner) < 3:
                continue
            name, gender, team = inner[0].strip(), inner[1].strip().lower(), inner[2].strip()
            if name.lower() in ("your-name", "name"):
                continue
            key = (name, gender, team)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            if gender in _FEMALE_GENDERS:
                women[team].append(name)
            else:
                men[team].append(name)

    if duplicates:
        print(f"Hinweis: {duplicates} doppelte Anmeldung(en) wurden entfernt.")

    return women, men


def _select_equally(teams, n):
    """Selects n players via round-robin across teams for even distribution."""
    pools = {team: players[:] for team, players in teams.items()}
    for players in pools.values():
        random.shuffle(players)

    selected = []
    while len(selected) < n:
        made_progress = False
        for team, players in list(pools.items()):
            if players:
                selected.append((players.pop(0), team))
                made_progress = True
                if len(selected) >= n:
                    break
        if not made_progress:
            break

    unlucky = [(p, team) for team, players in pools.items() for p in players]
    return selected, unlucky


def _create_pairs(women, men, pair_names):
    """Pairs each woman with a man, preferring different teams."""
    random.shuffle(pair_names)
    men_pool = list(men)
    random.shuffle(men_pool)

    pairs = []
    for i, (woman_name, woman_team) in enumerate(women):
        matched_idx = next(
            (j for j, (_, man_team) in enumerate(men_pool) if man_team != woman_team),
            0 if men_pool else None,
        )
        if matched_idx is None:
            break
        man_name, man_team = men_pool.pop(matched_idx)
        pairs.append(
            {
                "pair_name": pair_names[i] if i < len(pair_names) else f"Pärchen {i + 1}",
                "woman_name": woman_name,
                "woman_team": woman_team,
                "man_name": man_name,
                "man_team": man_team,
            }
        )

    return pairs


def _read_pair_names():
    with open(INPUT_PAIR_NAMES, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _write_pairs(pairs, path: Path):
    sorted_pairs = sorted(pairs, key=lambda p: p["pair_name"].lower())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["pair_name", "woman_name", "woman_team", "man_name", "man_team"],
        )
        writer.writeheader()
        writer.writerows(sorted_pairs)


_GENDER_ORDER = {"frau": 0, "mann": 1}


def _write_unlucky(unlucky_women, unlucky_men, path: Path):
    entries = [("Frau", name, team) for name, team in unlucky_women] + \
              [("Mann", name, team) for name, team in unlucky_men]
    entries.sort(key=lambda e: (e[2].lower(), _GENDER_ORDER.get(e[0].lower(), 2), e[1].lower()))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["geschlecht", "name", "team"])
        for geschlecht, name, team in entries:
            writer.writerow([geschlecht, name, team])
