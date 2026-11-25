# Source of the municipal boundaries

## gemeinden_2087.geojson

Derived from **swissBOUNDARIES3D**, not collected by us.

- **Dataset:** swissBOUNDARIES3D, edition **2026-01**, layer `tlm_hoheitsgebiet`
- **Publisher:** swisstopo, the Federal Office of Topography
- **Retrieved on:** 7 November 2026, via `scripts/hole_geodaten.py`
- **Download of the raw file:** https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip
- **Product page:** https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
- **Licence:** free geodata from swisstopo. Use, distribution, modification and
  commercial use are all permitted; **attribution is mandatory**. No account and
  no registration required.
  Terms of use: https://www.swisstopo.admin.ch/de/nutzungsbedingungen-kostenlose-geodaten-und-geodienste
- **Prescribed attribution:** one of six equivalent forms. We use **`©swisstopo`**
  (written exactly like that, without a space), whose spelled-out German form is
  «Bundesamt für Landestopografie swisstopo». The attribution appears inside the
  image on both maps.
- **Join key:** `bfs_nummer`, integer, called `gemeinde_nr` in our data

### What was done with the raw data

The raw file is 36 MB compressed and 74 MB uncompressed, and is **not** kept in
the repository; `.gitignore` excludes `daten/geo/_roh/`. `scripts/hole_geodaten.py`
produces the file in this folder from it:

1. only the 2,087 municipalities of our analysis set, verified: **all 2,087 are
   present in edition 2026-01, no gaps**
2. Z dimension removed, it is not needed for a map of areas
3. outlines simplified with a tolerance of 100 m, computed in LV95, where metres
   really are metres
4. reprojected to WGS84 (EPSG:4326), because web maps expect it
5. coordinates rounded to five decimal places, roughly 1 m of precision

Result: 1,869,294 bytes instead of 74 MB, 0 empty and 0 invalid geometries.

### Limitation

Every polygon is simplified on its own. A boundary line shared by two neighbours
is therefore not treated identically on both sides, and arithmetically tiny gaps
can appear. At the scale of the whole of Switzerland this is not visible; for a
map of a single district one would have to simplify more finely.
