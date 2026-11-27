> **Internal working document.** This list is kept in German on purpose. It is the
> team's working record of which requirement is covered by what, and it is not a
> submission file. Its content goes into the appendix of the presentation PDF, and
> it is translated at that point, not here.

# Punkteliste

Data Analytics, ZHAW, HS2026 · Lenny Frei · Metehan Altay · Sub Raj Singh
Stand: 27. November 2026

**Was geprüft ist und was nicht.** Die mit 🔍 markierten Angaben wurden unabhängig
nachgerechnet oder nachgezählt: auf einem frischen Klon, in einer frischen virtuellen
Umgebung, durch Ausführen der Notebooks und durch Nachzählen in den Dateien. Alles
ohne 🔍 stammt aus den Notebooks und Dokumentationen der Gruppe und ist nicht
unabhängig geprüft.

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
  `guete_A`). Nachgeprüft: R² 0.227 / 0.068 / 0.069 / 0.221 / 0.297, R² adj.
  0.224 / 0.065 / 0.065 / 0.218 / 0.295, RMSE 2.563 bis 3.837 Rp. (nachgezogen am
  27.11.2026 aus Subrajs Lauf `ed9b39e` nach dem Platzhalter-Filter; vorher R² 0.218 /
  0.068 / 0.069 / 0.214 / 0.290)
- 🔍 **Kein Train-Test-Split, sondern 5-fache Kreuzvalidierung** (§6) – und zwar in
  zwei Varianten: mit zufälligen Folds (`KFold`) und mit nach Netzbetreiber
  **gruppierten** Folds (`GroupKFold`). Das ist für diese Daten das **stärkere**
  Verfahren: Ein einzelner zufälliger Split würde Gemeinden desselben Netzbetreibers
  auf Trainings- und Testteil verteilen und die Güte dadurch überschätzen, weil die
  Beobachtungen nicht unabhängig sind (Abschnitt 5b der Projektanleitung). Die
  gruppierten Folds halten ganze Versorgungsgebiete zurück und messen damit, was das
  Modell wirklich überträgt.
- 🔍 Das Ergebnis dieser Prüfung ist zugleich das Hauptresultat des Projekts: Bei
  zufälligen Folds bleibt R² fast unverändert (0.222 gegen 0.227 in der Stichprobe),
  bei gruppierten Folds wird es **negativ** (−0.120 / −0.007 / −0.025 / −0.066 /
  −0.063). Das Modell sagt dann schlechter voraus als der blosse Mittelwert.
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

### Pflicht 8 🟡 Dokumentation der AI-Nutzung · alle, gebündelt von Subraj

> «Documentation of AI usage for creating the code and the presentation (the use of AI
> is not only allowed but desired), including the advantages and disadvantages you
> found and where something did not work with the help of AI.»

| Teil | Beleg |
|---|---|
| Lenny | `ai-doku/ai_dokumentation_lenny.md` – 15 dokumentierte Fehlschläge mit Datum, dazu Abschnitte «Was gut funktioniert hat» und «Was mühsam war» |
| Metehan | `ai-doku/AI-Documentation_DataCollection_Metehan.md`, `ai-doku/AI-Documentation_SQLite_Metehan.md`, `ai-doku/AI-Documentation_PostgreSQL_Metehan.md`, `ai-doku/AI-Documentation_Presentation_Metehan.md` |
| Subraj | `ai-doku/ai_dokumentation_subraj.md` – Sitzungsprotokoll mit dokumentierten Fehlschlägen, Vorteile, Nachteile |

| Gebündelt | `ai-doku/ai_dokumentation_gruppe_15.md` – Werkzeuge, Einsatz pro Aufgabe, Vorteile, Nachteile, 18 Fälle, in denen etwas nicht funktioniert hat, Lehren, Vorschlag für Folien und Video |

🔍 Geprüft: Alle fünf Dateien enthalten einen eigenen Abschnitt zu Fehlschlägen, so
wie es die Anforderung verlangt («where something did not work with the help of AI»).
Die Bündelung `ai-doku/ai_dokumentation_gruppe_15.md` hat Subraj am 22.11.2026
angelegt; damit ist dieser Teil von Pflicht 8 erledigt.

