"""
Fetches the additional FSO data that is contained neither in the ElCom data nor in
the regional portraits: canton, language region and municipality typology.

Two sources:
  A  "Die Raumgliederungen der Schweiz 2019" (XLSX), the FSO's Spatial divisions
     -> canton, language area, municipality typology, territorial status
        (German: Gebietsstand) of 1 January 2019
  B  "Historisiertes Gemeindeverzeichnis", the historicized list of the Swiss
     official commune register, REST interface (CSV)
     -> register snapshot of 1 January 2021 and the municipality changes
        2018-2022. These resolve the municipalities that did not yet exist in 2019.

Run with:   python scripts/hole_zusatzdaten.py

Where the files land does not depend on the working directory: the script always
writes inside the repository, not into the current folder.
"""

from pathlib import Path

import requests

WURZEL = Path(__file__).resolve().parent.parent

QUELLEN = [
    # (URL, target path relative to the repository root)
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
    print(f"  {ziel.relative_to(WURZEL)}  {len(r.content):,} bytes")


def main() -> None:
    print("Fetching the additional data from the FSO:")
    for url, pfad in QUELLEN:
        hole(url, WURZEL / pfad)
    print("Done.")


if __name__ == "__main__":
    main()
