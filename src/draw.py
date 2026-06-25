import csv
import random
from collections import defaultdict
from pathlib import Path

from src import config
from src.i18n import t

INPUT_PAIR_NAMES = Path("signups/pair_names.txt")

_FEMALE_GENDERS = {"frau", "f", "female", "w"}
_GENDER_SORT = {"female": 0, "male": 1}


def show_signup_summary(tournament: Path):
    input_signups = tournament / "input" / "signups.csv"
    if not input_signups.exists():
        return
    women, men = _read_signups(input_signups)
    total_w = sum(len(v) for v in women.values())
    total_m = sum(len(v) for v in men.values())
    pairs = min(total_w, total_m)
    print(t("signup_summary_header"))
    print(t("signup_summary_women", w=total_w))
    print(t("signup_summary_men", m=total_m))
    print(t("signup_summary_total", total=total_w + total_m))
    print(t("signup_summary_pairs", pairs=pairs))
    print()


def run(tournament: Path):
    print(t("draw_header") + "\n")

    input_signups = tournament / "input" / "signups.csv"
    output_pairs = tournament / "output" / "pairs.csv"
    output_unlucky = tournament / "output" / "unlucky.csv"

    if not input_signups.exists():
        print(t("error_file_not_found", path=input_signups))
        print(f"  {t('error_signups_hint', name=tournament.name)}\n")
        return
    if not INPUT_PAIR_NAMES.exists():
        print(t("error_file_not_found", path=INPUT_PAIR_NAMES) + "\n")
        return

    women, men = _read_signups(input_signups)
    total_w = sum(len(v) for v in women.values())
    total_m = sum(len(v) for v in men.values())
    print(t("signups_loaded", w=total_w, m=total_m, total=total_w + total_m) + "\n")

    courts = _resolve_courts(total_w, total_m)
    if courts is None:
        return

    n_pairs = courts * config.PAIRS_PER_COURT
    sit_out_w = total_w - n_pairs
    sit_out_m = total_m - n_pairs
    print(t("drawing_n_pairs", n=n_pairs))
    if sit_out_w > 0 or sit_out_m > 0:
        print(f"  {t('sit_out', w=sit_out_w, m=sit_out_m)}\n")

    selected_women, unlucky_women = _select_equally(women, n_pairs)
    selected_men, unlucky_men = _select_equally(men, n_pairs)

    pair_names = _read_pair_names()
    if len(pair_names) < n_pairs:
        print(t("pair_names_warning", available=len(pair_names), needed=n_pairs))

    pairs = _create_pairs(selected_women, selected_men, pair_names)

    (tournament / "output").mkdir(exist_ok=True)
    _write_pairs(pairs, output_pairs)
    _write_unlucky(unlucky_women, unlucky_men, output_unlucky)

    print(f"\n{t('draw_success', n=len(pairs))}")
    print(f"  {t('output_pairs_label', path=output_pairs)}")
    print(f"  {t('output_unlucky_label', path=output_unlucky)}")
    if unlucky_women or unlucky_men:
        print(f"  {t('unlucky_count', w=len(unlucky_women), m=len(unlucky_men))}")
    print()


def _resolve_courts(total_w, total_m):
    courts = config.COURTS
    while True:
        available = min(total_w, total_m)
        needed = courts * config.PAIRS_PER_COURT
        if available >= needed:
            return courts

        next_courts = courts - 1
        if next_courts == 0:
            print(t("error_min_signups", min=config.PAIRS_PER_COURT) + "\n")
            return None

        next_pairs = next_courts * config.PAIRS_PER_COURT
        print(t("not_enough_signups", courts=courts, needed=needed, available=available))
        print(f"  1) {t('option_abort')}")
        print(f"  2) {t('option_fewer_courts', courts=next_courts, pairs=next_pairs)}")
        print()

        while True:
            try:
                choice = input("  > ").strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{t('draw_aborted')}\n")
                return None
            if choice == "1":
                print(t("draw_aborted") + "\n")
                return None
            if choice == "2":
                courts -= 1
                print()
                break
            print(t("prompt_1_or_2"))


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
        print(t("duplicates_removed", n=duplicates))

    return women, men


def _select_equally(teams, n):
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
                "pair_name": pair_names[i] if i < len(pair_names) else t("pair_fallback", n=i + 1),
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


def _write_unlucky(unlucky_women, unlucky_men, path: Path):
    entries = [("female", name, team) for name, team in unlucky_women] + \
              [("male", name, team) for name, team in unlucky_men]
    entries.sort(key=lambda e: (e[2].lower(), _GENDER_SORT[e[0]], e[1].lower()))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([t("col_gender"), t("col_name"), t("col_team")])
        for gender_key, name, team in entries:
            label = t("gender_female") if gender_key == "female" else t("gender_male")
            writer.writerow([label, name, team])
