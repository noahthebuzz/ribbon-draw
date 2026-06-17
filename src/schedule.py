import csv
import random
from pathlib import Path

from src import config


def run(tournament: Path):
    print("=== Spielplan-Generator ===\n")
    print(f"Konfiguration: {config.COURTS} Felder, {config.PAIRS_PER_COURT} Pärchen/Feld, {config.ROUNDS} Runden\n")

    input_pairs = tournament / "output" / "pairs.csv"
    output_schedule = tournament / "output" / "schedule.csv"

    if not input_pairs.exists():
        print(f"Fehler: '{input_pairs}' wurde nicht gefunden.")
        print(f"  Führe zuerst die Auslosung durch.\n")
        return

    pairs = _read_pairs(input_pairs)
    print(f"{len(pairs)} Pärchen aus {input_pairs} geladen.\n")

    needed = config.COURTS * config.PAIRS_PER_COURT
    if len(pairs) < needed:
        print(
            f"Fehler: Zu wenige Pärchen – benötigt {needed} "
            f"({config.COURTS} Felder × {config.PAIRS_PER_COURT}), vorhanden {len(pairs)}.\n"
        )
        return

    (tournament / "output").mkdir(exist_ok=True)
    _generate_schedule(pairs, config.ROUNDS, config.COURTS, output_schedule)

    print(f"\nSpielplan gespeichert unter {output_schedule}\n")


def _read_pairs(path: Path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row["pair_name"] for row in reader]


def _generate_schedule(pairs, rounds, courts, path: Path):
    needed = courts * config.PAIRS_PER_COURT

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        header = ["Runde"]
        for i in range(courts):
            header += [f"Feld {i + 1}", "", ""]
        writer.writerow(header)

        for round_num in range(1, rounds + 1):
            active = pairs[:needed]
            if round_num > 1:
                random.shuffle(active)

            for pair_idx in range(3):
                row = [round_num if pair_idx == 0 else ""]
                for court_idx in range(courts):
                    base = court_idx * config.PAIRS_PER_COURT
                    row += [
                        active[base + pair_idx],
                        "vs." if pair_idx == 0 else "",
                        active[base + 3 + pair_idx],
                    ]
                writer.writerow(row)

            writer.writerow([])
