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

Die Hypothese, die geprüft wird: Nicht die Geografie über die Netzkosten erklärt die
Unterschiede zwischen Gemeinden, sondern die Beschaffungsstrategie der Netzbetreiber
über den Energieanteil. Und dieses Gewicht hat sich mit der Krise verschoben.

---

## 2. Daten

### Quelle 1, primär: ElCom Strompreise

Über den SPARQL-Endpunkt von LINDAS, `https://lindas.admin.ch/query`,
Datensatz `https://lindas.admin.ch/elcom/electricityprice`.

Abgeholt per Python-Skript, nicht von Hand heruntergeladen. Das ist Pflicht:
Die Aufgabenstellung verlangt Erhebung per Web Scraping oder Web API und schliesst
fertige Datensätze als Primärquelle ausdrücklich aus.

Dateien im Repo: `Daten_Strompreise_2021.csv`, `_2024.csv`, `_2027.csv`.
Skript: `strompreise_holen.py`. Abfrage: `query.txt`.

Spalten: jahr, gemeinde_nr, gemeinde, netzbetreiber_id, netzbetreiber, produkt,
kategorie, total, energie, netznutzung, abgaben, netzzuschlag, fixkosten.

### Quelle 2: Gemeindedaten des Bundesamts für Statistik

Regionalporträts: Einwohner, Fläche, Dichte, Gemeindetypologie, Kanton, Sprachregion.
Verknüpfung über die BFS-Gemeindenummer.

Für die zweite Quelle ist ein Download zulässig. Die Vorgabe zur eigenen Erhebung
gilt nur für die Primärquelle, die Aufgabenstellung nennt als Beispiel ausdrücklich
«scraped data enriched with data from opendataswiss».

---

## 3. Festgelegte Entscheide

Diese Entscheide sind getroffen. Nicht ohne Rücksprache mit der Gruppe ändern.

- **Verbrauchskategorie H4**, 4500 kWh pro Jahr. Sonst vergleicht man Unvergleichbares.
- **produkt == "standard"**, nicht "cheapest". `cheapest` existiert nur dort, wo der
  Betreiber mehrere Produkte anbietet, und deckt je nach Jahr nur 742 bis 1207
  Gemeinden ab statt über 2100. Wer damit rechnet, vergleicht pro Jahr eine andere
  Auswahl und merkt es nicht.
- **Nur die 2087 Gemeinden**, die in allen drei Jahren vorkommen. 2021 sind es 2203,
  2024 noch 2140, 2027 noch 2109. Die Differenz sind Gemeindefusionen.
- **Mehrere Netzbetreiber pro Gemeinde**: betrifft 6 bis 7 Prozent, maximal fünf in
  einer Gemeinde. Mittelwert bilden und dokumentieren.
- **gemeinde_nr als Ganzzahl einlesen**, nicht als Text. Die ElCom-Daten haben keine
  führenden Nullen. Sonst findet `4811` seinen Partner `04811` nicht.
- **Fixkosten bleiben aussen vor.** Die jährliche Grundgebühr in Franken wird nicht
  umgerechnet und nicht dazugezählt, weil nicht dokumentiert ist, wie sie im
  Gesamtpreis berücksichtigt ist. Als Einschränkung im Bericht erwähnen: Für
  Gemeinden mit hoher Grundgebühr unterschätzt die Analyse die tatsächlichen Kosten.

### Beim Beschaffen immer alles holen

Aussortiert wird später im Code, nie an der Quelle. Wer eine Spalte beim Abholen
weglässt und sie später braucht, fängt von vorn an.

---

## 4. Bekanntes Datenproblem: Messtarif ab 2026

In 2021 und 2024 ergibt die Summe aus energie, netznutzung, abgaben und netzzuschlag
exakt den Wert in `total`, die grösste Abweichung ist 0.001 Rappen. In 2027 fehlen
im Schnitt 1.675 Rappen, und zwar bei 100 Prozent der Zeilen. Ursache ist ein
Bestandteil, den die ElCom ab 2026 zusätzlich ausweist.

**Folge für die Analyse:** Für den Vergleich über die Zeit die vier Bestandteile
summieren, nicht `total` verwenden. Diese vier gibt es in allen drei Jahren.
`total` nur für absolute Preise eines einzelnen Jahres.

Ohne diese Korrektur wird der Preisanstieg um rund 1.7 Rappen überschätzt.

Dieser Fund gehört in die Integrationsdokumentation. Eine Veränderung der
Datenstruktur mitten im Vergleichszeitraum zu finden und zu korrigieren ist genau
das, was die Aufgabenstellung bei Integration und Interpretation bewertet.

---

## 5. Bisherige Resultate

H4, standard, 2087 Gemeinden in allen drei Jahren:

| | 2021 | 2024 | 2027 | 2027 bereinigt |
|---|---|---|---|---|
| Mittelwert | 20.86 Rp | 31.99 Rp | 27.25 Rp | 25.58 Rp |
| Standardabweichung | 2.99 | 3.71 | 3.05 | 3.05 |

