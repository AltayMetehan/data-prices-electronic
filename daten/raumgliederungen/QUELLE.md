# Source of the spatial division data

## raumgliederungen_2019.xlsx

- **Dataset:** «Die Raumgliederungen der Schweiz 2019» — the German edition, which
  is the one downloaded. The FSO's English name for this topic is «Spatial
  divisions».
- **Publisher:** Federal Statistical Office, FSO (German: «Bundesamt für
  Statistik BFS»)
- **Retrieved on:** 7 November 2026, via `scripts/hole_zusatzdaten.py`
- **Download:** https://dam-api.bfs.admin.ch/hub/api/dam/assets/9046166/master
- **Information page:** https://statistik.admin.ch/de/asset/9046166
- **Licence:** OPEN-BY, free use with attribution, no account required
- **Territorial status** (German: «Gebietsstand»)**:** 1 January 2019
- **Format:** XLSX, 745,506 bytes, sheet `Daten`, 2,212 municipalities, 30 columns
- **Join key:** column `BFS Gde-nummer`, integer without leading zeros

### Why this source

Neither the ElCom price data nor the FSO regional portraits contain the canton,
the language region or the municipality typology. This single file supplies all
three.

### Columns used

The names on the left are the column headings inside the XLSX file and are
reproduced exactly as they appear there, in German.

| Column in the file | Column in our data |
|---|---|
| `BFS Gde-nummer` | `gemeinde_nr` (join key) |
| `Kantons-nummer` | `kanton_nr` |
| `Kanton` | `kanton` |
| `Sprachgebiete` | `sprachregion` (code translated into a label) |
| `Gemeindetypologie 2012 (9 Typen)` | `gemeindetyp_9` |

Code list of the language regions, taken from sheet `CH1+CL_SPRGEB+2011.2` of the
file: 1 = `Deutsch`, 2 = `Französisch`, 3 = `Italienisch`, 4 = `Rätoromanisch`.

These four labels are **data values** and stay German in the CSV, in SQLite and in
PostgreSQL. Only when they are displayed in a chart or a table are they renamed to
German, French, Italian and Romansh, immediately before drawing. See `glossar.md`,
section 0b.

### Limitation

The territorial status is 1 January 2019, while our analysis set is from 2021.
Four of our 2,087 municipalities were created through mergers in 2020 and 2021 and
are therefore missing. They are resolved through the historicized list of the
Swiss official commune register, see `daten/bfs/QUELLE.md` and
`dokumentation_integration_lenny.md`.
