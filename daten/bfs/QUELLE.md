# Source of the FSO data

## regionalportraets_2021.csv

- **Dataset:** «Regionalporträts 2021: Kennzahlen aller Gemeinden» — the German
  edition, which is the one downloaded. The FSO publishes the same product in
  English as «Regional portraits 2021: communes».
- **Publisher:** Federal Statistical Office, FSO (German: «Bundesamt für
  Statistik BFS»)
- **Retrieved on:** 30 October 2026
- **Download:** https://dam-api.bfs.admin.ch/hub/api/dam/assets/16484444/master
- **Dataset page:** https://www.bfs.admin.ch/asset/de/ts-x-21.03.01
- **Catalogue entry:** https://ckan.opendata.swiss/dataset/regionalportrats-2021-kennzahlen-aller-gemeinden
  (reachable in a browser; opendata.swiss answers automated requests with
  HTTP 403, checked on 8 November 2026. The FSO page above is authoritative.)
- **Data as at:** 1 January 2021
- **Municipal boundaries:** as at 1 January 2016, swissBOUNDARIES3D © swisstopo
- **Format:** CSV, semicolon separated, UTF-8 with BOM, CRLF
- **Structure:** long format, one row per region and indicator

Downloading is permissible here: the assignment requires collecting the data
ourselves only for the primary source. For the second source it explicitly gives
the example «scraped data enriched with data from opendataswiss».

---

## gemeindeverzeichnis_2021.csv and gemeindemutationen_2018_2022.csv

- **Dataset:** «Historisiertes Gemeindeverzeichnis der Schweiz» — the historicized
  list of the Swiss official commune register
- **Publisher:** Federal Statistical Office (FSO)
- **Retrieved on:** 7 November 2026, via `scripts/hole_zusatzdaten.py`
- **Downloads:**
  - Register snapshot: `https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date=01-01-2021`
  - Changes: `https://www.agvchapp.bfs.admin.ch/api/communes/mutations?StartPeriod=01-01-2018&EndPeriod=31-12-2022`
- **Application:** https://www.agvchapp.bfs.admin.ch/de/
- **Licence:** OPEN-BY, free use with attribution, no account required
- **Territorial status** (German: «Gebietsstand»)**:** freely selectable; 1 January
  2021 is used here. The interface rejects future reference dates, the latest
  possible status is the current day.
- **Format:** CSV, 140,046 and 22,504 bytes respectively
- **Join keys:** `BfsCode` in the register snapshot, `InitialCode` and
  `TerminalCode` in the changes file. All integers without leading zeros.

### What it is used for

The register snapshot of 1 January 2021 serves as a cross-check: it contains 2,172
municipalities, exactly as many as the regional portraits, and all 2,087 of our
analysis set.

The changes file resolves the four municipalities that are missing from the
Spatial divisions 2019 because they were only created in 2020 and 2021 through
mergers. Each row links a predecessor municipality (`InitialCode`) to its
successor (`TerminalCode`). The characteristics are taken over from the
predecessors, after checking that these agree with one another.
