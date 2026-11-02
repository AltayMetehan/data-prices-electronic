# AI-Dokumentation: SQLite-Datenbank

ZHAW Data Analytics HS2026 · Altay Metehan · Stand 2. November 2026

## Überblick

Für die SQLite-Datenbank (Pflicht 3) hat Claude das Datenmodell entworfen, die Datenbank gebaut und das Notebook `02_sqlite_datenbank.ipynb` geschrieben. Das Ergebnis stimmt bei allen 2'087 Gemeinden mit Lennys Join überein.

| Punkt | Angabe |
| --- | --- |
| Tool | Claude (Anthropic), Modell Claude Opus 5.5, in der Claude-App |
| Datum | 2. November 2026 |
| Projektteil | Strompreise und BFS-Gemeindedaten in einer SQLite-Datenbank speichern und mit SQL aus Python abfragen |
| Eingaben | Meine drei Jahresdateien der Strompreise, die BFS-Regionalporträts 2021, Lennys verbundene Tabelle, unser Projektplan |
| Ergebnis | Notebook, Datenbank `strompreise.db` mit 5 Tabellen und 2 Views, 24 MB |

## Einsatzprotokoll

Eine einzige Anfrage («Wie mache ich die Tabellen in SQLite? Beschreiben und machen») löste sechs Arbeitsschritte aus.

| Nr | Was die AI gemacht hat | Ergebnis |
| --- | --- | --- |
| 1 | Alle Dateien untersucht: Zeilen, Duplikate, fehlende Werte, Summe der Preisbestandteile | 143'837 Preiszeilen, keine Duplikate, Summe geht überall auf |
| 2 | Nachgerechnet, wie Lenny bei mehreren Netzbetreibern pro Gemeinde den Preis gebildet hat | Mittelwert über die Netzbetreiber, bei allen 2'087 Gemeinden bestätigt |
| 3 | BFS-Codes (`Ind_01_01` usw.) Bezeichnungen zugeordnet, Websuche nach der offiziellen Liste | 5 Codes eindeutig über Lennys Spalten geprüft, 36 nur abgeleitet |
| 4 | Datenmodell entworfen: 5 Tabellen mit Primär- und Fremdschlüsseln, 2 Views für die Analyse | `gemeinde`, `netzbetreiber`, `tarif`, `indikator`, `kennzahl`, `v_preis_h4`, `v_analyse` |
| 5 | Notebook geschrieben: Tabellen anlegen, laden, prüfen, fünf Beispielabfragen mit GROUP BY, JOIN, CASE und Unterabfrage | Läuft ohne Fehler durch |
| 6 | Ergebnis gegen Lennys Datei verglichen | 0 Abweichungen in allen 8 Spalten |

## Wo es nicht funktioniert hat oder unsicher ist

Die grösste offene Stelle sind die Bezeichnungen der BFS-Kennzahlen: 36 von 41 sind nicht gegen eine offizielle Liste geprüft.

1. **BFS-Bezeichnungen nur abgeleitet.** Die BFS-Datei enthält nur Codes. Die AI hat online nach der offiziellen Liste gesucht, aber auf opendata.swiss keine Zuordnung gefunden. Sie hat die Bezeichnungen dann aus Plausibilität erschlossen, etwa Zürich mit 0.15 % Leerwohnungen. Sicher sind nur 5 Codes, deren Werte genau mit Lennys Spalten übereinstimmen. In der Datenbank sind die übrigen als `abgeleitet` markiert. Vor der Verwendung im Modell müssen wir sie mit der Kopfzeile der BFS-Originaldatei vergleichen.
2. **Notebook nicht in Jupyter ausgeführt.** In der Umgebung der AI liess sich Jupyter nicht installieren. Die AI hat deshalb ein eigenes Hilfsprogramm geschrieben, das die Zellen nacheinander ausführt und die Ausgaben ins Notebook schreibt. Der Code ist also gelaufen, aber nicht in einem echten Jupyter-Kernel. Das muss ich bei mir einmal nachholen.
3. **Falscher Erklärtext.** In der ersten Version stand, dass fusionierte Gemeinden von 2021 keinen Namen haben. Die Ausgabe zeigte aber 0 Gemeinden ohne Namen, weil die Namen vom BFS kommen. Die AI hat den Widerspruch selbst bemerkt und den Text korrigiert.
4. **Kein Median in SQLite.** SQLite hat keine Median-Funktion. Der Median wird darum in pandas berechnet, nicht in SQL.

