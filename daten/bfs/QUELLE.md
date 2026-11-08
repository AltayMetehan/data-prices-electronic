# Quelle der BFS-Daten

## regionalportraets_2021.csv

- **Datensatz:** Regionalporträts 2021: Kennzahlen aller Gemeinden
- **Herausgeber:** Bundesamt für Statistik (BFS)
- **Bezogen am:** 30.10.2026
- **Download:** https://dam-api.bfs.admin.ch/hub/api/dam/assets/16484444/master
- **Datensatzseite:** https://www.bfs.admin.ch/asset/de/ts-x-21.03.01
- **Katalogeintrag:** https://ckan.opendata.swiss/dataset/regionalportrats-2021-kennzahlen-aller-gemeinden
  (im Browser erreichbar; automatisierte Abfragen beantwortet opendata.swiss mit
  HTTP 403, geprüft am 08.11.2026. Verbindlich ist die BFS-Seite oben.)
- **Datenstand:** 01.01.2021
- **Gemeindegrenzen:** Stand 01.01.2016, swissBOUNDARIES3D © swisstopo
- **Format:** CSV, Semikolon getrennt, UTF-8 mit BOM, CRLF
- **Aufbau:** Langformat, eine Zeile je Region und Indikator

Download zulässig: Die Aufgabenstellung verlangt eigene Erhebung nur für die
Primärquelle. Für die zweite Quelle nennt sie ausdrücklich das Beispiel
«scraped data enriched with data from opendataswiss».

---

## gemeindeverzeichnis_2021.csv und gemeindemutationen_2018_2022.csv

- **Datensatz:** Historisiertes Gemeindeverzeichnis der Schweiz
- **Herausgeber:** Bundesamt für Statistik (BFS)
- **Bezogen am:** 07.11.2026, per `scripts/hole_zusatzdaten.py`
- **Downloads:**
  - Gemeindestand: `https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date=01-01-2021`
  - Mutationen: `https://www.agvchapp.bfs.admin.ch/api/communes/mutations?StartPeriod=01-01-2018&EndPeriod=31-12-2022`
- **Anwendung:** https://www.agvchapp.bfs.admin.ch/de/
- **Lizenz:** OPEN-BY, freie Nutzung mit Quellenangabe, kein Konto nötig
- **Gebietsstand:** frei wählbar; hier 01.01.2021. Zukünftige Stichtage lehnt die
  Schnittstelle ab, der späteste mögliche Stand ist der heutige Tag.
- **Format:** CSV, 140 046 bzw. 22 504 Byte
- **Join-Schlüssel:** `BfsCode` im Gemeindestand, `InitialCode` und `TerminalCode`
  in den Mutationen. Alle Ganzzahl ohne führende Nullen.

### Wofür

Der Gemeindestand 01.01.2021 dient als Kontrolle: Er enthält 2172 Gemeinden, genau
so viele wie die Regionalporträts, und alle 2087 unserer Analysemenge.

Die Mutationsdatei löst die vier Gemeinden auf, die in den Raumgliederungen 2019
fehlen, weil sie erst 2020 und 2021 durch Fusion entstanden sind. Jede Zeile
verbindet eine Vorgängergemeinde (`InitialCode`) mit ihrer Nachfolgerin
(`TerminalCode`). Die Merkmale werden von den Vorgängern übernommen, nachdem geprüft
wurde, dass diese übereinstimmen.
