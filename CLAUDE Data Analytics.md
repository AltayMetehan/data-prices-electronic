# Data Analytics Projekt: Strompreise der Schweizer Gemeinden

ZHAW, Modul Data Analytics, HS2026. Dozenten: Dr. Mario Gellrich (modulverantwortlich),
Dr. Alexander Walter.
Gruppe: Lenny Frei, Altay Metehan, Singh Sub Raj.

Sprache in Code, Kommentaren und Bericht: Deutsch. Schweizer Rechtschreibung,
immer «ss», nie «ß». Englische Fachbegriffe nicht eindeutschen.

Anspruch der Gruppe: Bestnote. Optionale Kriterien und Zusatzpunkte werden wie
Pflicht behandelt, nicht wie Kür.

---

## 1. Forschungsfrage

Welche Merkmale einer Gemeinde erklären die Höhe ihres Strompreises für Haushalte,
und haben sich diese Zusammenhänge mit dem Preisanstieg 2023 verändert?

Der zweite Teil ist nicht schmückendes Beiwerk. Die Aufgabenstellung verlangt, dass
die Forschungsfrage über eine reine Vorhersage hinausgeht und einen Vergleich
zwischen Gruppen, Regionen, Zeiträumen oder Datenquellen enthält. Der Zeitvergleich
erfüllt das.

### Unterfragen und die jeweilige Methode

| Nr | Unterfrage | Methode |
|---|---|---|
| 1 | Wie stark unterscheiden sich die Preise zwischen Gemeinden, Kantonen und Sprachregionen, und welcher Preisbestandteil macht den Unterschied aus? | EDA, Karte, ANOVA |
| 2 | Welche Gemeindemerkmale hängen mit dem Preis zusammen? Einwohner, Dichte, Grösse des Netzbetreibers | Korrelation mit p-Wert |
| 3 | Wie gut erklärt ein Modell den Preis, welche Merkmale wiegen am schwersten? | Multiple Regression, R², RMSE |
| 4 | Haben sich diese Zusammenhänge verändert? Verglichen werden 2021, 2024, 2027 | Dasselbe Modell pro Jahr, Koeffizienten vergleichen |
| 5 | Lassen sich Gemeindetypen bilden, unterscheiden sie sich im Niveau und im Anstieg? | k-means, ANOVA über die Cluster |

### Warum diese drei Jahre

| Jahr | Was es zeigt |
|---|---|
| 2021 | vor der Krise, der Normalzustand |
| 2024 | auf dem Höhepunkt |
| 2027 | danach, und zwar sehr ungleich |

### Erwartete Resultate

Wir erwarten, dass Gemeindemerkmale den Strompreis nur schwach erklären. Nicht die
Lage einer Gemeinde entscheidet, sondern von welchem Netzbetreiber sie beliefert wird
und wie dieser seinen Strom eingekauft hat. Der Energieanteil erklärte 2024 rund
80 Prozent der Unterschiede zwischen Gemeinden, und er ist eine Einkaufsentscheidung
des Betreibers.

Wir rechnen deshalb mit einem niedrigen R², vermutlich unter 0.3. Das ist kein
Misserfolg, sondern das Resultat: Der Strompreis einer Gemeinde hängt weniger von ihr
selbst ab als von ihrem Versorger.

---

## 2. Daten

### Quelle 1, primär: ElCom Strompreise

Über den SPARQL-Endpunkt `https://ld.admin.ch/query`, Cube
`https://energy.ld.admin.ch/elcom/electricityprice`, Dimensionen unter
`https://energy.ld.admin.ch/elcom/electricityprice/dimension/`.

Massgebend sind die Werte in `strompreise_holen.py` und `query.txt`, nicht diese
Zusammenfassung. Korrigiert am 01.11.2026: Hier standen vorher Adressen unter
`lindas.admin.ch`, die ins Leere laufen.

Abgeholt per Python-Skript, nicht von Hand heruntergeladen. Das ist Pflicht:
Die Aufgabenstellung verlangt Erhebung per Web Scraping oder Web API und schliesst
fertige Datensätze als Primärquelle ausdrücklich aus.

Dateien im Repo: `daten/strompreise/Daten_Strompreise_2021.csv`, `_2024.csv`,
`_2027.csv`. Skript: `scripts/strompreise_holen.py`. Abfrage: `query.txt`.

Spalten, 14 insgesamt: jahr, gemeinde_nr, gemeinde, netzbetreiber_id,
netzbetreiber, produkt, kategorie, total, energie, netznutzung, abgaben,
netzzuschlag, messtarif, messtarif_chf_jahr.

