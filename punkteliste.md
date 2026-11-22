# Punkteliste

Data Analytics, ZHAW, HS2026 · Gruppe Frei / Metehan / Sub Raj
Stand: 22. November 2026

**Was geprüft ist und was nicht.** Die mit 🔍 markierten Angaben habe ich am
22.11.2026 selber nachgerechnet oder nachgezählt: auf einem frischen Klon, in einer
frischen virtuellen Umgebung, durch Ausführen der Notebooks und durch Nachzählen in
den Dateien. Alles ohne 🔍 stammt aus den Notebooks und Dokumentationen der Gruppe und
ist nicht unabhängig geprüft.

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

- 🔍 R², **angepasstes R²** und **RMSE** für alle fünf Zielgrössen, RMSE verglichen
  mit der Standardabweichung der Zielgrösse (`04_modell_subraj.ipynb` §3, Tabelle
  `guete_A`). Nachgeprüft: R² 0.218 / 0.068 / 0.069 / 0.214 / 0.290, R² adj.
  0.215 / 0.065 / 0.065 / 0.212 / 0.288, RMSE 2.645 bis 3.893 Rp.
- 🔍 **Kein Train-Test-Split, sondern 5-fache Kreuzvalidierung** (§6) – und zwar in
  zwei Varianten: mit zufälligen Folds (`KFold`) und mit nach Netzbetreiber
  **gruppierten** Folds (`GroupKFold`). Das ist für diese Daten das **stärkere**
  Verfahren: Ein einzelner zufälliger Split würde Gemeinden desselben Netzbetreibers
  auf Trainings- und Testteil verteilen und die Güte dadurch überschätzen, weil die
  Beobachtungen nicht unabhängig sind (Abschnitt 5b der Projektanleitung). Die
  gruppierten Folds halten ganze Versorgungsgebiete zurück und messen damit, was das
  Modell wirklich überträgt.
- 🔍 Das Ergebnis dieser Prüfung ist zugleich das Hauptresultat des Projekts: Bei
  zufälligen Folds bleibt R² fast unverändert (0.213 gegen 0.218 in der Stichprobe),
  bei gruppierten Folds wird es **negativ** (−0.104 / −0.007 / −0.025 / −0.058 /
  −0.050). Das Modell sagt dann schlechter voraus als der blosse Mittelwert.
- Residuen gegen Vorhersage, Histogramm und Q-Q-Plot (§7)
- Varianzinflationsfaktor gegen Multikollinearität (§1.2)

**Stand: ✅ erfüllt.** Die Anforderung nennt R² und RMSE als Beispiele; beide werden
berichtet, dazu das angepasste R² und eine Gütemessung ausserhalb der Stichprobe.
Anmerkung zur Nachvollziehbarkeit: Subraj berechnet die Masse in einer eigenen
Funktion `ols_geclustert` statt mit `r2_score` oder `mean_squared_error`. Wer im Code
nach diesen Namen sucht, findet sie nicht – die Masse sind trotzdem da.

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
| **Bündelung** | `ai-doku/ai_dokumentation_gruppe_15.md` – von Subraj am 22.11.2026 angelegt, fasst alle drei zusammen |

🔍 Geprüft: Alle fünf Dateien enthalten einen eigenen Abschnitt zu Fehlschlägen, so
wie es die Anforderung verlangt («where something did not work with the help of AI»).

**Stand: 🟡 teilweise.** Was fehlt, ist nur noch **ein** Punkt:
der Teil «and the presentation». Die Folien entstehen ab dem 24. November. Die
Bündelung nennt das in ihrem Abschnitt 6 ausdrücklich als nachzutragen – das ist
korrekt markiert, aber noch nicht erfüllt.

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

### Bonus 2 🟡 PostgreSQL · Metehan

> «Use of a PostgreSQL or similar database (no SQLite!) with, e.g. SQL joins and
> aggregations from within Python.»

- `sql/03_postgresql.ipynb`: überträgt alle 5 Tabellen aus SQLite nach PostgreSQL,
  baut die beiden Views nach und rechnet Auswertungen mit `JOIN`, `GROUP BY`, `HAVING`,
  `percentile_cont`, `STDDEV`, `CORR` und den Fensterfunktionen `RANK`, `LAG`, `NTILE`
- `requirements.txt`: enthält `psycopg2-binary`
- Kein interaktives Passwort: Verbindung über `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`
  und `PGPASSWORD`
- SQLite-Pfad relativ zur Repo-Wurzel, sodass das Notebook aus mehreren Arbeitsverzeichnissen
  gestartet werden kann
- Kontrollen: gleiche Zeilenzahl in allen Tabellen, Summe der Bestandteile, Analysetabelle
  gegen SQLite (grösste Abweichung 7e-15)

