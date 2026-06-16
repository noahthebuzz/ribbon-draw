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


def main():
    print(BANNER)
    while True:
        print("Was möchtest du tun?")
        print("  1) Auslosung   – Pärchen aus Anmeldungen auslosen")
        print("  2) Spielplan   – Spielplan generieren")
        print("  3) Beenden")
        print()
        try:
            choice = input("  > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nTschüss!")
            sys.exit(0)

        print()

        if choice == "1":
            draw.run()
        elif choice == "2":
            schedule.run()
        elif choice in ("3", "q", "exit"):
            print("Tschüss!")
            sys.exit(0)
        else:
            print("Unbekannte Eingabe. Bitte 1, 2 oder 3 eingeben.\n")


if __name__ == "__main__":
    main()