**Stand: 🟡 teilweise.** Was fehlt, ist nur noch **ein** Punkt: der Teil «and the
presentation» bei allen dreien. Die Präsentation entsteht ab dem 24. November; danach
ist Abschnitt 6 der gebündelten Fassung zu ergänzen. Sie nennt das dort ausdrücklich
als nachzutragen – korrekt markiert, aber noch nicht erfüllt.

### Pflicht 9 ⬜ Material auf Moodle · Subraj

> «Making the material (data, Jupyter notebooks, ...) available on Moodle.»

Abgabe im Januar: `materials_group_XX.zip`. Die Gruppennummer ist noch offen.

**Stand: ⬜ offen.**

---

## Bonus, maximal 6 Punkte

### Bonus 1 🟡 Kreativität · alle

> «Creativity of implementation (creative is anything not specified in the lessons and
> exercises).»

Was in den Lektionen und Übungen **nicht** vorkam. Geprüft am 21.11.2026 gegen die
beiden öffentlichen Kurs-Repos, die auf Moodle als Übungsmaterial verlinkt sind:
`mario-gellrich-zhaw/data_analytics` (Stand 10.11.2026) und
`mario-gellrich-zhaw/spatial_data_analysis` (Stand 13.10.2026), alle Notebooks und Skripte
durchsucht.

| Was | Beleg | Fundstelle im Kursmaterial |
|---|---|---|
| **SPARQL** gegen einen Linked-Data-Endpunkt | `scripts/strompreise_holen.py`, `query.txt` | kommt nicht vor; die Übungen holen Daten per REST-API mit `requests` (Woche 1 und 5) |
| **Maschinelle Auflösung von Gemeindefusionen** über die Mutationstabelle des historisierten Gemeindeverzeichnisses | `scripts/01_daten_bfs_lenny.ipynb`; `dokumentation_integration_lenny.md` §9b | kommt nicht vor; die Übungen verbinden Tabellen, ohne Gebietsstände zu behandeln |
| **Permutationstest** auf Auswahlverzerrung, 20 000 Ziehungen | `scripts/01_daten_bfs_lenny.ipynb`; `dokumentation_integration_lenny.md` §7 | nur im Agenten-Experiment des Dozenten erwähnt, nicht in Lektionen oder Übungen; unterrichtet sind t-Test (Woche 6), ANOVA (Woche 6), Kontingenztafeln und Korrelation (Woche 7) |
| **Varianzzerlegung nach Netzbetreibern**, Kanton und Sprachregion (eta²) | `scripts/03_analyse_subraj.ipynb` §7; Projektanleitung Abschnitt 5b | kommt nicht vor; die ANOVA in Woche 6 testet Unterschiede, ohne eine Effektstärke oder die Aggregationsebene zu behandeln |
| **Nach Netzbetreiber geclusterte Standardfehler**, selbst implementiert | `scripts/04_modell_subraj.ipynb` §2 | kommt nicht vor; die Regression in Woche 8 nutzt statsmodels mit gewöhnlichen Standardfehlern |
| **Gruppierte Kreuzvalidierung** (GroupKFold) im Vergleich zur zufälligen | `scripts/04_modell_subraj.ipynb` §6 | kommt nicht vor; die Übung in Woche 9 nutzt `cross_val_score` mit zufälliger Aufteilung |
| **Alexander-Govern-Test, Tukey-Test, Bonferroni-Korrektur** | `scripts/03_analyse_subraj.ipynb` §8 | kommen nicht vor; die ANOVA in Woche 6 hat keinen Post-hoc-Test und keine Korrektur für mehrfaches Testen |
| **Cluster-robuster Wald-Test** über die k-means-Cluster | `scripts/04_modell_subraj.ipynb` §8.4 | kommt nicht vor; k-means in Woche 10 wählt k über Ellbogen und Silhouette, ohne die Cluster statistisch zu vergleichen |

**Nicht beanspruchen:** Die Karte in Python ist **nicht** kreativ im Sinn der Vorgabe. Die
Übungen zu Woche 5 (`spatial_data_analysis`, Notebooks 01 bis 06) zeichnen Karten mit
geopandas und folium, auch eingefärbte Gemeindekarten. Die Karte zählt für Bonus 3, nicht
für Bonus 1.

**Stand: 🟡 teilweise.** Die Techniken existieren und sind belegt. Sie sind bis jetzt
aber nirgends **beansprucht** – diese Liste ist der erste Ort. Vollständig wird der
Punkt erst, wenn sie im Anhang des Präsentations-PDF mit Screenshots und
Code-Ausschnitten steht.

