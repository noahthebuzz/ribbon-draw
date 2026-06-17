import os
import sys
from pathlib import Path

os.chdir(Path(__file__).parent)

from src import draw, schedule

BANNER = """
╔══════════════════════════════════╗
║          ribbon-draw             ║
║  Volleyball Turnier-Verwaltung   ║
╚══════════════════════════════════╝
"""

SIGNUPS_DIR = Path("signups")


def main():
    print(BANNER)
    tournament = _select_tournament()
    if tournament is None:
        sys.exit(1)

    while True:
        print(f"Turnier: {tournament.name}")
        print("Was möchtest du tun?")
        print("  1) Auslosung        – Pärchen aus Anmeldungen auslosen")
        print("  2) Spielplan        – Spielplan generieren")
        print("  3) Turnier wechseln – anderes Turnier laden")
        print("  4) Beenden")
        print()
        try:
            choice = input("  > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nTschüss!")
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
        elif choice in ("4", "q", "exit"):
            print("Tschüss!")
            sys.exit(0)
        else:
            print("Unbekannte Eingabe. Bitte 1, 2, 3 oder 4 eingeben.\n")


def _select_tournament():
    if not SIGNUPS_DIR.exists():
        print(f"Fehler: Ordner '{SIGNUPS_DIR}' wurde nicht gefunden.\n")
        return None

    tournaments = sorted([d for d in SIGNUPS_DIR.iterdir() if d.is_dir()])

    if not tournaments:
        print("Keine Turniere gefunden.")
        print(f"  Erstelle einen Unterordner in '{SIGNUPS_DIR}/' mit dem Namen des Turniers")
        print(f"  und lege die Anmeldungsdatei dort ab:")
        print(f"  signups/<turnier-name>/input/signups.csv\n")
        return None

    while True:
        print("Welches Turnier soll verwendet werden?")
        for i, t in enumerate(tournaments, 1):
            print(f"  {i}) {t.name}")
        print(f"  R) Neu laden")
        print(f"  X) Beenden")
        print()

        try:
            choice = input("  > ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\nTschüss!")
            sys.exit(0)

        print()

        if choice == "R":
            tournaments = sorted([d for d in SIGNUPS_DIR.iterdir() if d.is_dir()])
        elif choice == "X":
            print("Tschüss!")
            sys.exit(0)
        elif choice.isdigit() and 1 <= int(choice) <= len(tournaments):
            selected = tournaments[int(choice) - 1]
            print(f"Turnier \"{selected.name}\" ausgewählt.\n")
            return selected
        else:
            print(f"Ungültige Eingabe.\n")


if __name__ == "__main__":
    main()
