"""
Holt die Zusatzdaten des BFS, die weder in den ElCom-Daten noch in den
Regionalportraets stehen: Kanton, Sprachregion und Gemeindetypologie.

Zwei Quellen:
  A  Die Raumgliederungen der Schweiz 2019 (XLSX)
     -> Kanton, Sprachgebiet, Gemeindetypologie, Gebietsstand 01.01.2019
  B  Historisiertes Gemeindeverzeichnis, REST-Schnittstelle (CSV)
     -> Gemeindestand 01.01.2021 und die Gemeindemutationen 2018-2022.
        Damit werden die Gemeinden aufgeloest, die es 2019 noch nicht gab.

Ausfuehren:   python scripts/hole_zusatzdaten.py

Die Ablage ist unabhaengig vom Arbeitsverzeichnis: Das Skript legt die Dateien
immer im Repo ab, nicht im aktuellen Ordner.
"""

from pathlib import Path

import requests

WURZEL = Path(__file__).resolve().parent.parent

QUELLEN = [
    # (URL, Zielpfad relativ zur Repo-Wurzel)
    ("https://dam-api.bfs.admin.ch/hub/api/dam/assets/9046166/master",
     "daten/raumgliederungen/raumgliederungen_2019.xlsx"),
    ("https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date=01-01-2021",
     "daten/bfs/gemeindeverzeichnis_2021.csv"),
    ("https://www.agvchapp.bfs.admin.ch/api/communes/mutations"
     "?StartPeriod=01-01-2018&EndPeriod=31-12-2022",
     "daten/bfs/gemeindemutationen_2018_2022.csv"),
]


def hole(url: str, ziel: Path) -> None:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    ziel.write_bytes(r.content)
    print(f"  {ziel.relative_to(WURZEL)}  {len(r.content):,} Byte")


def main() -> None:
    print("Zusatzdaten vom BFS holen:")
    for url, pfad in QUELLEN:
        hole(url, WURZEL / pfad)
    print("Fertig.")


if __name__ == "__main__":
    main()
