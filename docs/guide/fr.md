# ribbon-draw — Guide d'utilisation

## Prérequis

- Python 3.8 ou supérieur ([python.org](https://www.python.org))
- Aucun paquet supplémentaire requis

## Lancer le programme

**Windows :** Double-cliquer sur `start.bat`

**Mac / Linux :**
```bash
chmod +x start.sh
./start.sh
```

**Ou directement :**
```bash
python3 main.py
```

## Créer votre premier tournoi

1. Créer un sous-dossier dans `signups/` avec le nom du tournoi (au choix)
2. Créer un dossier `input/` à l'intérieur
3. Placer le fichier d'inscriptions sous le nom `signups.csv` dans ce dossier `input/`

```
signups/
  mon-tournoi/
    input/
      signups.csv      ← placer le fichier ici
    output/            ← créé automatiquement
```

## Déroulement

Au démarrage, le programme demande d'abord une langue, puis un tournoi.

### Étape 1 — Tirage au sort

Lit les inscriptions et forme des paires mixtes (une femme + un homme), réparties équitablement entre les équipes. Les joueurs sans place sont listés comme malchanceux.

Si les inscriptions sont insuffisantes pour le nombre de terrains configuré, le programme demande si l'on souhaite annuler ou continuer avec un terrain de moins.

**Résultats :**
- `output/pairs.csv` — paires tirées au sort (triées A→Z par nom de paire)
- `output/unlucky.csv` — joueurs sans place (triés par équipe, genre, nom)

### Étape 2 — Planning

Génère un planning de matchs sur tous les terrains et toutes les manches.

- **Manche 1 :** Les paires sont attribuées dans l'ordre trié (paires 1–6 → terrain 1, 7–12 → terrain 2, …)
- **Manches 2+ :** Les paires sont attribuées aléatoirement

**Résultat :**
- `output/schedule.csv` — planning complet, s'ouvre directement dans Excel

## Configuration

Modifier `config.ini` dans le dossier principal :

```ini
[Turnier]
courts = 9           # nombre de terrains
pairs_per_court = 6  # paires par terrain
rounds = 5           # nombre de manches
```

## Noms des paires

`signups/pair_names.txt` contient les noms des paires (un par ligne, ex. `Roméo & Juliette`). Ce fichier est partagé entre tous les tournois et peut être librement modifié.

## Format du fichier d'inscriptions

Chaque ligne contient une inscription au format suivant :

```
"Nom,""Frau"",""Nom d'équipe"",""2025-07-05T08:00:00+00:00"""
```

| Position | Contenu                  |
|----------|--------------------------|
| 1        | Nom complet              |
| 2        | `Frau` ou `Mann`         |
| 3        | Nom d'équipe             |
| 4        | Horodatage (ignoré)      |

Les entrées en double (même nom + genre + équipe) sont supprimées automatiquement.
