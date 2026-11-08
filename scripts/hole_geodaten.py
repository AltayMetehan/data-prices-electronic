"""
Holt die Gemeindegrenzen von swisstopo und erzeugt daraus eine kleine
Geometriedatei fuer unsere 2087 Gemeinden.

Quelle: swissBOUNDARIES3D, Ausgabe 2026-01, Ebene tlm_hoheitsgebiet.
Die Rohdatei ist rund 36 MB gepackt und 74 MB entpackt. Sie wird NICHT ins Repo
gelegt, sondern nach daten/geo/_roh/ geholt, das die .gitignore ausschliesst.

Im Repo landet nur daten/geo/gemeinden_2087.geojson:
  - nur unsere 2087 Gemeinden
  - ohne Z-Dimension
  - vereinfacht mit 100 m Toleranz
  - umgerechnet von LV95 (EPSG:2056) nach WGS84 (EPSG:4326), weil folium das braucht

Ausfuehren:   python scripts/hole_geodaten.py
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
import shapely

WURZEL = Path(__file__).resolve().parent.parent
URL = ("https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/"
       "swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip")
ROH = WURZEL / "daten" / "geo" / "_roh" / "swissboundaries3d_2026-01.gpkg.zip"
ZIEL = WURZEL / "daten" / "geo" / "gemeinden_2087.geojson"
EBENE = "tlm_hoheitsgebiet"
TOLERANZ_M = 100


def hole_roh() -> None:
    if ROH.exists():
        print(f"  Rohdatei schon vorhanden: {ROH.relative_to(WURZEL)}")
        return
    ROH.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Lade {URL.rsplit('/', 1)[-1]} ...")
    r = requests.get(URL, timeout=900)
    r.raise_for_status()
    ROH.write_bytes(r.content)
    print(f"  {ROH.relative_to(WURZEL)}  {len(r.content):,} Byte")


def baue_geojson() -> None:
    tabelle = pd.read_csv(WURZEL / "daten" / "verbunden" / "strompreise_gemeinden.csv")
    unsere = set(tabelle["gemeinde_nr"])

    pfad = f"/vsizip/{ROH}/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
    g = gpd.read_file(pfad, layer=EBENE,
                      columns=["bfs_nummer", "name", "kantonsnummer", "objektart"])
    print(f"  Ebene {EBENE}: {len(g)} Objekte")

    g = g[g["bfs_nummer"].isin(unsere)].copy()
    print(f"  Davon unsere Gemeinden: {len(g)} "
          f"(eindeutige Nummern: {g['bfs_nummer'].nunique()})")

    fehlend = sorted(unsere - set(g["bfs_nummer"]))
    if fehlend:
        raise SystemExit(f"ABBRUCH: {len(fehlend)} Gemeinden ohne Geometrie: {fehlend}")

    g["geometry"] = shapely.force_2d(g.geometry)          # Hoehe weg, wird nicht gebraucht
    g["geometry"] = g.geometry.simplify(TOLERANZ_M)       # in Metern, weil LV95
    g = g.to_crs(4326)                                    # folium rechnet in WGS84

    leer = int(g.geometry.is_empty.sum())
    ungueltig = int((~g.geometry.is_valid).sum())
    print(f"  Nach dem Vereinfachen: {leer} leere, {ungueltig} ungueltige Geometrien")

    g = g.rename(columns={"bfs_nummer": "gemeinde_nr"})[["gemeinde_nr", "name", "geometry"]]
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    g.to_file(ZIEL, driver="GeoJSON", COORDINATE_PRECISION=5)
    print(f"  {ZIEL.relative_to(WURZEL)}  {ZIEL.stat().st_size:,} Byte")


def main() -> None:
    print("Gemeindegrenzen von swisstopo:")
    hole_roh()
    baue_geojson()
    print("Fertig.")


if __name__ == "__main__":
    main()