### Bonus 2 ✅ PostgreSQL · Metehan

> «Use of a PostgreSQL or similar database (no SQLite!) with, e.g. SQL joins and
> aggregations from within Python.»

- `sql/03_postgresql.ipynb`: überträgt alle 5 Tabellen aus SQLite nach PostgreSQL 17,
  baut die beiden Views nach und rechnet Auswertungen mit `JOIN`, `GROUP BY`, `HAVING`,
  `percentile_cont`, `STDDEV`, `CORR` und den Fensterfunktionen `RANK`, `LAG`, `NTILE`
- Kontrollen: gleiche Zeilenzahl in allen Tabellen, Summe der Bestandteile, Analysetabelle
  gegen SQLite (grösste Abweichung 7e-15)

**Stand: ✅ erfüllt.** Alle drei Mängel vom 22.11.2026 sind behoben. Am 23.11.2026
einzeln nachgeprüft:

| | Mangel | Stand |
|---|---|---|
| 1 | Keine Einrichtungsanleitung | ✅ **behoben.** `README.md` enthält jetzt drei Anleitungen: Windows, macOS (Homebrew oder Postgres.app) und Linux (Debian/Ubuntu und Fedora), je mit Installation, Dienststart, `CREATE DATABASE` und den Umgebungsvariablen |
| 2 | `getpass` blockiert jeden automatischen Lauf | ✅ **behoben.** 🔍 `getpass` kommt im Code nicht mehr vor. Alle Verbindungsangaben stammen aus Umgebungsvariablen mit den Standardwerten `localhost`, `5432`, `strompreise`, `postgres`; fehlt `PGPASSWORD`, gibt es eine klare Fehlermeldung |
| 3 | Ausgaben vom Ersatzmodul statt von `psycopg2` | ✅ **behoben.** 🔍 Siehe unten |

**Wie Punkt 3 geprüft wurde** – das war der heikelste:

- 🔍 **Kein Ersatzmodul mehr im Code.** Durchsucht nach `subprocess`, `os.system`,
  `psql`, `popen`, `shell=True` und eigenen Connection-Klassen: **null Treffer**.
  Vorhanden sind `import psycopg2`, `psycopg2.connect` und `execute_values` aus
  `psycopg2.extras`.
- 🔍 **Das Notebook wurde neu ausgeführt.** 15 Ausgaben statt vorher 13, 0 Fehler.
  Neu ist unter anderem eine Zelle, die `PostgreSQL 17.12 on x86_64-...` ausgibt –
  eine Versionsabfrage, die nur aus einer echten Serververbindung kommen kann.
- 🔍 **Die unveränderten Ausgaben sind plausibel.** Sieben der Ausgaben sind gleich
  geblieben. Alle stammen aus deterministischen Abfragen über unveränderte Daten
  (Tabellen- und Zeilenzahlen, Mittelwerte je Jahr, Betreiber-Rangliste). Dass sie
  identisch sind, ist das erwartete Ergebnis und kein Zeichen alter Ausgaben.
- 🔍 **Die geänderten Ausgaben enthalten dieselben Zahlen.** Bei den Zellen 14, 18,
  20 und 22 änderte sich nur die Anzeigebreite von pandas, nicht ein einziger Wert.
- 🔍 **Der Abgleich gegen SQLite geht weiterhin auf:** 2087 / 2087 Gemeinden, gleiche
  Gemeindenummern, grösste Abweichung 7.11e-15 bei den Preisen und 0.00 bei den
  Gemeindemerkmalen.

**Sicherheitsprüfung am 23.11.2026** (weil die Commit-Nachricht «basierend auf eigenes
Gerät» lautete): Kein Passwort im Klartext, kein absoluter Pfad, kein Benutzer- oder
Rechnername, keine fremde IP. Alle Passwortstellen sind Platzhalter
(`das-eigene-passwort`) oder Lesezugriffe auf `PGPASSWORD`. Host und Port sind
`localhost` und `5432` als Standardwerte aus Umgebungsvariablen.

**Was ich nicht prüfen kann:** Dass die eingebetteten Ausgaben tatsächlich auf
Metehans Rechner mit genau diesem Code entstanden sind. Belegbar ist, dass der Code
kein Ersatzmodul mehr enthält, dass die Ausgaben zu einem echten PostgreSQL-17-Server
passen und dass die Zahlen mit SQLite und mit unserer eigenen Berechnung
übereinstimmen.


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
Netzbetreiber erklärt 94 bis 97 Prozent der Preisstreuung, der Kanton 23 bis 62, die
Sprachregion 0.4 bis 3.4.

