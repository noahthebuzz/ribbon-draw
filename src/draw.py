import csv
import random
from collections import defaultdict
from pathlib import Path

INPUT_SIGNUPS = Path("input/signups.csv")
INPUT_PAIR_NAMES = Path("input/pair_names.txt")
OUTPUT_PAIRS = Path("output/pairs.csv")
OUTPUT_UNLUCKY = Path("output/unlucky.csv")

_FEMALE_GENDERS = {"frau", "f", "female", "w"}


def run():
    print("=== Auslosung ===\n")

    if not INPUT_SIGNUPS.exists():
        print(f"Fehler: '{INPUT_SIGNUPS}' wurde nicht gefunden.")
        print("  Lege die Anmeldungsdatei als 'input/signups.csv' ab.\n")
        return
    if not INPUT_PAIR_NAMES.exists():
        print(f"Fehler: '{INPUT_PAIR_NAMES}' wurde nicht gefunden.\n")
        return

    women, men = _read_signups()
    total_w = sum(len(v) for v in women.values())
    total_m = sum(len(v) for v in men.values())
    print(f"Anmeldungen geladen: {total_w} Frauen, {total_m} Männer ({total_w + total_m} gesamt)\n")

    if total_w < 6 or total_m < 6:
        print(f"Fehler: Zu wenige Anmeldungen – mindestens 6 Frauen und 6 Männer benötigt.")
        print(f"  Aktuell: {total_w} Frauen, {total_m} Männer.\n")
        return

    n_pairs = (min(total_w, total_m) // 6) * 6
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

    Path("output").mkdir(exist_ok=True)
    _write_pairs(pairs)
    _write_unlucky(unlucky_women, unlucky_men)

    print(f"\n{len(pairs)} Pärchen wurden erfolgreich ausgelost.")
    print(f"  Pärchen    → {OUTPUT_PAIRS}")
    print(f"  Pechvögel  → {OUTPUT_UNLUCKY}")
    if unlucky_women or unlucky_men:
        print(f"  ({len(unlucky_women)} Frauen und {len(unlucky_men)} Männer haben keinen Platz bekommen.)")
    print()


def _read_signups():
    women = defaultdict(list)
    men = defaultdict(list)
    seen = set()
    duplicates = 0

    with open(INPUT_SIGNUPS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            gender = row["gender"].strip().lower()
            team = row["team"].strip()
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
        # Prefer a man from a different team
        matched_idx = next(
            (j for j, (_, man_team) in enumerate(men_pool) if man_team != woman_team),
            0 if men_pool else None,
        )
        if matched_idx is None:
            break
        man_name, man_team = men_pool.pop(matched_idx)
        pairs.append(
            {
                "number": i + 1,
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


def _write_pairs(pairs):
    with open(OUTPUT_PAIRS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["number", "pair_name", "woman_name", "woman_team", "man_name", "man_team"],
        )
        writer.writeheader()
        writer.writerows(pairs)


def _write_unlucky(unlucky_women, unlucky_men):
    with open(OUTPUT_UNLUCKY, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["geschlecht", "name", "team"])
        for name, team in unlucky_women:
            writer.writerow(["Frau", name, team])
        for name, team in unlucky_men:
            writer.writerow(["Mann", name, team])


