"""
Fetches the municipal boundaries from swisstopo and builds a small geometry file
for our 2,087 municipalities from them.

Source: swissBOUNDARIES3D, edition 2026-01, layer tlm_hoheitsgebiet.
The raw file is about 36 MB compressed and 74 MB uncompressed. It is NOT placed
in the repository but fetched into daten/geo/_roh/, which .gitignore excludes.

Only daten/geo/gemeinden_2087.geojson ends up in the repository:
  - only our 2,087 municipalities
  - without the Z dimension
  - simplified with a tolerance of 100 m
  - reprojected from LV95 (EPSG:2056) to WGS84 (EPSG:4326), because folium needs it

Run with:   python scripts/hole_geodaten.py
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
        print(f"  Raw file already present: {ROH.relative_to(WURZEL)}")
        return
    ROH.parent.mkdir(parents=True, exist_ok=True)
    print(f"  Downloading {URL.rsplit('/', 1)[-1]} ...")
    r = requests.get(URL, timeout=900)
    r.raise_for_status()
    ROH.write_bytes(r.content)
    print(f"  {ROH.relative_to(WURZEL)}  {len(r.content):,} bytes")


def baue_geojson() -> None:
    tabelle = pd.read_csv(WURZEL / "daten" / "verbunden" / "strompreise_gemeinden.csv")
    unsere = set(tabelle["gemeinde_nr"])

    pfad = f"/vsizip/{ROH}/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
    g = gpd.read_file(pfad, layer=EBENE,
                      columns=["bfs_nummer", "name", "kantonsnummer", "objektart"])
    print(f"  Layer {EBENE}: {len(g)} objects")

    g = g[g["bfs_nummer"].isin(unsere)].copy()
    print(f"  Of which our municipalities: {len(g)} "
          f"(distinct numbers: {g['bfs_nummer'].nunique()})")

    fehlend = sorted(unsere - set(g["bfs_nummer"]))
    if fehlend:
        raise SystemExit(f"ABORT: {len(fehlend)} municipalities without geometry: {fehlend}")

    g["geometry"] = shapely.force_2d(g.geometry)          # drop height, not needed
    g["geometry"] = g.geometry.simplify(TOLERANZ_M)       # in metres, because LV95
    g = g.to_crs(4326)                                    # folium works in WGS84

    leer = int(g.geometry.is_empty.sum())
    ungueltig = int((~g.geometry.is_valid).sum())
    print(f"  After simplifying: {leer} empty, {ungueltig} invalid geometries")

    g = g.rename(columns={"bfs_nummer": "gemeinde_nr"})[["gemeinde_nr", "name", "geometry"]]
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    g.to_file(ZIEL, driver="GeoJSON", COORDINATE_PRECISION=5)
    print(f"  {ZIEL.relative_to(WURZEL)}  {ZIEL.stat().st_size:,} bytes")


def main() -> None:
    print("Municipal boundaries from swisstopo:")
    hole_roh()
    baue_geojson()
    print("Done.")


if __name__ == "__main__":
    main()
