import csv
import random
from pathlib import Path

INPUT_PAIRS = Path("output/pairs.csv")
OUTPUT_SCHEDULE = Path("output/schedule.csv")

PAIRS_PER_COURT = 6


def run():
    print("=== Spielplan-Generator ===\n")

    if not INPUT_PAIRS.exists():
        print(f"Fehler: '{INPUT_PAIRS}' wurde nicht gefunden.")
        print("  Führe zuerst die Auslosung durch, oder lege eine Pärchen-Datei unter 'output/pairs.csv' ab.\n")
        return

    pairs = _read_pairs()
    print(f"{len(pairs)} Pärchen aus {INPUT_PAIRS} geladen.\n")

    rounds = _ask_int("Wie viele Runden sollen gespielt werden? ")
    if rounds is None:
        return
    courts = _ask_int("Wie viele Felder stehen zur Verfügung? ")
    if courts is None:
        return

    needed = courts * PAIRS_PER_COURT
    if len(pairs) < needed:
        print(
            f"\nFehler: Zu wenige Pärchen – benötigt {needed} "
            f"({courts} Felder × {PAIRS_PER_COURT}), vorhanden {len(pairs)}.\n"
        )
        return

    Path("output").mkdir(exist_ok=True)
    _generate_schedule(pairs, rounds, courts)

    print(f"\nSpielplan gespeichert unter {OUTPUT_SCHEDULE}\n")


def _read_pairs():
    with open(INPUT_PAIRS, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row["pair_name"] for row in reader]


def _generate_schedule(pairs, rounds, courts):
    needed = courts * PAIRS_PER_COURT

    with open(OUTPUT_SCHEDULE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        header = ["Runde"]
        for i in range(courts):
            header += [f"Feld {i + 1}", "", ""]
        writer.writerow(header)

        for round_num in range(1, rounds + 1):
            active = pairs[:needed]
            random.shuffle(active)

            for pair_idx in range(3):
                row = [round_num if pair_idx == 0 else ""]
                for court_idx in range(courts):
                    base = court_idx * PAIRS_PER_COURT
                    row += [
                        active[base + pair_idx],
                        "vs." if pair_idx == 0 else "",
                        active[base + 3 + pair_idx],
                    ]
                writer.writerow(row)

            writer.writerow([])


def _ask_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Bitte eine positive Zahl eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
        except (KeyboardInterrupt, EOFError):
            print()
            return None