Stand 27.10.2026: Metehan hat die Abfrage angepasst. `messtarif` und
`messtarif_chf_jahr` sind neu dazugekommen, `fixkosten` ist weggefallen.

### Quelle 2: Gemeindedaten des Bundesamts für Statistik

Regionalporträts 2021, Kennzahlen aller Gemeinden. Verknüpfung über die
BFS-Gemeindenummer, in der Datei als `CODE_REGION`.

**Was wirklich drin ist**, geprüft am 01.11.2026 an der Rohdatei. Sie hat acht
Spalten: `PERIOD_REF`, `PERIOD_COMP`, `CODE_REGION`, `REGION`, `INDICATORS`,
`UNIT_MES`, `VALUE`, `STATUS`. Im Langformat, eine Zeile je Gemeinde und Kennzahl,
41 Kennzahlen:

| Thema | Kennzahlen |
|---|---|
| Bevölkerung | Einwohner, Veränderung, Dichte, Altersgruppen, Ausländeranteil, Haushalte |
| Fläche | Gesamtfläche, Siedlung, Landwirtschaft, Wald, unproduktiv |
| Wirtschaft | Beschäftigte und Arbeitsstätten, je total und nach Sektor |
| Wohnen | Leerwohnungsziffer, neu gebaute Wohnungen |
| Soziales | Sozialhilfequote |
| Politik | Wähleranteile der Parteien |

**Was nicht drin ist: Kanton, Sprachregion und Gemeindetypologie.** Keines dieser
drei Merkmale kommt in der Datei vor, und die ElCom-Daten enthalten sie auch nicht.

Korrigiert am 07.11.2026: Hier stand vorher, die Regionalporträts enthielten
Gemeindetypologie, Kanton und Sprachregion. Das war nie geprüft und ist falsch.

**Folge:** Unterfrage 1 der Forschungsfrage, die Unterschiede zwischen Kantonen und
Sprachregionen, und die ANOVA dazu (Bonus 4) sind mit dem aktuellen Datenstand nicht
rechenbar. Es braucht eine dritte Quelle, siehe Abschnitt 11.

Für die zweite Quelle ist ein Download zulässig. Die Vorgabe zur eigenen Erhebung
gilt nur für die Primärquelle, die Aufgabenstellung nennt als Beispiel ausdrücklich
«scraped data enriched with data from opendataswiss».

### Quelle 3: Raumgliederungen der Schweiz

Weil Quelle 2 Kanton, Sprachregion und Gemeindetypologie nicht enthält, kommt eine
dritte Quelle dazu: «Die Raumgliederungen der Schweiz 2019» des BFS, eine XLSX mit
2212 Gemeinden und 30 Spalten.

- Download: `https://dam-api.bfs.admin.ch/hub/api/dam/assets/9046166/master`
- Lizenz: OPEN-BY, freie Nutzung mit Quellenangabe
- Gebietsstand: 01.01.2019
- Join über `BFS Gde-nummer`, Ganzzahl ohne führende Nullen
- Übernommen: `kanton`, `kanton_nr`, `sprachregion`, `gemeindetyp_9`

Geholt wird sie per `scripts/hole_zusatzdaten.py`, abgelegt unter
`daten/raumgliederungen/` mit Herkunftsnachweis.

Weil der Gebietsstand 2019 ist, fehlen vier unserer 2087 Gemeinden, die 2020 und
2021 durch Fusion entstanden sind. Sie werden über die Mutationstabelle des
historisierten Gemeindeverzeichnisses aufgelöst, nicht von Hand. Siehe
`dokumentation_integration_lenny.md`, Abschnitt 9b.

### Geodaten für die Karte

Geprüft am 30.10.2026: Die Geodaten im Kurs-Repo von Dr. Gellrich
(`https://github.com/mario-gellrich-zhaw/data_analytics`, Woche 05, Ordner `Geodata`)
decken **nur den Kanton Zürich** ab. `municipality_map_epsg4326.kml` enthält
166 Gemeinden mit BFS-Nummern zwischen 0 und 298, `municipalities_canton_ZH.shp`
ebenfalls nur Zürich. Für eine Karte der 2087 Gemeinden sind sie unbrauchbar.

Verwendet wird stattdessen **swissBOUNDARIES3D von swisstopo**, Ausgabe 2026-01,
Ebene `tlm_hoheitsgebiet`. Geprüft am 07.11.2026: Alle 2087 Gemeinden unserer
Analysemenge sind darin enthalten, keine Lücke.

- Lizenz: kostenlose Geodaten von swisstopo, Nutzung und Bearbeitung erlaubt,
  **Quellenangabe Pflicht**. Wir verwenden `©swisstopo`, im Bild jeder Karte.