Netto 2021 bis 2027 bereinigt: **+4.72 Rp**.
**14.5 Prozent** der Gemeinden sind 2027 wieder unter dem Niveau von 2021,
85.5 Prozent zahlen weiterhin mehr.

Die Streuung ist dagegen fast wieder auf dem Vorkrisenniveau. Die Unterschiede
zwischen den Gemeinden haben sich normalisiert, das Preisniveau nicht.

### Welcher Bestandteil erklärt die Unterschiede zwischen Gemeinden

Anteil an der Streuung des Gesamtpreises:

| | 2021 | 2024 | 2027 |
|---|---|---|---|
| Energie | 31.6 % | 79.6 % | 44.8 % |
| Netznutzung | 56.6 % | 21.8 % | 54.5 % |
| Abgaben | 11.1 % | −1.3 % | 0.4 % |

2021 erklärte die Netznutzung die Unterschiede, also die Geografie. 2024 kippte es
zur Energie, also zur Beschaffungsstrategie der Betreiber. 2027 schwingt es zurück.

Damit ist die Hauptfrage bereits messbar beantwortbar: Ja, die Zusammenhänge haben
sich verändert, und sie verändern sich gerade wieder zurück.

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
3. Vollständiger Join und Dokumentation: Matching-Keys, verlorene Datensätze → Pflicht 2
4. Gemeindegrenzen und Karte → Bonus 3

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
| Pflicht 2 | Zwei Quellen, Integration dokumentiert: Matching-Keys, Joins, verlorene und gewonnene Datensätze | Lenny |
| Pflicht 3 | SQLite mit SQL-Abfragen aus Python | Metehan |
| Pflicht 4 | Ausführliche EDA, grafisch und nicht-grafisch | Subraj |
| Pflicht 5 | Regression oder Klassifikation, Forschungsfrage über reine Vorhersage hinaus | Subraj |
| Pflicht 6 | Modellgüte mit passenden Massen, R², RMSE | Subraj |
| Pflicht 7 | Korrekte Interpretation der Resultate | Subraj |
| Pflicht 8 | Dokumentation der AI-Nutzung | alle, Lenny bündelt |
| Pflicht 9 | Material auf Moodle verfügbar machen | Metehan |
| Bonus 1 | Kreativität, alles was nicht in Lektionen und Übungen vorkommt | alle |
| Bonus 2 | PostgreSQL zusätzlich, nicht SQLite, mit Joins und Aggregationen | Metehan |
| Bonus 3 | Integration und Visualisierung von Geodaten | Lenny |
| Bonus 4 | Chi-Quadrat, ANOVA oder Korrelation, jeweils mit p-Wert | Subraj |
| Bonus 5 | k-means zusätzlich zum Regressions- oder Klassifikationsmodell | Subraj |
| Bonus 6 | Öffentliches GitHub-Repo, URL in der Präsentation nennen | Metehan |
| Video, 7 Pkt | 15 Minuten, je 5 Minuten pro Person | alle drei |

### Zur AI-Dokumentation

Verlangt ist nicht nur, welches Tool benutzt wurde, sondern auch wofür, welche
Vorteile und Nachteile aufgefallen sind, und besonders **wo etwas mit AI nicht
funktioniert hat**. Dieser letzte Teil wird am häufigsten vergessen und lässt sich
am Schluss nicht rekonstruieren. Laufend mitschreiben.

### Zum Anhang der Abgabe

Im Anhang des Präsentations-PDF muss stehen, was für welche Punkte gemacht wurde,
mit Screenshots und Code-Ausschnitten. Die Punkteliste ist also nicht nur internes
Hilfsmittel, sondern Teil der Abgabe.

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

Das PDF der Präsentation wird vor dem 8. Dezember auf Moodle hochgeladen. Die dort
angegebene Frist vom 10. Januar ist mit hoher Wahrscheinlichkeit ein Kopierfehler.

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

- `01_daten_elcom_metehan.ipynb`
- `02_daten_bfs_lenny.ipynb`
- `03_analyse_subraj.ipynb`

Am Schluss werden die Resultate zusammengeführt, nicht die Dateien während der Arbeit.

Die Umgebung ist GitHub Codespaces mit Python und Jupyter. Es wird nichts lokal
installiert, damit alle drei dieselbe Umgebung haben.

---

## 11. Noch offen

- Gruppennummer von Moodle, für die Dateinamen bei der Abgabe
- Ob der Messtarif ab 2026 als eigene Spalte aus der SPARQL-Abfrage zu holen ist
- Ob 2027 in den ElCom-Daten vollständig vorliegt, sonst 2026 nehmen
- Mail an die Dozenten für eine Ersteinschätzung, falls Fragen auftauchen.
  Laut Aufgabenstellung genügen zwei bis drei Sätze mit Thema und Forschungsfrage
