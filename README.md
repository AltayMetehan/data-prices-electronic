# Strompreise der Schweizer Gemeinden

Gruppenprojekt im Modul Data Analytics, ZHAW, HS2026.

**Forschungsfrage:** Welche Merkmale einer Gemeinde erklären die Höhe ihres
Strompreises für Haushalte, und haben sich diese Zusammenhänge mit dem
Preisanstieg 2023 verändert?

**Daten**
- Strompreise pro Gemeinde: ElCom über den SPARQL-Endpunkt von LINDAS
- Gemeindedaten: Bundesamt für Statistik
- Verglichene Jahre: 2021, 2024, 2027

**Gruppe:** Lenny Frei, Altay Metehan, Singh Sub Raj

Projektanleitung siehe `CLAUDE Data Analytics.md`,
Anforderungen siehe `moodle_aufgabenstellung.pdf`.

## Ordnerstruktur

```
daten/strompreise/   ElCom-Rohdaten, eine CSV pro Jahr        (Metehan)
daten/bfs/           BFS-Gemeindedaten mit Herkunftsnachweis  (Lenny)
daten/verbunden/     die verbundene Tabelle für alle drei     (Lenny)
scripts/             Beschaffungsskript und Notebooks
sql/                 SQLite-Datenbank                         (Metehan)
daten/geo/           Gemeindegrenzen als GeoJSON              (Lenny)
abbildungen/         Karten als PNG für die Präsentation      (Lenny)
karten/              interaktive Karten als HTML              (Lenny)
ai-doku/             AI-Dokumentation der drei Teammitglieder
```

Zwei Arten von Dateien werden bei jedem Lauf neu erzeugt und unterscheiden sich
danach in den Bytes, auch wenn sich inhaltlich nichts geändert hat:

- `sql/strompreise.db`, gebaut von `scripts/02_sqlite_metehan.ipynb`
- `karten/*.html`, gebaut von `scripts/01_daten_bfs_lenny.ipynb`; folium vergibt bei
  jedem Durchlauf neue zufällige Element-IDs

Beide nur committen, wenn sich an den Daten wirklich etwas geändert hat, nicht nach
jedem Durchlauf.

Aus demselben Grund zeigt das Notebook die interaktiven Karten **nicht** inline an,
sondern schreibt sie nur nach `karten/`. Eingebettet würden sie das Notebook bei
jedem Lauf um rund 4 MB vergrössern.

Die Notebooks in `scripts/` bestimmen die Repo-Wurzel selber und leiten alle Pfade
davon ab. Sie laufen deshalb sowohl aus `scripts/` als auch aus der Repo-Wurzel.

**Wer Dateien verschiebt**, zieht die Pfade in beiden Notebooks und in
`scripts/strompreise_holen.py` nach und lässt beide Notebooks einmal komplett
durchlaufen. Am 07.11.2026 wurde die Struktur umgebaut, ohne die Pfade nachzuziehen –
danach brachen beide Notebooks auf einem frischen Klon ab.

## Stand

- Letzte Änderung: 07.11.2026
- Fertig: Datenbeschaffung (Metehan), Join der drei Quellen inklusive Kanton,
  Sprachregion und Gemeindetypologie (Lenny), SQLite (Metehan),
  Geodaten und Karten (Lenny)
- Als Nächstes: EDA und Statistik (Subraj), PostgreSQL (Metehan)
