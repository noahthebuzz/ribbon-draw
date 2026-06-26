import csv
import random
from pathlib import Path

from src import config
from src.i18n import t


def run(tournament: Path):
    print(t("schedule_header") + "\n")

    input_pairs = tournament / "output" / "pairs.csv"
    output_schedule = tournament / "output" / "schedule.csv"

    if not input_pairs.exists():
        print(t("error_file_not_found", path=input_pairs))
        print(f"  {t('error_pairs_hint')}\n")
        return

    pairs = _read_pairs(input_pairs)
    print(t("pairs_loaded", n=len(pairs), path=input_pairs) + "\n")

    if len(pairs) < config.PAIRS_PER_COURT:
        print(t("error_too_few_pairs", needed=config.PAIRS_PER_COURT, courts=1, ppc=config.PAIRS_PER_COURT, available=len(pairs)) + "\n")
        return

    courts = len(pairs) // config.PAIRS_PER_COURT
    print(t("schedule_config", courts=courts, ppc=config.PAIRS_PER_COURT, rounds=config.ROUNDS) + "\n")
    if courts < config.COURTS:
        print(t("schedule_fewer_courts", courts=courts) + "\n")

    (tournament / "output").mkdir(exist_ok=True)
    _generate_schedule(pairs, config.ROUNDS, courts, output_schedule)

    print(t("schedule_saved", path=output_schedule) + "\n")


def _read_pairs(path: Path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row["pair_name"] for row in reader]


def _generate_schedule(pairs, rounds, courts, path: Path):
    needed = courts * config.PAIRS_PER_COURT

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        header = [t("col_round")]
        for i in range(courts):
            header += [t("court_label", n=i + 1), "", ""]
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