**Stand: 🟡 teilweise.** Zwei der drei Mängel vom 22.11.2026 sind seit Metehans
Korrekturen behoben, der dritte nicht. Einzeln nachgeprüft:

| | Mangel | Stand |
|---|---|---|
| 1 | Keine Einrichtungsanleitung | ✅ **behoben.** Metehan hat sie ins README geschrieben: Installation, `CREATE DATABASE strompreise`, Benutzer, Umgebungsvariablen. **Einschränkung:** Die Anleitung beschreibt nur **Windows** (winget, PowerShell). Für macOS und Linux fehlen die Schritte |
| 2 | `getpass` blockiert jeden automatischen Lauf | ✅ **behoben.** 🔍 Geprüft: `getpass` kommt im Code nicht mehr vor. Alle Verbindungsangaben kommen aus Umgebungsvariablen, bei fehlendem `PGPASSWORD` gibt es eine klare Fehlermeldung |
| 3 | Eingebettete Ausgaben stammen vom Ersatzmodul, nicht von `psycopg2` | ❌ **offen.** 🔍 Geprüft: Alle 11 Ergebnisausgaben sind zeichengleich mit der Fassung von vor der Korrektur. Das Notebook wurde seither **nicht neu ausgeführt** |

🔍 Zusätzlich geprüft und in Ordnung: Der relative Pfad ist durch einen Anker auf die
Repo-Wurzel ersetzt. Getestet aus der Repo-Wurzel **und** aus `sql/` – beide Male wird
`sql/strompreise.db` gefunden.

**Warum der Punkt trotzdem noch nicht auf ✅ steht.** Metehans eigene AI-Dokumentation
hält fest: «In der Umgebung der AI liess sich `psycopg2` nicht installieren […] Die AI
hat stattdessen ein Ersatzmodul geschrieben, das jeden Befehl über das
Kommandozeilenprogramm `psql` an den Server schickt. Die Ausgaben im Notebook stammen
von diesem Ersatz.» Das SQL ist also auf einem echten PostgreSQL-Server gelaufen – das
ist der Kern des Bonuspunkts und er ist belegt. Die im Notebook **sichtbaren** Zahlen
sind aber nicht über den Treiber entstanden, den das Notebook importiert.

**Was den Punkt schliesst, Aufwand etwa zehn Minuten:** Metehan führt das Notebook
einmal mit dem echten `psycopg2` gegen seinen Server aus und committet die neuen
Ausgaben. Danach steht der Punkt auf ✅.

Kleinigkeit ohne Punkterelevanz: Der Verweis auf `02_sqlite_datenbank.ipynb` meint
`02_sqlite_metehan.ipynb`.

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
| Bonus (6) | 3 | 3 | – |
| Video (7 Pkt) | – | – | alle |

🔍 Am 22.11.2026 auf einem frischen Klon mit frischer virtueller Umgebung geprüft:
`01`, `02`, `03` und `04` laufen fehlerfrei durch, jedes aus seinem Verzeichnis.
`sql/03_postgresql.ipynb` scheitert am fehlenden Server, siehe Bonus 2.

**Lennys Teil:** Pflicht 2 ✅, Bonus 3 ✅, Pflicht 8 🟡 (nur noch der
Präsentationsteil fehlt, die Bündelung hat Subraj am 22.11. angelegt), Bonus 1 🟡
(beansprucht, aber noch nicht im PDF-Anhang).

**Metehans Teil:** Pflicht 1 ✅, Pflicht 3 ✅, Bonus 2 🟡 (Anleitung geschrieben,
aber nur für Windows; Notebook noch nicht mit echtem `psycopg2` neu ausgeführt),
Bonus 6 ⬜ (es gibt noch keine Präsentation, in der die URL stehen könnte).

**Subrajs Teil:** Pflicht 4 bis 7 ✅, Bonus 4 ✅, Bonus 5 ✅, Pflicht 9 ⬜ (Zip im Januar).

**Offen bis zur Abgabe:** Pflicht 8 (Präsentationsteil), Pflicht 9 (Zip), Bonus 1
und 6 (im PDF-Anhang beziehungsweise in der Präsentation beanspruchen), Bonus 2
(Notebook mit echtem `psycopg2` neu ausführen, Anleitung für macOS und Linux), das
Video und der PDF-Anhang mit Screenshots und Code-Ausschnitten zu jedem Punkt.

**Was nicht belegbar ist:** Ob Metehans Beschaffungsskript bei einem Lauf exakt die
Dateien im Repo erzeugt – das wurde nicht nachgerechnet, weil es Netzzugriff braucht.
