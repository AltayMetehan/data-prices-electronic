# Punkteliste

Data Analytics, ZHAW, HS2026 · Gruppe Frei / Metehan / Sub Raj
Stand: 21. November 2026

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

### Pflicht 1 ✅ Datenbeschaffung · Metehan

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

### Pflicht 4 ✅ Ausführliche EDA · Subraj

> «Rich non-graphical and graphical exploratory data analysis (EDA).»

`scripts/03_analyse_subraj.ipynb`, Abschnitte 1 bis 7

| Geforderter Teil | Beleg |
|---|---|
| nicht-grafisch | Datenqualität (§1), Kennzahlen pro Jahr mit Variationskoeffizient, Schiefe, Kurtosis, Ausreissern (§2.1), Rangkorrelation zwischen den Jahren (§3), Varianzzerlegung nach Preisbestandteilen (§4.2), Korrelationsmatrix der Merkmale (§5.1), Kennzahlen pro Sprachregion (§6.1), eta² nach Netzbetreiber, Kanton und Sprachregion (§7) |
| grafisch | Histogramme und Boxplots der Preise (§2.2, §2.3), Streudiagramme zwischen den Jahren (§3), gestapelte Balken der Bestandteile (§4.1), Histogramme der Merkmale roh und logarithmiert (§5.1), Heatmap der Rangkorrelationen (§5.2), Boxplots nach Sprachregion (§6.1), Preise pro Kanton (§6.2) |

**Stand: ✅ erfüllt.** Jeder Abschnitt hat eine Interpretation. Das Notebook läuft aus
`scripts/` ohne Fehler durch.

### Pflicht 5 ✅ Modellierung über reine Vorhersage hinaus · Subraj

> «Modeling: use of either regression or classification. The research question must go
> beyond a standard prediction task (e.g. include a comparison between groups, regions,
> time periods, or data sources).»

`scripts/04_modell_subraj.ipynb`, Abschnitte 1 bis 5

| Geforderter Teil | Beleg |
|---|---|
| Regression | multiple lineare Regression (OLS), Standardfehler nach Netzbetreiber geclustert (§2) |
| Vergleich über Zeiträume | dasselbe Modell für 2021, 2024 und 2027 (§3); das Modell für den Anstieg testet formal, ob sich ein Zusammenhang verändert hat, weil sein Koeffizient genau die Differenz der Koeffizienten zweier Jahre ist (§3, mit `assert` geprüft) |
| Vergleich zwischen Gruppen und Regionen | Sprachregionen als Dummies (§3), Modell mit Kantonen (§4) |
| Vergleich der Ebenen | Modell auf Ebene der 485 Netzbetreiber (§5) |

**Stand: ✅ erfüllt.**

### Pflicht 6 ✅ Modellgüte · Subraj

> «Model evaluation using suitable measures of fit (e.g. r-squared, RMSE, accuracy,
> recall, precision, ...).»

- R², angepasstes R² und RMSE für alle fünf Zielgrössen, RMSE verglichen mit der
  Standardabweichung (`04_modell_subraj.ipynb` §3)
- Kreuzvalidierung, zufällig und nach Netzbetreiber gruppiert, gegen den Mittelwert als
  Vergleichsmassstab (§6)
- Residuen gegen Vorhersage, Histogramm und Q-Q-Plot (§7)
- Varianzinflationsfaktor gegen Multikollinearität (§1.2)

**Stand: ✅ erfüllt.**

### Pflicht 7 ✅ Korrekte Interpretation · Subraj

> «Correct interpretation of model results and measures of fit.»

Interpretationen nach jedem Abschnitt in `03_analyse_subraj.ipynb` und
`04_modell_subraj.ipynb`, Zwischenfazit (03 §9) und Fazit mit Antwort auf die
Forschungsfrage (04 §9). Der Vorbehalt aus Abschnitt 5b der Projektanleitung ist
umgesetzt: Jeder Test und das Modell sind zusätzlich auf Betreiberebene gerechnet, die
Standardfehler nach Betreiber geclustert. Das negative R² der gruppierten
Kreuzvalidierung ist ausdrücklich gedeutet (04 §6).

**Stand: ✅ erfüllt.**

### Pflicht 8 🟡 Dokumentation der AI-Nutzung · alle, Lenny bündelt

> «Documentation of AI usage for creating the code and the presentation (the use of AI
> is not only allowed but desired), including the advantages and disadvantages you
> found and where something did not work with the help of AI.»

| Teil | Beleg |
|---|---|
| Lenny | `ai-doku/ai_dokumentation_lenny.md` – 11 dokumentierte Fehlschläge mit Datum, dazu Abschnitte «Was gut funktioniert hat» und «Was mühsam war» |
| Metehan | `ai-doku/AI-Dokumentation_Datenbeschaffung_Metehan.md`, `ai-doku/AI-Dokumentation_SQLite_Metehan.md`, `ai-doku/AI-Dokumentation_PostgreSQL_Metehan.md` |
| Subraj | `ai-doku/ai_dokumentation_subraj.md` – Sitzungsprotokoll mit dokumentierten Fehlschlägen, Vorteile, Nachteile |

