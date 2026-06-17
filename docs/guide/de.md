# ribbon-draw — Anleitung

## Voraussetzungen

- Python 3.8 oder höher ([python.org](https://www.python.org))
- Keine zusätzlichen Pakete erforderlich

## Programm starten

**Windows:** `start.bat` doppelklicken

**Mac / Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Oder direkt:**
```bash
python3 main.py
```

## Erstes Turnier anlegen

1. Einen Unterordner in `signups/` mit dem Namen des Turniers erstellen (frei wählbar)
2. Darin einen `input/`-Ordner erstellen
3. Die Anmeldungsdatei als `signups.csv` in diesen `input/`-Ordner legen

```
signups/
  mein-turnier/
    input/
      signups.csv      ← hier ablegen
    output/            ← wird automatisch erstellt
```

## Ablauf

Beim Programmstart wird zuerst eine Sprache ausgewählt, danach das Turnier.

### Schritt 1 — Auslosung

Liest die Anmeldungen und lost gemischte Pärchen aus (je eine Frau und ein Mann), gleichmäßig über die Teams verteilt. Personen ohne Platz werden als Pechvögel aufgeführt.

Falls nicht genug Anmeldungen für die konfigurierte Feldanzahl vorhanden sind, fragt das Programm ob mit einem Feld weniger weitergemacht werden soll.

**Ausgabe:**
- `output/pairs.csv` — ausgeloste Pärchen (alphabetisch nach Pärchennamen sortiert)
- `output/unlucky.csv` — Personen ohne Platz (sortiert nach Team, Geschlecht, Name)

### Schritt 2 — Spielplan

Generiert einen Spielplan über alle Felder und Runden.

- **Runde 1:** Pärchen werden in sortierter Reihenfolge auf die Felder verteilt (Pärchen 1–6 → Feld 1, 7–12 → Feld 2, …)
- **Ab Runde 2:** Pärchen werden zufällig verteilt

**Ausgabe:**
- `output/schedule.csv` — Spielplan, direkt in Excel öffenbar

## Konfiguration

`config.ini` im Hauptordner anpassen:

```ini
[Turnier]
courts = 9           # Anzahl Felder
pairs_per_court = 6  # Pärchen pro Feld
rounds = 5           # Anzahl Runden
```

## Pärchennamen

`signups/pair_names.txt` enthält die Namen der Pärchen (einer pro Zeile, z.B. `Romeo & Julia`). Die Datei wird von allen Turnieren gemeinsam genutzt und kann frei bearbeitet werden.

## Format der Anmeldungsdatei

Jede Zeile enthält einen Eintrag im folgenden Format:

```
"Name,""Frau"",""Teamname"",""2025-07-05T08:00:00+00:00"""
```

| Position | Inhalt                  |
|----------|-------------------------|
| 1        | Vollständiger Name      |
| 2        | `Frau` oder `Mann`      |
| 3        | Teamname                |
| 4        | Zeitstempel (ignoriert) |

Doppelte Einträge (gleicher Name + Geschlecht + Team) werden automatisch entfernt.