- Geholt per `scripts/hole_geodaten.py`. Die Rohdatei ist 36 MB und liegt **nicht**
  im Repo; die `.gitignore` schliesst `daten/geo/_roh/` aus.
- Im Repo liegt nur `daten/geo/gemeinden_2087.geojson`, 1.9 MB: unsere Gemeinden,
  ohne Höhendimension, mit 100 m Toleranz vereinfacht, in WGS84.

Details in `daten/geo/QUELLE.md`.

---

## 3. Festgelegte Entscheide

Diese Entscheide sind getroffen. Nicht ohne Rücksprache mit der Gruppe ändern.

- **Verbrauchskategorie H4**, 4500 kWh pro Jahr. Sonst vergleicht man Unvergleichbares.
- **produkt == "standard"**, nicht "cheapest". `cheapest` existiert nur dort, wo der
  Betreiber mehrere Produkte anbietet, und deckt je nach Jahr nur 742 bis 1207
  Gemeinden ab statt über 2100. Wer damit rechnet, vergleicht pro Jahr eine andere
  Auswahl und merkt es nicht.
- **Nur die 2087 Gemeinden**, die in allen drei Jahren vorkommen. 2021 sind es 2201,
  2024 noch 2140, 2027 noch 2109. Die Differenz sind Gemeindefusionen. Alle Zahlen in
  diesem Abschnitt beziehen sich auf die Auswahl H4/standard; die Rohdateien enthalten
  über alle Kategorien und beide Produkte mehr Gemeinden.
- **Mehrere Netzbetreiber pro Gemeinde**: betrifft 6 bis 7 Prozent, maximal fünf in
  einer Gemeinde. Mittelwert bilden und dokumentieren.
- **gemeinde_nr als Ganzzahl einlesen**, nicht als Text. Die ElCom-Daten haben keine
  führenden Nullen. Sonst findet `4811` seinen Partner `04811` nicht.
- **Die Grundgebühren stecken bereits im Rappenpreis.** Geklärt am 01.11.2026 an der
  ElCom-Wegleitung zur Tarifdeklaration 2026: Grund- und Leistungspreise werden in
  Rappen pro kWh umgerechnet, der Messtarif wird dabei berücksichtigt. Die
  veröffentlichten Rappenwerte enthalten die jährlichen Grundgebühren also schon,
  umgerechnet auf den Verbrauch der jeweiligen Kategorie. Der Kommentar in
  `strompreise_holen.py` stimmt, die Spalte `fixkosten` wird nicht gebraucht.
  Korrigiert: Hier stand vorher die Behauptung, die Analyse unterschätze die
  tatsächlichen Kosten bei hoher Grundgebühr. Das ist falsch.

### Beim Beschaffen immer alles holen

Aussortiert wird später im Code, nie an der Quelle. Wer eine Spalte beim Abholen
weglässt und sie später braucht, fängt von vorn an.

---

## 4. Messtarif ab 2026: ein Umbau, keine neue Position

Ab 2026 weist die ElCom den Messtarif **separat** aus. Er ist dadurch nicht neu
entstanden: Vorher steckte er in der Netznutzung.

> «Der Messtarif wird neu separat ausgewiesen. Er war bislang im Netznutzungstarif
> integriert», weshalb «grundsätzlich keine neue Belastung für die Endverbraucherinnen
> und Endverbraucher verbunden ist».
>
> ElCom, Mitteilung zu den Tarifen 2026,
> https://www.elcom.admin.ch/de/newnsb/8nuE_fvwnfqCu8OHNOwKu

