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
scripts/             Beschaffungsskript und Notebooks 01 bis 04
sql/                 SQLite-Datenbank und das PostgreSQL-     (Metehan)
                     Notebook 03_postgresql.ipynb
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

Die vier Notebooks in `scripts/` bestimmen die Repo-Wurzel selber (`finde_wurzel`)
und leiten alle Pfade davon ab. Sie laufen deshalb sowohl aus `scripts/` als auch aus
der Repo-Wurzel.

**Eine Ausnahme:** `sql/03_postgresql.ipynb` verwendet einen relativen Pfad
(`sqlite3.connect("strompreise.db")`) und läuft nur, wenn man es aus `sql/` startet.
Geprüft am 22.11.2026.

**Wer Dateien verschiebt**, zieht die Pfade in allen Notebooks und in
`scripts/strompreise_holen.py` nach und lässt sie einmal komplett durchlaufen. Am
07.11.2026 wurde die Struktur umgebaut, ohne die Pfade nachzuziehen – danach brachen
zwei Notebooks auf einem frischen Klon ab.

## Projekt aufsetzen

**Python 3.11 wird vorausgesetzt.** Entwickelt und geprüft auf 3.11.4. Der Pin
`scipy>=1.17.1,<1.18` in der `requirements.txt` ist nötig, weil scipy ab 1.18
Python 3.12 verlangt; mit einer höheren Version schlägt die Installation auf 3.11
fehl, bevor ein Notebook startet.

```bash
python3 --version          # muss 3.11.x anzeigen
git clone https://github.com/AltayMetehan/data-prices-electronic.git
cd data-prices-electronic
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Danach laufen vier der fünf Notebooks ohne weitere Vorbereitung, jedes aus dem
Verzeichnis, in dem es liegt:

```bash
cd scripts && jupyter nbconvert --to notebook --execute --inplace 01_daten_bfs_lenny.ipynb
```

Geprüft am 22.11.2026 auf einem frischen Klon mit frischer virtueller Umgebung:
`01`, `02`, `03` und `04` laufen fehlerfrei durch.

### PostgreSQL, für `sql/03_postgresql.ipynb`

Dieses Notebook braucht zusätzlich einen **laufenden PostgreSQL-Server** auf
`localhost:5432` mit einer Datenbank `strompreise` und dem Benutzer `postgres`. Das
Passwort liest es aus der Umgebungsvariablen `PGPASSWORD`; ist sie nicht gesetzt,
fragt es interaktiv danach und kann dann nicht automatisch durchlaufen.

> **Offen:** Wie der Server installiert und die Datenbank angelegt wird, ist noch
> nicht dokumentiert. **Metehan trägt diese Anleitung nach.** Ohne sie lässt sich
> Bonus 2 von aussen nicht nachvollziehen.

## Stand

- Letzte Änderung: 22.11.2026
- **Fertig:** Datenbeschaffung und SQLite (Metehan), Join der drei Quellen mit
  Kanton, Sprachregion und Gemeindetypologie sowie Geodaten und Karten (Lenny),
  EDA mit statistischen Tests und Modell mit k-means (Subraj), PostgreSQL (Metehan)
- **Als Nächstes:** Konzept-Präsentation am 8. Dezember, danach Bericht, Video und
  Abgabe. Offene Punkte stehen in `CLAUDE Data Analytics.md`, Abschnitt 11, und in
  `punkteliste.md`.
