# Punkteliste

Data Analytics, ZHAW, HS2026 · Gruppe Frei / Metehan / Sub Raj
Stand: 8. November 2026

Diese Liste gehört in den Anhang des Präsentations-PDF. Die Aufgabenstellung verlangt
das ausdrücklich:

> «IMPORTANT!!! In the appendix of the PDF document of the presentation, include what
> you think you did to earn the points. Use screenshots and code snippets to clearly
> demonstrate this. Note that the final evaluation will be made by the lecturer, not
> exclusively based on your listing!»

Der Wortlaut der Anforderungen ist aus `moodle_aufgabenstellung.pdf` übernommen, nicht
aus unserer Projektanleitung.

**Stand-Legende:** ✅ erfüllt · 🟡 teilweise · ⬜ offen · ❔ nicht belegbar

---

## Pflicht, 9 Punkte

### Pflicht 1 ⬜→✅ Datenbeschaffung · Metehan

> «Data collection using Web Scraping and/or a Web API. The data must be collected by
> the group itself; ready-made datasets (e.g. from Kaggle) are not permitted as the
> primary data source.»

- `scripts/strompreise_holen.py` – SPARQL-Abfrage gegen den LINDAS-Endpunkt
  `https://ld.admin.ch/query`, Cube `https://energy.ld.admin.ch/elcom/electricityprice`
- `query.txt` – die Abfrage einzeln, zum Nachvollziehen
- `daten/strompreise/Daten_Strompreise_{2021,2024,2027}.csv` – 54 210 / 48 187 / 41 440 Zeilen

**Stand: ✅ erfüllt.** Die Spalten von `query.txt` stimmen mit den CSV überein (geprüft).
Ein vollständiger Lauf des Skripts wurde **nicht** nachgerechnet, weil er Netzzugriff
auf LINDAS braucht.

### Pflicht 2 ✅ Zwei Quellen und dokumentierte Integration · Lenny

> «Data preparation and integration: the project must combine data from at least two
> different sources (e.g. scraped data enriched with data from opendataswiss). The
> integration step (matching keys, joining, resolving inconsistencies, number of
> records lost/gained) must be documented.»

| Geforderter Teil | Beleg |
|---|---|
| mindestens zwei Quellen | drei: ElCom, BFS-Regionalporträts, BFS-Raumgliederungen · `dokumentation_integration_lenny.md` §1 |
| matching keys | §2: BFS-Gemeindenummer, Format beider Seiten geprüft, keine führenden Nullen |
| joining | §3 (Pivot), §5 (Join), `scripts/01_daten_bfs_lenny.ipynb` |
| resolving inconsistencies | §6 (Tabelle mit sechs aufgelösten Widersprüchen), §9b (vier Fusionsgemeinden einzeln) |
| records lost/gained | §5: 0 verloren, 0 gewonnen, Trefferquote 100 Prozent · §7: 202 Gemeinden fallen vor dem Join heraus, mit Permutationstest |

**Stand: ✅ erfüllt.** Alle vier geforderten Teile sind belegt. Zusätzlich dokumentiert:
die Zeitebenen der Tabelle (§7b) und die Verzerrungsprüfung der Auswahl (§7).

### Pflicht 3 ✅ SQLite mit SQL aus Python · Metehan

> «Data storage in a SQLite database including SQL queries from within Python.»

- `scripts/02_sqlite_metehan.ipynb`, `sql/strompreise.db` (23 MB)
- Nachgezählt in der Datenbank: **5 Tabellen** (gemeinde 2225, netzbetreiber 609,
  tarif 143 837, indikator 41, kennzahl 89 052 Zeilen) und **2 Views**
  (`v_analyse`, `v_preis_h4`)
- **4 Fremdschlüssel** im Schema, 5 Primärschlüssel
- Im Notebook: 10× `read_sql`, 9× `execute`, 8× `GROUP BY`, 8× `JOIN`, 7× `CASE`

**Stand: ✅ erfüllt.** Das Notebook läuft aus `scripts/` ohne Fehler durch, und seine
Kontrollzelle zeigt 0 Abweichungen gegenüber Lennys Join in allen acht Spalten.

### Pflicht 4 ⬜ Ausführliche EDA · Subraj

> «Rich non-graphical and graphical exploratory data analysis (EDA).»

Kein Notebook `scripts/03_analyse_subraj.ipynb` im Repo.

**Stand: ⬜ offen.**

### Pflicht 5 ⬜ Modellierung über reine Vorhersage hinaus · Subraj

