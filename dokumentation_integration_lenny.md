# Integration der zwei Datenquellen

**Pflichtanforderung 2** · Lenny Frei · Data Analytics, ZHAW, HS2026 · 1. November 2026

Der vollständige Weg mit Code und Ausgaben steht in `02_daten_bfs_lenny.ipynb`.
Dieses Dokument fasst zusammen, was zusammengeführt wurde, wie, und was dabei
verloren ging.

---

## 1. Die zwei Quellen

| | Quelle 1 | Quelle 2 |
|---|---|---|
| Inhalt | Strompreise pro Gemeinde | Gemeindemerkmale |
| Herausgeber | ElCom | Bundesamt für Statistik |
| Bezug | SPARQL-Endpunkt von LINDAS, eigenes Python-Skript | Download, `regionalportraets_2021.csv` |
| Zuständig | Metehan | Lenny |
| Datenstand | 2021, 2024, 2027 | 01.01.2021 |

Die Aufgabenstellung verlangt eigene Erhebung nur für die Primärquelle und nennt für
die Zweitquelle ausdrücklich das Beispiel «scraped data enriched with data from
opendataswiss». Der Download der BFS-Daten ist damit zulässig.

---

## 2. Der Matching-Key

Verbunden wird über die **BFS-Gemeindenummer**. Sie ist die amtliche, eindeutige
Nummer jeder Schweizer Gemeinde und kommt in beiden Quellen vor: als `gemeinde_nr` in
den ElCom-Daten, als `CODE_REGION` in den BFS-Daten.

**Warum er funktioniert.** Vor dem Join wurde das Format beider Seiten geprüft:

- Die BFS-Codes sind 1 bis 4 Stellen lang
- **Kein einziger Code hat eine führende Null**
- Beide Seiten werden als Ganzzahl eingelesen

Das ist der Punkt, an dem ein Join am häufigsten scheitert: Läge eine Seite als Text
mit führenden Nullen vor, würde `04811` seinen Partner `4811` nie finden. Hier war das
nicht der Fall, die Formate passen ohne Umbau zusammen.

Zusätzlich geprüft: In den BFS-Daten kommt **keine** Kombination aus Gemeinde und
Kennzahl doppelt vor. Ohne diese Kontrolle hätte der Pivot stillschweigend Werte
überschrieben.

---

## 3. Vorbereitung: vom Lang- ins Breitformat

Die BFS-Datei liegt im **Langformat** vor: eine Zeile pro Gemeinde *und* Kennzahl.
Aeugst am Albis belegt 41 Zeilen. Insgesamt sind es 89 093 Zeilen für 2172 Gemeinden.

Ein Join braucht eine Zeile pro Gemeinde. Mit `pivot` wurde die Tabelle gedreht: aus
41 Zeilen wird eine Zeile mit 39 Spalten. Ohne diesen Schritt wäre jede Gemeinde beim
Verbinden 41-mal aufgetaucht und die Preisdaten entsprechend vervielfacht worden.

Die Zeile für die ganze Schweiz (`CODE_REGION = "CH"`) wurde vorher entfernt, da sie
keine Gemeinde ist.

---

## 4. Unterschiedliche Bezugsjahre je Kennzahl

Obwohl die Datei «Regionalporträts 2021» heisst, stammen die Kennzahlen aus
verschiedenen Jahren:

| Kennzahl | Bezugsjahr | verwendet |
|---|---|---|
| Einwohner, Bevölkerungsdichte, Anteil 65+ | 2019 | ja |
| Beschäftigte | 2018 | ja |
| Fläche Total | 2016 | ja |
| **Siedlungsflächen und deren Veränderung** | **2004/2009** | **nein** |

**Ausgeschlossen** wurden `Ind_04_02` und `Ind_04_03`, die Siedlungsflächen. Daten aus
dem Zeitraum 2004/2009 gegen Strompreise von 2027 zu stellen, wäre nicht zu
verteidigen.

**Behalten** wurde die Gesamtfläche von 2016: Gemeindeflächen ändern sich praktisch
nur durch Fusionen, und Fusionsgemeinden sind ohnehin ausgeschlossen.

