# Quelle der Raumgliederungsdaten

## raumgliederungen_2019.xlsx

- **Datensatz:** Die Raumgliederungen der Schweiz 2019
- **Herausgeber:** Bundesamt für Statistik (BFS)
- **Bezogen am:** 07.11.2026, per `scripts/hole_zusatzdaten.py`
- **Download:** https://dam-api.bfs.admin.ch/hub/api/dam/assets/9046166/master
- **Infoseite:** https://statistik.admin.ch/de/asset/9046166
- **Lizenz:** OPEN-BY, freie Nutzung mit Quellenangabe, kein Konto nötig
- **Gebietsstand:** 01.01.2019
- **Format:** XLSX, 745 506 Byte, Blatt `Daten`, 2212 Gemeinden, 30 Spalten
- **Join-Schlüssel:** Spalte `BFS Gde-nummer`, Ganzzahl ohne führende Nullen

### Warum diese Quelle

Weder die ElCom-Preisdaten noch die BFS-Regionalporträts enthalten Kanton,
Sprachregion oder Gemeindetypologie. Diese eine Datei liefert alle drei.

### Verwendete Spalten

| Spalte in der Datei | Spalte bei uns |
|---|---|
| `BFS Gde-nummer` | `gemeinde_nr` (Join-Schlüssel) |
| `Kantons-nummer` | `kanton_nr` |
| `Kanton` | `kanton` |
| `Sprachgebiete` | `sprachregion` (Code in Label übersetzt) |
| `Gemeindetypologie 2012 (9 Typen)` | `gemeindetyp_9` |

Codeliste der Sprachgebiete, aus dem Blatt `CH1+CL_SPRGEB+2011.2` der Datei:
1 = Deutsch, 2 = Französisch, 3 = Italienisch, 4 = Rätoromanisch.

### Einschränkung

Der Gebietsstand ist 01.01.2019, unsere Analysemenge stammt von 2021. Vier unserer
2087 Gemeinden sind 2020 und 2021 durch Fusion entstanden und fehlen deshalb. Sie
werden über das historisierte Gemeindeverzeichnis aufgelöst, siehe
`daten/bfs/QUELLE.md` und `dokumentation_integration_lenny.md`.