## Vorteile und Nachteile

Die AI hat nicht nur Code geliefert, sondern auch Entscheidungen begründet. Wo Wissen fehlte, hat sie aber geraten.

**Vorteile**

- **Datenmodell mit Begründung.** Die AI hat erklärt, warum die Daten auf mehrere Tabellen verteilt werden und wozu Primär- und Fremdschlüssel dienen. Das Notebook kann ich so im Video erklären.
- **Lennys Logik nachgebaut.** Statt eine Methode anzunehmen, hat die AI nachgerechnet, wie Lenny den Preis pro Gemeinde gebildet hat. Datenbank und Join rechnen so mit denselben Zahlen.
- **Kontrollen eingebaut.** Fremdschlüssel, Summe der Preisbestandteile und Vergleich mit Lennys Datei laufen bei jedem Durchgang mit.
- **Weiterverwendbar.** Die Views sind für Subraj und Lenny gedacht, das Schema passt fast unverändert für PostgreSQL (Bonus 2).

**Nachteile**

- **Raten ohne Quelle.** Bei den BFS-Codes hat die AI Bezeichnungen erschlossen. Sie hat das zwar offen markiert, aber ein Fehler wäre im Modell schwer zu erkennen.
- **Mehr als gefragt.** Die AI hat auch erste Auswertungen gemacht, zum Beispiel Preise nach Gemeindegrösse. Das sind nur Mittelwerte ohne Test und noch keine Ergebnisse fürs Projekt.
- **Grösse der Datenbank.** Mit 24 MB ist die Datei gross für das Repo. Weil das Notebook sie neu erzeugt, gehört sie besser in `.gitignore`.

## Wie die Resultate überprüft wurden

Die Datenbank liefert bei allen 2'087 Gemeinden genau dieselben Werte wie Lennys unabhängig gebauter Join.

| Prüfung | Ergebnis |
| --- | --- |
| Zeilen geladen: tarif / kennzahl | 143'837 / 89'052, gleich viele wie in den CSV-Dateien |
| Verletzte Fremdschlüssel | 0 |
| Preiszeilen, bei denen die Bestandteile nicht das Total ergeben | 0 in allen drei Jahren |
| Gemeinden nur in der Datenbank oder nur bei Lenny | 0 / 0 |
| Abweichende Werte in `v_analyse` gegenüber Lennys Datei (Preise 2021/2024/2027, Einwohner, Dichte, Fläche, Beschäftigte, Anteil 65+) | 0 in allen 8 Spalten |

Offen ist noch: das Notebook bei mir in Jupyter laufen lassen und die 36 abgeleiteten BFS-Bezeichnungen mit der Originaldatei vergleichen.

## Fazit und Lehren

Die Datenbank ist verlässlich, weil sie gegen eine zweite, unabhängige Rechnung geprüft wurde. Die Bezeichnungen der BFS-Codes sind es noch nicht.

- **Gegen etwas Unabhängiges prüfen.** Lennys Join war der beste Test: Zwei Wege führen zu denselben Zahlen.
- **Unsicheres markieren lassen.** Die Spalte `label_quelle` zeigt, welche Angaben geprüft und welche nur geraten sind. Das sollte die AI immer so machen.
- **Ausgaben lesen, nicht nur den Code.** Der falsche Erklärtext fiel nur auf, weil die Ausgabe etwas anderes zeigte.
- **Alles gleich mitgeben.** Diesmal waren alle Dateien und der Projektplan von Anfang an dabei. Die AI musste deshalb nichts annehmen, anders als bei der Datenbeschaffung.

## Quellen

- [BFS Regionalporträts 2021: Kennzahlen aller Gemeinden (opendata.swiss)](https://ckan.opendata.swiss/dataset/regionalportrats-2021-kennzahlen-aller-gemeinden)
- [ElCom: Tarifdaten und Visualisierungen](https://www.elcom.admin.ch/en/tariff-data-and-visualisations)