> «Modeling: use of either regression or classification. The research question must go
> beyond a standard prediction task (e.g. include a comparison between groups, regions,
> time periods, or data sources).»

Die Forschungsfrage erfüllt die Zusatzbedingung bereits durch den Vergleich der drei
Jahre 2021, 2024 und 2027 (Projektanleitung, Abschnitt 1). Das Modell selbst fehlt.

**Stand: ⬜ offen.** Die Datengrundlage liegt vor: `daten/verbunden/strompreise_gemeinden.csv`
mit 2087 Zeilen und 17 Spalten.

### Pflicht 6 ⬜ Modellgüte · Subraj

> «Model evaluation using suitable measures of fit (e.g. r-squared, RMSE, accuracy,
> recall, precision, ...).»

**Stand: ⬜ offen.**

### Pflicht 7 ⬜ Korrekte Interpretation · Subraj

> «Correct interpretation of model results and measures of fit.»

Vorgearbeitet ist der methodische Vorbehalt in Abschnitt 5b der Projektanleitung: Die
Preise werden pro Netzbetreiber gesetzt, die effektive Fallzahl liegt bei rund 500
statt 2087, und p-Werte wirken dadurch stärker als sie sind.

**Stand: ⬜ offen.**

### Pflicht 8 🟡 Dokumentation der AI-Nutzung · alle, Lenny bündelt

> «Documentation of AI usage for creating the code and the presentation (the use of AI
> is not only allowed but desired), including the advantages and disadvantages you
> found and where something did not work with the help of AI.»

| Teil | Beleg |
|---|---|
| Lenny | `ai-doku/ai_dokumentation_lenny.md` – 11 dokumentierte Fehlschläge mit Datum, dazu Abschnitte «Was gut funktioniert hat» und «Was mühsam war» |
| Metehan | `ai-doku/AI-Dokumentation_Datenbeschaffung_Metehan.md`, `ai-doku/AI-Dokumentation_SQLite_Metehan.md` |
| Subraj | fehlt |

**Stand: 🟡 teilweise.** Was fehlt:
1. Subrajs Notizen
2. die Bündelung aller drei zu einem Dokument
3. der Teil «and the presentation» – es gibt noch keine Präsentation

### Pflicht 9 ⬜ Material auf Moodle · Subraj

> «Making the material (data, Jupyter notebooks, ...) available on Moodle.»

Abgabe im Januar: `materials_group_XX.zip`. Die Gruppennummer ist noch offen.

**Stand: ⬜ offen.**

---

## Bonus, maximal 6 Punkte

### Bonus 1 🟡 Kreativität · alle

> «Creativity of implementation (creative is anything not specified in the lessons and
> exercises).»

Was in den Lektionen und Übungen **nicht** vorkam:

| Was | Beleg | Warum nicht im Unterricht |
|---|---|---|
| **Karte in Python** statt in QGIS | `scripts/01_daten_bfs_lenny.ipynb`, Kartenabschnitt; `abbildungen/*.png`, `karten/*.html` | Woche 5 unterrichtete Choroplethenkarten in QGIS mit Screenshots als Abgabe; geopandas stand nur als Literaturquelle in der Liste |
| **Maschinelle Auflösung von Gemeindefusionen** über die Mutationstabelle des historisierten Gemeindeverzeichnisses | `scripts/01_daten_bfs_lenny.ipynb`; `dokumentation_integration_lenny.md` §9b | Der Unterricht behandelt Joins, nicht Gebietsstände und Mutationsnummern |
| **Varianzzerlegung nach Netzbetreibern** statt nach Gemeinden | Projektanleitung Abschnitt 5b; Kartenabschnitt des Notebooks | Die Frage nach der richtigen Aggregationsebene kam nicht vor |
| **Permutationstest** auf Auswahlverzerrung, 20 000 Ziehungen | `scripts/01_daten_bfs_lenny.ipynb`; `dokumentation_integration_lenny.md` §7 | Unterrichtet wurden t-Test, ANOVA, Chi-Quadrat; ein verteilungsfreier Resampling-Test nicht |
| **SPARQL** gegen einen Linked-Data-Endpunkt | `scripts/strompreise_holen.py`, `query.txt` | Der Unterricht behandelt Web Scraping und REST-APIs, kein SPARQL |

**Stand: 🟡 teilweise.** Die Techniken existieren und sind belegt. Sie sind bis jetzt
aber nirgends **beansprucht** – diese Liste ist der erste Ort. Vollständig wird der
Punkt erst, wenn sie im Anhang des Präsentations-PDF mit Screenshots und
Code-Ausschnitten steht.