**Stand: 🟡 teilweise.** Was fehlt:
1. die Bündelung aller drei zu einem Dokument
2. der Teil «and the presentation» bei allen dreien – die Präsentation entsteht ab dem 24. November

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
| **Nach Netzbetreiber geclusterte Standardfehler**, selbst implementiert | `scripts/04_modell_subraj.ipynb` §2 | Der Unterricht rechnet Regressionen mit gewöhnlichen Standardfehlern |
| **Gruppierte Kreuzvalidierung** (GroupKFold) gegen zufällige | `scripts/04_modell_subraj.ipynb` §6 | Kreuzvalidierung kam nur mit zufälligen Folds vor |
| **Alexander-Govern-Test, Tukey-Test, Bonferroni-Korrektur** | `scripts/03_analyse_subraj.ipynb` §8 | Unterrichtet wurde die klassische ANOVA ohne Post-hoc-Test |
| **Cluster-robuster Wald-Test** über die k-means-Cluster | `scripts/04_modell_subraj.ipynb` §8.4 | k-means wurde ohne Test der Unterschiede zwischen Clustern behandelt |
| **SPARQL** gegen einen Linked-Data-Endpunkt | `scripts/strompreise_holen.py`, `query.txt` | Der Unterricht behandelt Web Scraping und REST-APIs, kein SPARQL |

**Stand: 🟡 teilweise.** Die Techniken existieren und sind belegt. Sie sind bis jetzt
aber nirgends **beansprucht** – diese Liste ist der erste Ort. Vollständig wird der
Punkt erst, wenn sie im Anhang des Präsentations-PDF mit Screenshots und
Code-Ausschnitten steht.

### Bonus 2 ✅ PostgreSQL · Metehan

> «Use of a PostgreSQL or similar database (no SQLite!) with, e.g. SQL joins and
> aggregations from within Python.»

- `sql/03_postgresql.ipynb`: überträgt alle 5 Tabellen aus SQLite nach PostgreSQL 16,
  baut die beiden Views nach und rechnet Auswertungen mit `JOIN`, `GROUP BY`, `HAVING`,
  `percentile_cont`, `STDDEV`, `CORR` und den Fensterfunktionen `RANK`, `LAG`, `NTILE`
- Kontrollen: gleiche Zeilenzahl in allen Tabellen, Summe der Bestandteile, Analysetabelle
  gegen SQLite (grösste Abweichung 7e-15)

**Stand: ✅ erfüllt.** Noch nachzuziehen: `psycopg2-binary` fehlt in `requirements.txt`, der
Verweis auf `02_sqlite_datenbank.ipynb` meint `02_sqlite_metehan.ipynb`, und
`strompreise.db` wird mit relativem Pfad geöffnet (läuft nur aus `sql/`).

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

### Bonus 4 ✅ Chi-Quadrat, ANOVA oder Korrelation mit p-Wert · Subraj

> «Use of a Chi-squared test, analysis of variance (ANOVA), or correlation analysis
> (each test must include a p-value).»

| Test | Beleg |
|---|---|
| ANOVA über Sprachregionen und Kantone, mit Levene, Alexander-Govern, Kruskal-Wallis, eta² und Tukey | `scripts/03_analyse_subraj.ipynb` §8.3, §8.4 |
| Korrelation nach Pearson und Spearman mit p-Wert und Bonferroni-Korrektur | `scripts/03_analyse_subraj.ipynb` §8.5, §8.6 |
| ANOVA über die k-means-Cluster, mit cluster-robustem Wald-Test | `scripts/04_modell_subraj.ipynb` §8.4 |

Jeder Test ist auf Gemeinde- und auf Betreiberebene gerechnet. Der gepaarte t-Test
(§8.2) steht zusätzlich im Notebook, zählt für diesen Punkt aber nicht.

**Stand: ✅ erfüllt.**

### Bonus 5 ✅ k-means · Subraj

> «Use of k-means clustering in addition to the regression or classification model.»

`scripts/04_modell_subraj.ipynb` §8: k-means auf Dichte, Fläche und Anteil 65+,
standardisiert; Wahl von k über Ellbogenkriterium und Silhouettenkoeffizient (k = 4);
Profile der vier Gemeindetypen; Kontrolle gegen die BFS-Gemeindetypologie; Vergleich von
Preis und Anstieg zwischen den Clustern. Das Clustering kommt zur Regression hinzu und
ersetzt sie nicht.

**Stand: ✅ erfüllt.**

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
| Pflicht (9) | 7 | 1 | 1 |
| Bonus (6) | 4 | 2 | – |
| Video (7 Pkt) | – | – | alle |

**Lennys Teil:** Pflicht 2 ✅, Bonus 3 ✅, Pflicht 8 🟡 (Bündelung und Präsentationsteil
fehlen), Bonus 1 🟡 (beansprucht, aber noch nicht im PDF-Anhang).

**Metehans Teil:** Pflicht 1 ✅, Pflicht 3 ✅, Bonus 2 ✅, Bonus 6 🟡 (URL muss in die
Präsentation).

**Subrajs Teil:** Pflicht 4 bis 7 ✅, Bonus 4 ✅, Bonus 5 ✅, Pflicht 9 ⬜ (Zip im Januar).

**Offen bis zur Abgabe:** Pflicht 8 (Präsentationsteil und Bündelung), Pflicht 9 (Zip),
Bonus 1 und 6 (im PDF-Anhang beanspruchen), das Video und der PDF-Anhang mit
Screenshots und Code-Ausschnitten zu jedem Punkt.

**Was nicht belegbar ist:** Ob Metehans Beschaffungsskript bei einem Lauf exakt die
Dateien im Repo erzeugt – das wurde nicht nachgerechnet, weil es Netzzugriff braucht.