**Drei offene Punkte vor der Abgabe.** Keiner kostet heute einen Punkt, alle drei
können nachträglich etwas kaputtmachen. Punkt 1 und 2 betreffen Bonus 3, Punkt 3
das Repo als Ganzes; sie stehen hier zusammen, damit alle Abgabe-Prüfungen an
einem Ort sind:

| | Was | Wann |
|---|---|---|
| 1 | **Beide interaktiven Karten im Browser öffnen und anschauen.** Die Hintergrundkacheln kommen von einem Drittanbieter, und genau das ist am 25.11.2026 schon einmal gebrochen: CartoDB verlangt seither einen Schlüssel und lieferte statt der Karte ein flächendeckendes Raster aus «API KEY REQUIRED». Umgestellt auf Esri World Light Gray Base – schlüsselfrei, aber derselbe Anbietertyp und damit dasselbe Risiko. **Das Notebook meldet in diesem Fall keinen Fehler.** Die Prüfung geht nur mit dem Auge. | vor der Abgabe im Januar |
| 2 | **Kantonsumrisse als eigene Ebene in die beiden folium-Karten legen.** Die Geometrie liegt bereits vor und wird in Zelle 54 für die statischen Karten verwendet (`kantone.boundary`). Danach bleibt die Schweiz erkennbar, auch wenn gar keine Kacheln mehr laden, und die Karte hängt nur noch an unseren eigenen swisstopo-Daten statt an einem Drittanbieter. | nach Freitag, 27.11. |
| 3 | **README nachführen: Datum und Abschnitt «Status».** Dort steht ein festes Datum und eine Liste, was fertig ist und was als Nächstes kommt. Beides veraltet bis zum 10. Januar sicher. Das README ist über Bonus 6 die Eingangstür für die Dozenten; ein falsches Datum auf der ersten Seite ist der billigste vermeidbare Fehler im ganzen Projekt. Dazu gehören die Passwort-Platzhalter in dieser Punkteliste, die noch deutsch sind. | vor der Abgabe im Januar |

### Bonus 4 ✅ Chi-Quadrat, ANOVA oder Korrelation mit p-Wert · Subraj

> «Use of a Chi-squared test, analysis of variance (ANOVA), or correlation analysis
> (each test must include a p-value).»

| Test | Beleg |
|---|---|
| ANOVA über Sprachregionen und Kantone, mit Levene, Alexander-Govern, Kruskal-Wallis, eta² und Tukey | `scripts/03_analyse_subraj.ipynb` §8.3, §8.4 |
| Korrelation nach Pearson und Spearman mit p-Wert und Bonferroni-Korrektur | `scripts/03_analyse_subraj.ipynb` §8.5, §8.6 |
| Korrelationen in der EDA, ebenfalls mit p-Wert (Preise zwischen den Jahren; Heatmap Merkmal und Preis mit Bonferroni-Stern) | `scripts/03_analyse_subraj.ipynb` §3, §5.2 |
| ANOVA über die k-means-Cluster, mit cluster-robustem Wald-Test | `scripts/04_modell_subraj.ipynb` §8.4 |
| **Chi-Quadrat-Test** auf der Kontingenztafel k-means-Cluster gegen BFS-Gemeindetypologie, mit Cramérs V, Prüfung der erwarteten Häufigkeiten und standardisierten Residuen | `scripts/04_modell_subraj.ipynb`, **Zelle 39** |

Jeder Test ist auf Gemeinde- und auf Betreiberebene gerechnet. Der gepaarte t-Test
(§8.2) steht zusätzlich im Notebook, zählt für diesen Punkt aber nicht.

🔍 **Am 27.11.2026 nachgeprüft:** Die Anforderung nennt drei Verfahren mit «or», es
genügt also eines. Belegt sind **alle drei**. Der Chi-Quadrat-Test steht in Notebook
04, Zelle 39, und gibt aus: `Chi² = 1247.5, degrees of freedom = 24, p = 1.8e-248`,
dazu `Cramér's V = 0.446` und die Kontrollzeile `cells with expected frequency below
5: 0 of 36`. Die Tafel umfasst 2086 Gemeinden, weil Prez (2237) keinen
Typologiewert hat.

