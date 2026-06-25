import os
import sys
from pathlib import Path

os.chdir(Path(__file__).parent)

from src import draw, i18n, schedule

SIGNUPS_DIR = Path("signups")


def main():
    _select_language()
    print(i18n.t("banner"))

    tournament = _select_tournament()
    if tournament is None:
        sys.exit(1)
    draw.show_signup_summary(tournament)

    while True:
        print(i18n.t("current_tournament", name=tournament.name))
        print(i18n.t("main_menu_prompt"))
        print(f"  1) {i18n.t('option_draw')}")
        print(f"  2) {i18n.t('option_schedule')}")
        print(f"  3) {i18n.t('option_switch')}")
        print(f"  4) {i18n.t('option_quit')}")
        print()
        try:
            choice = input("  > ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{i18n.t('goodbye')}")
            sys.exit(0)

        print()

        if choice == "1":
            draw.run(tournament)
        elif choice == "2":
            schedule.run(tournament)
        elif choice == "3":
            new = _select_tournament()
            if new is not None:
                tournament = new
                draw.show_signup_summary(tournament)
        elif choice in ("4", "q", "exit"):
            print(i18n.t("goodbye"))
            sys.exit(0)
        else:
            print(i18n.t("invalid_input_main") + "\n")


def _select_language():
    print("Sprache / Language / Langue:")
    for i, (code, label) in enumerate(i18n.LANGUAGES, 1):
        print(f"  {i}) {label}")
    print()
    while True:
        try:
            choice = input("  > ").strip()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(i18n.LANGUAGES):
            lang_code = i18n.LANGUAGES[int(choice) - 1][0]
            i18n.load(lang_code)
            print()
            return
        print(f"  1–{len(i18n.LANGUAGES)}")


def _select_tournament():
    if not SIGNUPS_DIR.exists():
        print(i18n.t("error_signups_dir_missing", dir=SIGNUPS_DIR) + "\n")
        return None

    tournaments = sorted([d for d in SIGNUPS_DIR.iterdir() if d.is_dir()])

    if not tournaments:
        print(i18n.t("no_tournaments_found"))
        print(f"  {i18n.t('no_tournaments_hint', dir=SIGNUPS_DIR)}\n")
        return None

    while True:
        print(i18n.t("select_tournament_prompt"))
        for i, tourn in enumerate(tournaments, 1):
            print(f"  {i}) {tourn.name}")
        print(f"  R) {i18n.t('option_reload')}")
        print(f"  X) {i18n.t('option_quit')}")
        print()

        try:
            choice = input("  > ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{i18n.t('goodbye')}")
            sys.exit(0)

        print()

        if choice == "R":
            tournaments = sorted([d for d in SIGNUPS_DIR.iterdir() if d.is_dir()])
        elif choice == "X":
            print(i18n.t("goodbye"))
            sys.exit(0)
        elif choice.isdigit() and 1 <= int(choice) <= len(tournaments):
            selected = tournaments[int(choice) - 1]
            print(i18n.t("tournament_selected", name=selected.name) + "\n")
            return selected
        else:
            print(i18n.t("invalid_input") + "\n")


if __name__ == "__main__":
    main()
