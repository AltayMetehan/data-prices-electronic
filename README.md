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

**Alle fünf Notebooks** bestimmen die Repo-Wurzel selber und leiten ihre Pfade davon
ab. Sie laufen deshalb sowohl aus ihrem eigenen Verzeichnis als auch aus der
Repo-Wurzel. Geprüft am 22.11.2026 für `sql/03_postgresql.ipynb` aus beiden Orten.

**Wer Dateien verschiebt**, zieht die Pfade in allen Notebooks und in
`scripts/strompreise_holen.py` nach und lässt sie einmal komplett durchlaufen. Am
07.11.2026 wurde die Struktur umgebaut, ohne die Pfade nachzuziehen – danach brachen
zwei Notebooks auf einem frischen Klon ab.

## Projekt aufsetzen

**Python 3.11 wird vorausgesetzt.** Entwickelt und geprüft auf 3.11.4. Die
Obergrenze `scipy<1.18` in der `requirements.txt` ist zwingend, weil scipy ab 1.18
Python 3.12 verlangt; ohne sie schlägt die Installation auf 3.11 fehl, bevor ein
Notebook startet.

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

Das fünfte Notebook, `sql/03_postgresql.ipynb`, braucht zusätzlich einen laufenden
PostgreSQL-Server. Dazu der nächste Abschnitt.

## PostgreSQL einrichten

1. PostgreSQL 17 fuer Windows installieren (winget:
   `winget install --id PostgreSQL.PostgreSQL.17 --exact`).
   Beim Installer den Benutzernamen `postgres` und ein eigenes Passwort festlegen.
2. In pgAdmin oder im SQL-Terminal die Datenbank `strompreise` mit folgendem Befehl
   anlegen:
   ```sql
   CREATE DATABASE strompreise;
   ```
   Falls das Projekt ein eigenes Datenbankkonto verwenden soll:
   ```sql
   CREATE USER strompreise_app WITH PASSWORD 'ein-eigenes-passwort';
   GRANT ALL PRIVILEGES ON DATABASE strompreise TO strompreise_app;
   ```
   Anschliessend das Notebook mit `strompreise_app` ausführen oder PostgreSQL-Standard
   `postgres` verwenden. Das Passwort nie in Dateien oder Git speichern.
3. Abhaengigkeiten installieren:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Verbindung lokal setzen, ohne interaktive Abfrage:
   ```powershell
   $env:PGHOST="localhost"
   $env:PGPORT="5432"
   $env:PGDATABASE="strompreise"
   $env:PGUSER="postgres"
   $env:PGPASSWORD="das-eigene-passwort"
   jupyter notebook sql/03_postgresql.ipynb
   ```
   Die Variablen koennen pro Terminal gesetzt werden. Das Notebook liest ausschliesslich
   Umgebungsvariablen; fehlende Einstellungen fuehren zu einer klaren Fehlermeldung.

### PostgreSQL unter macOS und Linux

Die Schritte oben gelten für Windows. Unter macOS und Linux unterscheiden sich nur
Installation, Start des Dienstes und das Setzen der Umgebungsvariablen. Schritt 2
(`CREATE DATABASE`, optional eigener Benutzer) bleibt gleich.

**macOS (Homebrew)**
```bash
brew install postgresql@17
brew services start postgresql@17
# postgresql@17 ist keg-only: psql und createdb liegen nicht automatisch im PATH
echo 'export PATH="$(brew --prefix postgresql@17)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
# Homebrew legt als Superuser den eigenen macOS-Benutzer an, nicht postgres:
createdb strompreise
psql -d strompreise -c "ALTER USER $(whoami) WITH PASSWORD 'das-eigene-passwort';"
```
Alternativ Postgres.app (postgresapp.com) installieren und starten. Danach als
`PGUSER` den eigenen macOS-Benutzernamen verwenden.

**Linux (Debian/Ubuntu)**
```bash
sudo apt install postgresql
sudo systemctl enable --now postgresql
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'das-eigene-passwort';"
sudo -u postgres createdb strompreise
```
Fedora: `sudo dnf install postgresql-server`, dann `sudo postgresql-setup --initdb`
und `sudo systemctl enable --now postgresql`.

**Abhängigkeiten und Umgebungsvariablen (macOS und Linux)**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=strompreise
export PGUSER=postgres          # macOS/Homebrew: export PGUSER=$(whoami)
export PGPASSWORD='das-eigene-passwort'
jupyter notebook sql/03_postgresql.ipynb
```
Die `export`-Zeilen gelten nur im aktuellen Terminal und gehören nicht in Dateien,
die committet werden.

## Stand

- Letzte Änderung: 22.11.2026
- **Fertig:** Datenbeschaffung und SQLite (Metehan), Join der drei Quellen mit
  Kanton, Sprachregion und Gemeindetypologie sowie Geodaten und Karten (Lenny),
  EDA mit statistischen Tests und Modell mit k-means (Subraj), PostgreSQL (Metehan)
- **Als Nächstes:** Konzept-Präsentation am 8. Dezember, danach Bericht, Video und
  Abgabe. Offene Punkte stehen in `CLAUDE Data Analytics.md`, Abschnitt 11, und in
  `punkteliste.md`.