### Bonus 2 ⬜ PostgreSQL · Metehan

> «Use of a PostgreSQL or similar database (no SQLite!) with, e.g. SQL joins and
> aggregations from within Python.»

**Stand: ⬜ offen.** Im Repo findet sich nichts zu PostgreSQL.

### Bonus 3 ✅ Geodaten integrieren und visualisieren · Lenny

> «Integration and visualization of geographical data.»

| Teil | Beleg |
|---|---|
| Integration | `daten/geo/gemeinden_2087.geojson`, über `gemeinde_nr` mit der Preistabelle verbunden; `scripts/hole_geodaten.py` |
| Visualisierung, statisch | `abbildungen/karte_preisniveau_2027.png`, `abbildungen/karte_veraenderung_2021_2027.png`, je 300 dpi |
| Visualisierung, interaktiv | `karten/karte_preisniveau_2027.html`, `karten/karte_veraenderung_2021_2027.html`, mit Tooltip |
| Quelle und Lizenz | `daten/geo/QUELLE.md`, swissBOUNDARIES3D ©swisstopo, Quellenangabe im Bild |

Geprüft: Alle 2087 Gemeinden haben eine Geometrie, 0 leere und 0 ungültige nach dem
Vereinfachen.

**Stand: ✅ erfüllt.** Die Karte beantwortet zusätzlich eine inhaltliche Frage: Der
Netzbetreiber erklärt 94 bis 97 Prozent der Preisstreuung, der Kanton 23 bis 60, die
Sprachregion 0.4 bis 3.0.

### Bonus 4 ⬜ Chi-Quadrat, ANOVA oder Korrelation mit p-Wert · Subraj

> «Use of a Chi-squared test, analysis of variance (ANOVA), or correlation analysis
> (each test must include a p-value).»

Vorhanden ist ein **Permutationstest** mit p-Werten
(`dokumentation_integration_lenny.md` §7). Er ist aber keiner der drei genannten
Tests und deckt den Punkt deshalb nicht ab.

**Stand: ⬜ offen.** Die Daten für eine ANOVA über Kantone und Sprachregionen liegen
seit dem 7. November bereit.

### Bonus 5 ⬜ k-means · Subraj

> «Use of k-means clustering in addition to the regression or classification model.»

**Stand: ⬜ offen.**

### Bonus 6 🟡 Öffentliches GitHub-Repo · Metehan

> «Code on a publicly available GitHub repository (provide the GitHub project URL in
> the project presentation).»

- Repo: https://github.com/AltayMetehan/data-prices-electronic
- Sichtbarkeit geprüft am 08.11.2026: **PUBLIC**

**Stand: 🟡 teilweise.** Das Repo ist öffentlich. Die URL muss zusätzlich **in der
Präsentation** genannt werden; die Präsentation existiert noch nicht.

---

## Video, maximal 7 Punkte · alle drei

> «Project presentation in the form of a video recording (max. 7 points)»

| Nr | Kriterium | Stand |
|---|---|---|
| 1 | Structure & outline | ⬜ |
| 2 | Topic presentation | ⬜ |
| 3 | Content | ⬜ |
| 4 | Language / auxiliary tools (freely spoken) | ⬜ |
| 5 | Quality of the presentation & slides | ⬜ |
| 6 | **Reflection on AI usage** – die Folien **und** das Video müssen zeigen, welche AI-Werkzeuge wofür eingesetzt wurden, welche Vorteile und Nachteile auffielen und wo etwas nicht funktioniert hat | ⬜ Grundlage vorhanden: `ai-doku/ai_dokumentation_lenny.md` |
| 7 | Time keeping: Minuten = Anzahl Studierende × 5, bei uns 15 Minuten | ⬜ |

**Stand: ⬜ offen.** Kriterium 6 ist eine eigene Anforderung **zusätzlich** zu Pflicht 8.

---

## Zusammenzug

| | erfüllt | teilweise | offen |
|---|---|---|---|
| Pflicht (9) | 3 | 1 | 5 |
| Bonus (6) | 1 | 2 | 3 |
| Video (7 Pkt) | – | – | alle |

**Lennys Teil:** Pflicht 2 ✅, Bonus 3 ✅, Pflicht 8 🟡 (Bündelung und Präsentationsteil
fehlen), Bonus 1 🟡 (beansprucht, aber noch nicht im PDF-Anhang).

**Was nicht belegbar ist:** Ob Metehans Beschaffungsskript bei einem Lauf exakt die
Dateien im Repo erzeugt – das wurde nicht nachgerechnet, weil es Netzzugriff braucht.