Die Einwohnerzahlen von 2019 sind gegenüber den Preisen von 2027 acht Jahre alt. Da
sich Einwohnerzahlen langsam ändern, ist das vertretbar, muss aber im Bericht stehen.

---

## 5. Ergebnis des Joins

| | |
|---|---|
| Gemeinden in der Analyse | **2087** |
| Partner in den BFS-Daten gefunden | **2087** |
| Trefferquote | **100.00 Prozent** |
| Verlorene Datensätze beim Join | **0** |
| Gewonnene Datensätze | 0 |

**Warum die Trefferquote vollständig ist.** Unsere 2087 Gemeinden sind die
Schnittmenge aller drei Preisjahre. Wer darin vorkommt, existierte also bereits 2021.
Die BFS-Daten haben den Stand 1.1.2021 und enthalten damit jede Gemeinde, die 2021
existierte.

Das ist kein Zufall, sondern eine Folge einer Entscheidung, die ursprünglich aus einem
anderen Grund getroffen wurde: Die Beschränkung auf die 2087 Gemeinden sollte die
**Vergleichbarkeit über die Zeit** sichern. Sie löst zusätzlich den
**Altersunterschied zwischen den beiden Quellen**. Ein Entscheid, zwei gelöste
Probleme.

---

## 6. Aufgelöste Widersprüche zwischen den Quellen

| Widerspruch | Auflösung |
|---|---|
| Langformat gegen Breitformat | Pivot der BFS-Daten vor dem Join |
| Gemeindenummer als Text gegen Ganzzahl | beidseitig als Ganzzahl eingelesen, Format vorher geprüft |
| Gemeindefusionen zwischen 2021 und 2027 | nur Gemeinden, die in allen drei Jahren vorkommen |
| Mehrere Netzbetreiber je Gemeinde | Mittelwert des Preises; für die Betreiberzuordnung der Betreiber mit der kleinsten `netzbetreiber_id` |
| Messtarif erst ab 2026 | eigene Spalte `vergleichbar` ohne Messtarif für den Zeitvergleich |
| Kennzahlen aus verschiedenen Jahren | zwei Kennzahlen ausgeschlossen, Bezugsjahre dokumentiert |

Zur Betreiberzuordnung: Die Regel «kleinste `netzbetreiber_id`» ist willkürlich, aber
**reproduzierbar**. Eine frühere Auswertung hatte den Betreiber genommen, der in der
CSV-Datei zufällig zuerst steht. Dieses Ergebnis hängt an der Zeilenreihenfolge und
ändert sich, sobald die SPARQL-Abfrage neu läuft.

---

## 7. Welche Gemeinden fallen aus der Analyse heraus, und sind sie zufällig verteilt?

Beim Join selbst geht nichts verloren. Verloren geht vorher und nachher – aus zwei
voneinander unabhängigen Gründen.

**Grund 1: Gemeindefusionen.** 2021 enthalten die ElCom-Daten bei H4/standard 2201
Gemeinden, 2027 noch 2109. Wer nicht in allen drei Jahren vorkommt, fällt weg: 114
Gemeinden.

**Grund 2: Datenschutz.** Das BFS unterdrückt Werte, wenn sie Rückschlüsse auf
einzelne Betriebe oder Personen zuliessen (Status `Q`). Bei den Beschäftigten trifft
das 88 unserer 2087 Gemeinden.

Beide Gründe klingen harmlos. Zusammen betrachtet sind sie es nicht:

| Gruppe | Anzahl | Median Einwohner | Median Preis 2021 |
|---|---|---|---|
| Behalten, alle fünf Merkmale vorhanden | 1999 | **1717** | 20.53 Rp |
| Raus: Beschäftigte unterdrückt | 88 | **313** | 21.03 Rp |
| Raus: Gemeindefusion | 114 | **669** | 21.14 Rp |

**Befund:** Beide ausgeschlossenen Gruppen sind deutlich **kleiner** und etwas
**teurer** als die behaltenen. Die Verzerrungen ziehen in dieselbe Richtung und
verstärken sich. Von den 2201 Gemeinden, die 2021 vorhanden waren, fallen 202 heraus,
also gut 9 Prozent – überdurchschnittlich die kleinen und ländlichen.

