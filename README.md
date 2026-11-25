# Electricity prices of Swiss municipalities

Group project in the Data Analytics module, ZHAW, autumn semester 2026.

**Research question:** Which characteristics of a municipality explain the level of
its household electricity price, and did these relationships change with the price
rise of 2023?

**Data**
- Electricity prices per municipality: ElCom via the LINDAS SPARQL endpoint
- Municipality data: Federal Statistical Office (FSO)
- Years compared: 2021, 2024, 2027

**Group:** Lenny Frei, Altay Metehan, Singh Sub Raj

Project instructions see `CLAUDE Data Analytics.md`,
requirements see `moodle_aufgabenstellung.pdf`.

## Folder structure

```
daten/strompreise/   ElCom raw data, one CSV per year          (Metehan)
daten/bfs/           FSO municipality data with provenance     (Lenny)
daten/verbunden/     the joined table, for all three of us     (Lenny)
scripts/             collection scripts and notebooks 01 to 04
sql/                 SQLite database and the PostgreSQL        (Metehan)
                     notebook 03_postgresql.ipynb
daten/geo/           municipal boundaries as GeoJSON           (Lenny)
abbildungen/         maps as PNG for the presentation          (Lenny)
karten/              interactive maps as HTML                  (Lenny)
ai-doku/             AI documentation of the three of us
```

Two kinds of file are regenerated on every run and differ in their bytes afterwards,
even when nothing has changed in substance:

- `sql/strompreise.db`, built by `scripts/02_sqlite_metehan.ipynb`
- `karten/*.html`, built by `scripts/01_daten_bfs_lenny.ipynb`; folium assigns new
  random element IDs on every run

Commit either of them only when the data really has changed, not after every run.

For the same reason the notebook does **not** display the interactive maps inline,
it only writes them to `karten/`. Embedded, they would grow the notebook file by
about 4 MB on every run.

The four notebooks in `scripts/` determine the repository root themselves
(`finde_wurzel`) and derive every path from it. They therefore run both from
`scripts/` and from the repository root.

**All five notebooks** determine the repository root themselves and derive their
paths from it. They therefore run both from their own directory and from the
repository root. Checked on 22 November 2026 for `sql/03_postgresql.ipynb` from both
places.

**Whoever moves files** updates the paths in all notebooks and in
`scripts/strompreise_holen.py` and lets them run through once completely. On
7 November 2026 the structure was rearranged without updating the paths - after that,
two notebooks broke on a fresh clone.

## Setting up the project

**Python 3.11 is required.** Developed and checked on 3.11.4. The upper bound
`scipy<1.18` in `requirements.txt` is mandatory, because scipy from 1.18 onwards
requires Python 3.12; without it the installation fails on 3.11 before a single
notebook starts.

```bash
python3 --version          # must show 3.11.x
git clone https://github.com/AltayMetehan/data-prices-electronic.git
cd data-prices-electronic
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After that, four of the five notebooks run without further preparation, each from the
directory it lives in:

```bash
cd scripts && jupyter nbconvert --to notebook --execute --inplace 01_daten_bfs_lenny.ipynb
```

Checked on 22 November 2026 on a fresh clone with a fresh virtual environment:
`01`, `02`, `03` and `04` run through without errors.

The fifth notebook, `sql/03_postgresql.ipynb`, additionally needs a running
PostgreSQL server. See the next section.

## Setting up PostgreSQL

1. Install PostgreSQL 17 for Windows (winget:
   `winget install --id PostgreSQL.PostgreSQL.17 --exact`).
   In the installer, set the user name `postgres` and a password of your own.
2. In pgAdmin or in the SQL terminal, create the database `strompreise` with the
   following command:
   ```sql
   CREATE DATABASE strompreise;
   ```
   If the project is to use a database account of its own:
   ```sql
   CREATE USER strompreise_app WITH PASSWORD 'your-own-password';
   GRANT ALL PRIVILEGES ON DATABASE strompreise TO strompreise_app;
   ```
   Then run the notebook as `strompreise_app`, or use the PostgreSQL default
   `postgres`. Never store the password in files or in Git.
3. Install the dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Set the connection locally, without an interactive prompt:
   ```powershell
   $env:PGHOST="localhost"
   $env:PGPORT="5432"
   $env:PGDATABASE="strompreise"
   $env:PGUSER="postgres"
   $env:PGPASSWORD="your-own-password"
   jupyter notebook sql/03_postgresql.ipynb
   ```
   The variables can be set per terminal. The notebook reads environment variables
   exclusively; missing settings lead to a clear error message.

### PostgreSQL on macOS and Linux

The steps above apply to Windows. On macOS and Linux only the installation, the start
of the service and the setting of the environment variables differ. Step 2
(`CREATE DATABASE`, optionally a user of your own) stays the same.

**macOS (Homebrew)**
```bash
brew install postgresql@17
brew services start postgresql@17
# postgresql@17 is keg-only: psql and createdb are not automatically on the PATH
echo 'export PATH="$(brew --prefix postgresql@17)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
# Homebrew creates your own macOS user as the superuser, not postgres:
createdb strompreise
psql -d strompreise -c "ALTER USER $(whoami) WITH PASSWORD 'your-own-password';"
```
Alternatively, install and start Postgres.app (postgresapp.com). Then use your own
macOS user name as `PGUSER`.

**Linux (Debian/Ubuntu)**
```bash
sudo apt install postgresql
sudo systemctl enable --now postgresql
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'your-own-password';"
sudo -u postgres createdb strompreise
```
Fedora: `sudo dnf install postgresql-server`, then `sudo postgresql-setup --initdb`
and `sudo systemctl enable --now postgresql`.

**Dependencies and environment variables (macOS and Linux)**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=strompreise
export PGUSER=postgres          # macOS/Homebrew: export PGUSER=$(whoami)
export PGPASSWORD='your-own-password'
jupyter notebook sql/03_postgresql.ipynb
```
The `export` lines apply only in the current terminal and do not belong in files that
get committed.

## Status

- Last change: 22 November 2026
- **Done:** data collection and SQLite (Metehan), join of the three sources with
  canton, language region and municipality typology as well as geodata and maps
  (Lenny), EDA with statistical tests and model with k-means (Subraj), PostgreSQL
  (Metehan)
- **Next:** concept presentation on 8 December, then report, video and submission.
  Open points are in `CLAUDE Data Analytics.md`, section 11, and in `punkteliste.md`.