Die Wegleitung zur Tarifdeklaration 2026 hält fest, dass die Messkosten ab 2026
eigenständig tarifiert werden und «nicht mehr Teil der Netznutzung» sind. Der
Grundpreis darf keine Komponenten für Messung und Zählermiete mehr enthalten, und der
Messtarif wird bei der Umrechnung von Grund- und Leistungspreis in Rappen pro kWh
berücksichtigt
(https://www.elcom.admin.ch/dam/elcom/de/dokumente/2025/wegleitung-tarife-2026.pdf.download.pdf).

**Was das für die Daten heisst:**

| | 2021 und 2024 | ab 2026, also 2027 |
|---|---|---|
| `netznutzung` | enthält die Messkosten | enthält sie **nicht** mehr |
| `messtarif` | leer | separat ausgewiesen |
| `total` | enthält die Messkosten | enthält sie ebenfalls |

**Folge für die Analyse:** Für den Vergleich über die Zeit **`total` verwenden**. Nur
`total` enthält in allen drei Jahren dieselben Bestandteile.

Die Summe der vier Bestandteile energie, netznutzung, abgaben und netzzuschlag ist
über die Jahre **nicht** vergleichbar: Für 2021 und 2024 ergibt sie den vollen Preis,
für 2027 den Preis **ohne** Messkosten. Wer so rechnet, macht 2027 künstlich um rund
1.67 Rappen billiger und unterschätzt den Preisanstieg.

Geprüft am 27.10.2026 über alle drei Dateien: `energie + netznutzung + abgaben +
netzzuschlag + messtarif` ergibt in jeder Zeile genau `total`, grösste Abweichung
0.001 Rappen aus der Rundung auf drei Nachkommastellen.

Für H4/standard beträgt der Messtarif 2027 im Mittel **1.67 Rappen**. Die ElCom nennt
als Referenzwert 1.65 Rp./kWh bei H4, das passt. Zu den Unterschieden **zwischen**
Gemeinden trägt er kaum bei: nur 0.4 Prozent der Streuung des Gesamtpreises.

Vollständigkeit 2027, geprüft am 30.10.2026: Bei H4/standard liefert 2027 2109
Gemeinden, die Datei insgesamt 41 440 Zeilen. 2027 liegt vollständig vor, ein
Ausweichen auf 2026 ist nicht nötig.

**Korrigiert am 01.11.2026.** Hier stand seit dem 27.10. die umgekehrte Regel: Den
Messtarif gebe es vor 2026 nicht, darum sei er beim Zeitvergleich wegzulassen. Diese
Annahme war plausibel, aber falsch, und sie war bereits in die ausgelieferten Daten
eingebaut. Aufgefallen ist sie nur, weil der Kommentar in `strompreise_holen.py` etwas
anderes sagte als diese Anleitung. Geklärt wurde sie an der ElCom-Dokumentation.

Dieser Vorgang gehört in die Integrationsdokumentation und in die AI-Dokumentation.

---

## 5. Bisherige Resultate

H4, standard, 2087 Gemeinden in allen drei Jahren, Gesamtpreis `total`:

| | 2021 | 2024 | 2027 |
|---|---|---|---|
| Mittelwert | 20.86 Rp | 31.99 Rp | 27.25 Rp |
| Standardabweichung | 2.99 | 3.71 | 3.05 |

Netto 2021 bis 2027: **+6.39 Rp**.
**10.9 Prozent** der Gemeinden (227 von 2087) sind 2027 wieder unter dem Niveau von
2021, 89.1 Prozent zahlen weiterhin mehr.

Korrigiert am 01.11.2026: Hier standen vorher eine Spalte «2027 bereinigt» mit
25.58 Rp, ein Netto von +4.72 Rp und 14.5 Prozent. Diese Zahlen beruhten auf der
falschen Annahme, der Messtarif sei 2027 neu hinzugekommen. Siehe Abschnitt 4.

Die Streuung ist dagegen fast wieder auf dem Vorkrisenniveau. Die Unterschiede
zwischen den Gemeinden haben sich normalisiert, das Preisniveau nicht.

### Welcher Bestandteil erklärt die Unterschiede zwischen Gemeinden

Anteil an der Streuung des Gesamtpreises, berechnet als Kovarianz(Bestandteil,
Gesamtpreis) geteilt durch Varianz(Gesamtpreis). Jede Spalte ergibt 100 Prozent:

| | 2021 | 2024 | 2027 |
|---|---|---|---|
| Energie | 32.0 % | 80.3 % | 44.8 % |
| Netznutzung | 55.8 % | 21.2 % | 54.4 % |
| Abgaben | 11.4 % | −1.4 % | 0.4 % |
| Netzzuschlag | 0.8 % | −0.0 % | −0.0 % |
| Messtarif | 0.0 % | 0.0 % | 0.4 % |

2021 erklärte die Netznutzung die Unterschiede, also die Geografie. 2024 kippte es
zur Energie, also zur Beschaffungsstrategie der Betreiber. 2027 schwingt es zurück.

Damit ist die Hauptfrage bereits messbar beantwortbar: Ja, die Zusammenhänge haben
sich verändert, und sie verändern sich gerade wieder zurück.

---

## 5b. Methodischer Vorbehalt: Preise werden pro Netzbetreiber gesetzt

Strompreise legen nicht die Gemeinden fest, sondern die Netzbetreiber. Alle Gemeinden
desselben Betreibers haben denselben Preis. Eine Gemeinde ist in unseren Daten also
keine eigenständige Beobachtung, sondern eine Verwaltungseinheit, die einem Betreiber
zugeordnet ist.

Nachgerechnet am 30.10.2026, H4/standard, die 2087 Gemeinden aus allen drei Jahren.
Weil 119 bis 150 Gemeinden mehrere Betreiber haben, ist jede Gemeinde dem Betreiber
mit der kleinsten `netzbetreiber_id` zugeordnet:

| | 2021 | 2024 | 2027 |
|---|---|---|---|
| Gemeinden | 2087 | 2087 | 2087 |
| Netzbetreiber | 512 | 496 | 485 |
| Varianz zwischen Betreibern | 98.0 % | 95.6 % | 96.8 % |
| Varianz innerhalb der Betreiber | 2.0 % | 4.4 % | 3.2 % |
| Grösster Betreiber versorgt | 257 | 314 | 315 Gemeinden |
| Betreiber mit nur einer Gemeinde | 414 | 396 | 387 |

**Folge:** Die 2087 Beobachtungen sind nicht unabhängig voneinander. Die effektive
Fallzahl liegt bei rund 500, nicht bei 2087.

**Folge für die Modellierung:** Standardfehler werden unterschätzt, p-Werte wirken
stärker als sie sind. Wer eine Gemeindevariable findet, die mit dem Preis korreliert,
findet womöglich nur die Betreiberzugehörigkeit.

**Empfehlung an Subraj:** Die Regression zusätzlich auf Betreiberebene rechnen, rund
500 Fälle, und die Koeffizienten vergleichen. Das ist zugleich ein Vergleich zwischen
Aggregationsebenen, wie ihn Pflicht 5 verlangt.

Dieser Vorbehalt gehört in die Interpretation (Pflicht 7) und in die Präsentation.
Ihn zu verschweigen wäre der grösste Angriffspunkt.

---

## 6. Arbeitsteilung

Aufgeteilt nach drei Regeln: Reihenfolge der Abhängigkeiten, Ferienplan, Know-how.

### Metehan, Daten und Infrastruktur

1. Öffentliches GitHub-Repo aufsetzen, alle einladen → Bonus 6
2. SPARQL-Abfrage bei ElCom, Preise pro Gemeinde über mehrere Jahre → Pflicht 1
3. SQLite-Datenbank mit SQL-Abfragen aus Python → Pflicht 3
4. PostgreSQL mit Joins und Aggregationen → Bonus 2

Laufend: eigene AI-Notizen, Code auf GitHub, technischer Support, vor allem für
Lennys Geodaten-Join. Im Januar: Video zusammenschneiden.

Die Reihenfolge zählt. PostgreSQL ist ein Bonuspunkt, die Datenbeschaffung und
SQLite sind Pflicht und blockieren die ganze Gruppe.

### Subraj, Analyse

1. Ausführliche EDA, grafisch und nicht-grafisch → Pflicht 4
2. t-Test, ANOVA und Korrelation, jeweils mit p-Wert → Bonus 4
3. Regressionsmodell mit Vergleich über die Zeit → Pflicht 5
4. Modellgüte bewerten, R² und RMSE → Pflicht 6
5. Interpretation der Resultate → Pflicht 7
6. k-means zusätzlich zum Modell → Bonus 5

Laufend: eigene AI-Notizen, Code auf GitHub. Im Januar: zip mit Daten und
Notebooks → Pflicht 9.

EDA und Statistik gehören zusammen: Wer die Verteilungen und Ausreisser gesehen hat,
weiss schon, welcher Test sich lohnt.

### Lenny, Datenaufbereitung und Darstellung

1. Zweite Datenquelle holen, BFS-Gemeindedaten → Pflicht 2
2. Probe-Join mit Metehans Daten, passen die Gemeindenummern
3. Vollständiger Join und Dokumentation: Matching-Keys, Widersprüche auflösen,
   verlorene und gewonnene Datensätze → Pflicht 2. Widersprüche heisst hier:
   abweichende Gemeindenamen und Schreibweisen, Gemeindefusionen, unterschiedliche
   Formate der Gemeindenummer
4. Prüfen, ob die ausgeschlossenen Gemeinden systematisch abweichen. Bei H4/standard
   umfasst 2021 2201 Gemeinden, 2027 noch 2109, behalten werden 2087. Die 114
   ausgeschlossenen sind Gemeindefusionen, und Fusionen treffen kleine und ländliche
   Gemeinden häufiger. Falls wir systematisch die kleinen ausschliessen, verzerrt das
   jede Aussage über Stadt und Land. Zu vergleichen sind Grösse, Kanton und
   Preisniveau der Ausgeschlossenen gegen die Behaltenen. Das Resultat gehört in die
   Integrationsdokumentation → Pflicht 2
5. Die Wahl von H4 und `produkt == "standard"` begründen, nicht nur festlegen. H4 ist
   die Kategorie, die ElCom und die Medien für den Durchschnittshaushalt verwenden,
   4500 kWh im Jahr. `standard` deckt über 2100 Gemeinden ab, `cheapest` je nach Jahr
   nur 742 bis 1207, was den Vergleich über die Zeit verfälschen würde. Beides gehört
   in den Bericht
6. Gemeindegrenzen und Karte → Bonus 3

Laufend: eigene AI-Notizen, Code auf GitHub, Punkteliste führen, AI-Doku aller drei
bündeln → Pflicht 8. Im Januar: PDF mit Anhang und Punkteauflistung.

### Alle drei

- Video, 15 Minuten, je 5 Minuten pro Person. Jeder spricht über seinen eigenen Teil
- Konzept-Präsentation am 8. Dezember, alle drei reden
- AI-Dokumentation laufend mitschreiben
- Notebooks kommentieren, solange man noch weiss warum
- Schlusskontrolle vor der Abgabe: Punkteliste zu dritt durchgehen

### Wer auf wen wartet

Kein Domino. Metehan und Lenny starten parallel und unabhängig. Sie treffen sich
beim Zusammenführen der zwei Datensätze, und das ist Lennys Aufgabe und der einzige
echte Engpass. Danach arbeiten alle drei gleichzeitig auf derselben Tabelle.

---

## 7. Punkteliste, 22 Punkte

| Nr | Anforderung | Wer |
|---|---|---|
| Pflicht 1 | Datenbeschaffung per Web Scraping oder Web API, keine fertigen Datensätze als Primärquelle | Metehan |
| Pflicht 2 | Zwei Quellen, Integration dokumentiert: Matching-Keys, Joins, Widersprüche auflösen, verlorene und gewonnene Datensätze | Lenny |
| Pflicht 3 | SQLite mit SQL-Abfragen aus Python | Metehan |
| Pflicht 4 | Ausführliche EDA, grafisch und nicht-grafisch | Subraj |
| Pflicht 5 | Regression oder Klassifikation, Forschungsfrage über reine Vorhersage hinaus | Subraj |
| Pflicht 6 | Modellgüte mit passenden Massen, R², RMSE, bei Klassifikation accuracy, recall, precision | Subraj |
| Pflicht 7 | Korrekte Interpretation der Resultate | Subraj |
| Pflicht 8 | Dokumentation der AI-Nutzung für den Code und die Präsentation | alle, Lenny bündelt |
| Pflicht 9 | Material auf Moodle verfügbar machen | Subraj |
| Bonus 1 | Kreativität, alles was nicht in Lektionen und Übungen vorkommt | alle |
| Bonus 2 | PostgreSQL zusätzlich, nicht SQLite, mit Joins und Aggregationen | Metehan |
| Bonus 3 | Integration und Visualisierung von Geodaten | Lenny |
| Bonus 4 | Chi-Quadrat, ANOVA oder Korrelation, jeweils mit p-Wert | Subraj |
| Bonus 5 | k-means zusätzlich zum Regressions- oder Klassifikationsmodell | Subraj |
| Bonus 6 | Öffentliches GitHub-Repo, URL in der Präsentation nennen | Metehan |
| Video, 7 Pkt | Sieben Kriterien, siehe unten. 15 Minuten, je 5 Minuten pro Person | alle drei |

### Die sieben Kriterien des Videos

1. Structure & outline
2. Topic presentation, Thema klar definiert und überzeugend präsentiert
3. Content, Substanz, Tiefe, Gewichtung der Teile
4. Language / auxiliary tools, frei gesprochen
5. Quality of the presentation & slides
6. Reflection on AI usage. Originalwortlaut: «the presentation (slides and video)
   must include which AI tools were used and how, the advantages and disadvantages
   you found when using AI, and where something did not work with the help of AI»
7. Time keeping: Länge in Minuten = Anzahl Studierende pro Gruppe × 5

Kriterium 6 ist eine eigene Anforderung zusätzlich zu Pflicht 8: Die AI-Reflexion
muss in den Folien und im Video vorkommen, nicht nur in der Dokumentation.

### Zur AI-Dokumentation

Verlangt ist nicht nur, welches Tool benutzt wurde, sondern auch wofür, welche
Vorteile und Nachteile aufgefallen sind, und besonders **wo etwas mit AI nicht
funktioniert hat**. Dieser letzte Teil wird am häufigsten vergessen und lässt sich
am Schluss nicht rekonstruieren. Laufend mitschreiben.

### Zum Anhang der Abgabe

Im Anhang des Präsentations-PDF muss stehen, was für welche Punkte gemacht wurde,
mit Screenshots und Code-Ausschnitten. Die Punkteliste ist also nicht nur internes
Hilfsmittel, sondern Teil der Abgabe.

Der Dozent bewertet aber nicht allein nach unserer Auflistung. Originalwortlaut:
«Note that the final evaluation will be made by the lecturer, not exclusively based
on your listing!»

---

## 8. Konzept-Präsentation, 8. Dezember

11:00 Uhr, Raum SW301, zehn Minuten für die Gruppe, alle drei reden.
Zählt 20 Prozent der Modulnote.

Gezeigt wird das Konzept, nicht das fertige Projekt: Hintergrund, Problemstellung,
Ziel, Forschungsfrage, Daten, Methoden und erwartete Resultate.

Jedes der acht Kriterien wird einzeln mit einer Note von 1 bis 6 bewertet, der
Durchschnitt ergibt die Note:

| Nr | Kriterium | Worauf geachtet wird |
|---|---|---|
| 1 | Struktur und Gliederung | Klare Gliederung, logischer Faden, ausgewogene Teile, klarer Titel, Namen aller Studenten |
| 2 | Hintergrund und Problem | Kontext klar, Problem überzeugend begründet |
| 3 | Ziel und Forschungsfrage | Klar definiert |
| 4 | Daten | Quelle gezeigt, Struktur der Daten erklärt |
| 5 | Methoden | Passend zur Forschungsfrage, korrekt beschrieben und begründet |
| 6 | Erwartete Resultate | Plausibel, mit Rückbezug auf die Forschungsfrage |
| 7 | Sprache | Frei gesprochen |
| 8 | Qualität der Präsentation | Grafiken, Tabellen und Folien nach wissenschaftlichem Standard |

Vier der acht Kriterien brauchen keine Daten: Struktur, Hintergrund, Forschungsfrage
und erwartete Resultate. Nur Kriterium 4 verlangt, dass die Daten bis dahin
tatsächlich vorliegen.

Auf Moodle gibt es zwei Abgaben, beide mit Frist 10.01.2027: das PDF der
Konzept-Präsentation und das Endprojekt. Das Präsentations-PDF laden wir trotzdem
schon vor dem 8. Dezember hoch, weil wir an dem Tag präsentieren.

---

## 9. Termine

Vom 1. bis 21. November fehlt durchgehend jemand. Nur Metehan ist die ganze Zeit da.

| Zeitraum | Metehan | Lenny | Subraj |
|---|---|---|---|
| bis 31.10. | SPARQL, Repo | BFS-Daten holen | noch da |
| 01.–11.11. | Daten hochskalieren | Probe-Join, Folien schreiben | Ferien |
| 12.–21.11. | SQLite | Ferien | Notebooks vorbereiten |
| 22.11.–08.12. | PostgreSQL, Support | Karte, Folien | EDA, Tests, Modell, k-means |
| **08.12., 11:00** | **Konzept-Präsentation, SW301, 10 Minuten** | | |
| 09.–20.12. | PostgreSQL fertig | Karte fertig | Analyse fertig |
| 21.–27.12. | Folien und PDF schreiben, Resultate einbauen | | |
| 28.12.–04.01. | Jeder nimmt seine 5 Minuten Video auf | | |
| 05.–08.01. | Video schneiden | PDF fertigstellen | zip packen |
| 09.01. | Schlusskontrolle zu dritt, Punkteliste durchgehen | | |
| **10.01.2027, 23:59** | **Abgabe auf Moodle** | | |

### Abzugeben am 10. Januar

- Videoaufnahme als mp4, Dateiname nach Schema `video_recording_group_XX.mp4`
- zip mit allen Daten und Notebooks, `materials_group_XX.zip`
- Präsentation als PDF, `presentation_group_XX.pdf`, mit Titel und vollständigen
  Namen, Einleitung, Material und Methoden, Resultate und Diskussion, Schluss,
  Reflexion zur AI-Nutzung und dem Anhang mit der Punkteauflistung

Die Gruppennummer ist noch zu klären.

---

## 10. Konventionen im Repo

**Jeder arbeitet in seinem eigenen Notebook.** Jupyter-Notebooks vertragen sich
schlecht mit Git. Bei gemeinsamer Bearbeitung entstehen Konflikte, die kaum sauber
aufzulösen sind, weil in der Datei nicht nur Code steht, sondern auch alle Ausgaben.

- `scripts/01_daten_bfs_lenny.ipynb` (Lenny, zweite Quelle und Join)
- `scripts/02_sqlite_metehan.ipynb` (Metehan, SQLite)
- `scripts/03_analyse_subraj.ipynb` (Subraj, EDA und Modell, noch anzulegen)

Die Nummern folgen der Reihenfolge der Arbeit, nicht den Personen: Erst der Join,
dann die Datenbank darauf, dann die Analyse.

Am Schluss werden die Resultate zusammengeführt, nicht die Dateien während der Arbeit.

### Ordnerstruktur

```
daten/strompreise/   ElCom-Rohdaten, eine CSV pro Jahr
daten/bfs/           BFS-Gemeindedaten mit Herkunftsnachweis
daten/verbunden/     die verbundene Tabelle für alle drei
scripts/             Beschaffungsskript und Notebooks
sql/                 SQLite-Datenbank
ai-doku/             AI-Dokumentation und Integrationsdokumentation
```

Die Notebooks liegen in `scripts/`, die Daten in `daten/`. Damit das aus jedem
Arbeitsverzeichnis funktioniert, bestimmt jedes Notebook in der ersten Code-Zelle die
Repo-Wurzel selber (`finde_wurzel`) und leitet alle Pfade davon ab. Keine relativen
Pfade wie `daten/bfs/...` direkt im Code.

**Wer Dateien verschiebt**, zieht die Pfade in beiden Notebooks und in
`scripts/strompreise_holen.py` nach und lässt beide Notebooks einmal durchlaufen.
Am 07.11.2026 wurde die Struktur umgebaut, ohne die Pfade nachzuziehen; danach brachen
beide Notebooks auf einem frischen Klon mit `FileNotFoundError` ab.

Lokal arbeiten oder in GitHub Codespaces ist beides erlaubt. Massgebend ist die
`requirements.txt`. Wer lokal arbeitet, legt eine virtuelle Umgebung `.venv` an und
installiert die Pakete daraus. So haben alle drei dieselben Pakete, unabhängig vom
Rechner.

---

## 11. Noch offen

- Gruppennummer von Moodle, für die Dateinamen bei der Abgabe
- Mail an die Dozenten für eine Ersteinschätzung, falls Fragen auftauchen.
  Laut Aufgabenstellung genügen zwei bis drei Sätze mit Thema und Forschungsfrage
- Wer lädt die drei Dateien hoch. Das Original verlangt, dass eine Person pro Gruppe
  Video, zip und PDF hochlädt. Das Erstellen bleibt auf drei Personen verteilt, aber
  die hochladende Person müssen wir bestimmen
- Datumsfehler auf Moodle bei der Abgabe des Endprojekts: Der Titel nennt den
  10.01.2027, das Fälligkeitsfeld darunter den 11.01.2026. Bei den Dozenten
  nachfragen
- Auf welcher Ebene erwartet der Dozent die Analyse, Gemeinde oder Netzbetreiber.
  In der Mail an die Dozenten fragen
- **Dritte Quelle nötig für Kanton, Sprachregion und Gemeindetypologie.** Weder die
  Regionalporträts noch die ElCom-Daten enthalten diese Merkmale, geprüft am
  01.11.2026. Ohne sie sind Unterfrage 1 (Unterschiede zwischen Kantonen und
  Sprachregionen) und die ANOVA dazu (Bonus 4) nicht rechenbar. Kanton und
  Sprachregion vermutlich aus dem amtlichen Gemeindeverzeichnis des BFS. Dringend,
  weil Subraj darauf wartet
- Gemeindetypologie, tiefste Priorität. Es gibt eine vom BFS und eine vom ARE; welche
  gemeint ist, in der Mail an die Dozenten mitfragen

---

## 12. Zuständigkeit für Dateien

Jeder bearbeitet nur seine eigenen Dateien. Fremde Dateien werden gelesen, aber nie
geändert. Wenn an einer fremden Datei etwas falsch scheint: der Person melden, nicht
selber korrigieren.

- Metehan: `scripts/strompreise_holen.py`, `query.txt`,
  `daten/strompreise/Daten_Strompreise_*.csv`, `scripts/02_sqlite_metehan.ipynb`,
  `sql/`, alles zu SQLite und PostgreSQL,
  `ai-doku/AI-Dokumentation_*_Metehan.md`
- Subraj: `scripts/03_analyse_subraj.ipynb`
- Lenny: `scripts/01_daten_bfs_lenny.ipynb`, `daten/bfs/`, `daten/verbunden/`,
  `README.md`, `CLAUDE Data Analytics.md`, `dokumentation_integration_lenny.md`,
  `punkteliste.md`, `folien_entwurf_lenny.md`,
  `ai-doku/ai_dokumentation_lenny.md`, `moodle_aufgabenstellung.pdf`

Beim Committen nur die eigenen Dateien auswählen, nie alles auf einmal.

### Quellenregel

Jede Zahl im Bericht und in der Präsentation stammt aus unseren eigenen Daten und ist
nachgerechnet. Medienberichte dienen nur der Einleitung als Beleg, dass das Thema
öffentlich diskutiert wird, nie als Beleg für eine Zahl.