Für eine Aussage über Stadt und Land ist das erheblich. Wer die Verzerrung nicht
kennt, berichtet über eine Schweiz, in der die kleinen Gemeinden unterrepräsentiert
sind.

**Wie damit umgegangen wird.** Das Modell wird zweimal gerechnet:

1. mit den **vier vollständigen Merkmalen** auf allen **2087** Gemeinden
2. mit **allen fünf Merkmalen** auf den **1999** Gemeinden mit vollständigen Daten

Zeigen beide dasselbe Bild, ist die Verzerrung belanglos. Zeigen sie es nicht, ist das
selbst ein Resultat. Das ist eine Vorgabe an die Modellierung, nicht an die
Datenaufbereitung.

### Zur Wahl der Beschäftigten statt der Arbeitsstätten

Ursprünglich war `Ind_06_07` Arbeitsstätten als Merkmal für die gewerbliche Last
vorgesehen. Dort fehlen jedoch **269** statt 88 Werte, und die Lücken treffen ebenfalls
die kleinen Gemeinden. Gewählt wurde stattdessen `Ind_06_03` Beschäftigte Total:

- 181 Gemeinden mehr im Modell, 1999 statt 1818
- Die Korrelation zwischen beiden Kennzahlen beträgt **0.986**, inhaltlich messen sie
  dasselbe
- Beschäftigte sind sogar das bessere Mass: Für die Stromlast zählt, wie viele Menschen
  arbeiten, nicht wie viele Betriebe eingetragen sind. Eine Schreinerei mit 20
  Angestellten und ein Einmann-Treuhandbüro sind beide «eine Arbeitsstätte»

---

## 8. Ein bewusster Zug des Designs

Die BFS-Merkmale stammen aus **einer einzigen Erhebung** und sind für alle drei
Preisjahre **identisch**. Die Preise ändern sich zwischen 2021, 2024 und 2027, die
Gemeindemerkmale nicht.

Das ist kein Mangel, sondern ein sauberes Design: Jede Veränderung der
Regressionskoeffizienten zwischen den drei Jahren kommt damit **ausschliesslich von
der Preisseite**. Es gibt keine Vermischung mit sich gleichzeitig ändernden
Gemeindemerkmalen.

---

## 9. Die verbundene Tabelle

`daten/verbunden/strompreise_gemeinden.csv` · 2087 Zeilen · 15 Spalten

| Spalte | Inhalt |
|---|---|
| `gemeinde_nr` | BFS-Gemeindenummer, der Matching-Key |
| `gemeinde` | Gemeindename |
| `netzbetreiber_id`, `netzbetreiber` | Netzbetreiber, bei mehreren der mit der kleinsten id |
| `total_2021`, `total_2024`, `total_2027` | Gesamtpreis in Rappen pro kWh |
| `vergleichbar_2021`, `_2024`, `_2027` | Summe aus energie, netznutzung, abgaben, netzzuschlag – **ohne Messtarif** |
| `einwohner`, `dichte`, `flaeche_total`, `beschaeftigte`, `anteil_65plus` | die fünf Gemeindemerkmale |

**Wichtig für Metehan und Subraj:** Für Vergleiche **über die Zeit** die Spalten
`vergleichbar_*` verwenden, nicht `total_*`. Den Messtarif gibt es erst ab 2026; wer
`total` über die Jahre vergleicht, überschätzt den Anstieg 2027 um rund 1.67 Rappen.
`total_*` ist richtig für absolute Preise **eines einzelnen Jahres**.

Die Spalte `netzbetreiber_id` liegt bei, weil die Preise laut Abschnitt 5b der
Projektanleitung pro Netzbetreiber gesetzt werden und die Regression zusätzlich auf
dieser Ebene gerechnet werden soll.

---

## 10. Offen

- Kanton und Sprachregion aus dem amtlichen Gemeindeverzeichnis
- Gemeindegrenzen für die Karte, Bonus 3
- Gemeindetypologie, tiefste Priorität