**Nachtrag vom 23.11.2026.** Zwei Stellen in der EDA berichteten bis dahin nur den
Korrelationskoeffizienten ohne p-Wert. Subraj hat beide ergänzt. 🔍 Am 24.11.2026
nachgeprüft:

- **Zelle 18**, Korrelation der Preise zwischen den Jahren: jetzt mit «p (Spearman)»
  und «p (Pearson)». Beispiel 2024–2027: rho 0.567 bei p = 5.6e-178, r 0.594 bei
  p = 3e-199.
- **Zelle 33**, Heatmap der Merkmale gegen die Preise: jetzt eine eigene p-Wert-Matrix
  mit Bonferroni-Korrektur über **25 Tests**, Schwelle 0.05/25 = **0.0020**.
  Signifikant sind **18 von 25**. Die nicht signifikanten liegen fast alle in der
  Spalte «Preis 2027» – dort hängt der Preis mit keinem der fünf Gemeindemerkmale
  zusammen, was zum Hauptresultat passt.

Damit berichtet jeder Test in beiden Notebooks einen p-Wert, wie es die Anforderung
verlangt.

**Stand: ✅ erfüllt.**

### Bonus 5 ✅ k-means · Subraj

> «Use of k-means clustering in addition to the regression or classification model.»

`scripts/04_modell_subraj.ipynb` §8: k-means auf Dichte, Fläche und Anteil 65+,
standardisiert; Wahl von k über Ellbogenkriterium und Silhouettenkoeffizient (k = 4);
Profile der vier Gemeindetypen; Kontrolle gegen die BFS-Gemeindetypologie; Vergleich von
Preis und Anstieg zwischen den Clustern. Das Clustering kommt zur Regression hinzu und
ersetzt sie nicht.

**Stand: ✅ erfüllt.**

### Bonus 6 ⬜ Öffentliches GitHub-Repo · Metehan

> «Code on a publicly available GitHub repository (provide the GitHub project URL in
> the project presentation).»

- Repo: https://github.com/AltayMetehan/data-prices-electronic
- Sichtbarkeit geprüft am 24.11.2026: **PUBLIC**

**Stand: ⬜ offen.** Das Repo ist öffentlich, das ist die halbe Anforderung. Die
andere Hälfte verlangt die URL **in der Präsentation**, und die existiert noch nicht.
Vorgesehen ist sie auf Folie 1, siehe `folien_entwurf_lenny.md`.

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
| Bonus (6) | 4 | 1 | 1 |
| Video (7 Pkt) | – | – | alle |

🔍 Am 24.11.2026 auf einem frischen Klon mit frischer virtueller Umgebung geprüft:
`pip install -r requirements.txt` läuft durch, und die vier Notebooks `01`, `02`, `03`
und `04` laufen fehlerfrei, jedes aus seinem Verzeichnis. `sql/03_postgresql.ipynb`
braucht einen laufenden PostgreSQL-Server und wurde darum nicht ausgeführt; der Code
importiert das echte `psycopg2`.

**Lennys Teil:** Pflicht 2 ✅, Bonus 3 ✅, Pflicht 8 🟡 (Präsentationsteil
fehlt), Bonus 1 🟡 (beansprucht, aber noch nicht im PDF-Anhang).

**Metehans Teil:** Pflicht 1 ✅, Pflicht 3 ✅, Bonus 2 ✅ (am 23.11. nachgeprüft:
echtes `psycopg2`, Notebook neu ausgeführt, Anleitungen für Windows, macOS und Linux),
Bonus 6 ⬜ (Repo öffentlich, aber die URL muss in die Präsentation).

**Subrajs Teil:** Pflicht 4 bis 7 ✅, Bonus 4 ✅, Bonus 5 ✅, Pflicht 9 ⬜ (Zip im Januar).

**Offen bis zur Abgabe:** Pflicht 8 (Präsentationsteil), Pflicht 9 (Zip), Bonus 1
(im PDF-Anhang beanspruchen), Bonus 6 (Repo-URL in der Präsentation nennen), das Video
und der PDF-Anhang mit Screenshots und Code-Ausschnitten zu jedem Punkt.

**Was nicht belegbar ist:** Ob Metehans Beschaffungsskript bei einem Lauf exakt die
Dateien im Repo erzeugt – das wurde nicht nachgerechnet, weil es Netzzugriff braucht.
