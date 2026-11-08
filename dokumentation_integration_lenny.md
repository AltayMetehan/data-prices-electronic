# Integration der zwei Datenquellen

**Pflichtanforderung 2** · Lenny Frei · Data Analytics, ZHAW, HS2026 · 1. November 2026

Der vollständige Weg mit Code und Ausgaben steht in
`scripts/01_daten_bfs_lenny.ipynb`.
Dieses Dokument fasst zusammen, was zusammengeführt wurde, wie, und was dabei
verloren ging.

---

## 1. Die Quellen

| | Quelle 1 | Quelle 2 | Quelle 3 |
|---|---|---|---|
| Inhalt | Strompreise pro Gemeinde | Gemeindemerkmale | Kanton, Sprachregion, Typologie |
| Herausgeber | ElCom | Bundesamt für Statistik | Bundesamt für Statistik |
| Bezug | SPARQL-Endpunkt, eigenes Python-Skript | Download, `regionalportraets_2021.csv` | Download, `raumgliederungen_2019.xlsx` |
| Zuständig | Metehan | Lenny | Lenny |
| Datenstand | 2021, 2024, 2027 | 01.01.2021 | 01.01.2019 |

Die Pflicht verlangt zwei Quellen; die dritte kam dazu, weil weder Quelle 1 noch
Quelle 2 Kanton oder Sprachregion enthalten. Details in Abschnitt 9b.

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
| Messtarif ab 2026 separat statt in der Netznutzung | für den Zeitvergleich `total` verwenden, siehe Abschnitt 4 der Projektanleitung |
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

Mediane allein tragen keine Aussage. Darum ein **Permutationstest** mit 20 000
Ziehungen: Die Werte beider Gruppen werden zufällig neu verteilt, und der p-Wert
sagt, wie oft der Zufall einen mindestens so grossen Unterschied erzeugt. Das
Verfahren braucht keine Verteilungsannahme, was hier passt, weil Einwohnerzahlen
stark rechtsschief sind.

Jede Gruppe gegen die richtige Vergleichsgruppe: Die Fusionsgemeinden fielen **vor**
dem Join heraus, sie werden mit allen 2087 verglichen. Die Gemeinden ohne
Beschäftigtenzahl sind Teil der 2087 und werden mit den übrigen 1999 verglichen.

| Gruppe | Einwohner, Diff. Median | p | Preis, Diff. Median | p | Preis, Diff. Mittel | p |
|---|---|---|---|---|---|---|
| Fusion (114), gegen alle 2087 | **−958** | **0.007** | +0.61 Rp | **0.009** | −0.03 Rp | 0.91 |
| Beschäftigte unterdrückt (88), gegen 1999 | **−1404** | **0.0003** | +0.50 Rp | 0.25 | +0.34 Rp | 0.30 |

**Befund, so weit die Zahlen tragen:**

**Nach Gemeindegrösse ist die Auswahl verzerrt.** Beide ausgeschlossenen Gruppen sind
deutlich kleiner, und beide Male ist der Unterschied klar belegt (p = 0.007 und
p = 0.0003). Von den 2201 Gemeinden, die 2021 vorhanden waren, fallen 202 heraus,
gut 9 Prozent, überdurchschnittlich die kleinen und ländlichen. Für jede Aussage über
Stadt und Land ist das erheblich.

**Nach Preisniveau ist eine Verzerrung nicht belegt.** Bei den Fusionsgemeinden liegt
zwar der Median 0.61 Rappen höher (p = 0.009), der **Mittelwert ist jedoch praktisch
identisch**: 20.83 gegen 20.86 Rappen, p = 0.91. Der höhere Median geht also auf die
Verteilungsform zurück, nicht auf ein insgesamt teureres Preisniveau. Bei der zweiten
Gruppe hält weder der Median (p = 0.25) noch der Mittelwert (p = 0.30) einer Prüfung
stand.

Eine frühere Fassung dieses Abschnitts sagte, beide Gruppen seien «deutlich kleiner
und etwas teurer». Der erste Teil stimmt, der zweite war ohne Test formuliert und ist
so nicht haltbar. Korrigiert am 08.11.2026.

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

## 7b. Wie viele Zeitebenen stecken in einer Zeile?

Die verbundene Tabelle sieht aus wie ein Stand. Sie ist aber aus fünf Quellen mit
fünf Gebietsständen und sechs Datenjahren zusammengesetzt. Wer das nicht weiss, liest
sie falsch.

| Spalte | Quelle | Gebietsstand | Bezugsjahr des Werts |
|---|---|---|---|
| `gemeinde_nr`, `gemeinde` | ElCom | je Tarifjahr | – |
| `netzbetreiber_id`, `netzbetreiber` | ElCom | Tarifjahr 2027 | 2027 |
| `anz_gemeinden_betreiber` | ElCom, abgeleitet | Tarifjahr 2027 | 2027 |
| `total_2021` | ElCom | Tarifjahr 2021 | **2021** |
| `total_2024` | ElCom | Tarifjahr 2024 | **2024** |
| `total_2027` | ElCom | Tarifjahr 2027 | **2027** |
| `energie_*`, `netznutzung_*`, `abgaben_*`, `netzzuschlag_*` | ElCom | je Tarifjahr | 2021, 2024, 2027 |
| `messtarif_2027` | ElCom | Tarifjahr 2027 | **2027** |
| `einwohner` | Regionalporträts | 01.01.2021 | **2019** |
| `dichte` | Regionalporträts | 01.01.2021 | **2019** |
| `anteil_65plus` | Regionalporträts | 01.01.2021 | **2019** |
| `beschaeftigte` | Regionalporträts | 01.01.2021 | **2018** |
| `flaeche_total` | Regionalporträts | 01.01.2021 | **2016** |
| `kanton`, `kanton_nr` | Raumgliederungen | 01.01.2019 | 2019 |
| `sprachregion` | Raumgliederungen | 01.01.2019 | Sprachgebiete 2011 |
| `gemeindetyp_9` | Raumgliederungen | 01.01.2019 | Typologie 2012 |
| Geometrie (`daten/geo/`) | swissBOUNDARIES3D | Ausgabe 2026-01 | 2026 |
| vier Fusionsfälle | Historisiertes Gemeindeverzeichnis | Mutationen 2018–2022 | – |

Die Bezugsjahre der BFS-Kennzahlen sind direkt aus der Spalte `PERIOD_REF` der
Rohdatei gelesen, nicht aus einer Beschreibung übernommen.

**Was das für die Interpretation bedeutet, ohne Beschönigung: Wir erklären Preise von
2021 bis 2027 mit Gemeindemerkmalen von 2016 bis 2019.** Bei der Gemeindefläche sind
das bis zu elf Jahre Abstand, bei den Einwohnerzahlen bis zu acht. Gemeindeflächen
ändern sich fast nur durch Fusionen, und Fusionsgemeinden haben wir ausgeschlossen –
dort ist der Abstand unkritisch. Einwohnerzahlen und Beschäftigte ändern sich dagegen
laufend. Eine Gemeinde, die zwischen 2019 und 2027 stark gewachsen ist, wird in
unserem Modell mit ihrer alten Grösse geführt.

Das ist keine Nachlässigkeit, sondern die Folge der Datenlage: Die Regionalporträts
2021 sind die aktuellste Ausgabe, die das BFS veröffentlicht hat. Es gehört aber als
Einschränkung in den Bericht und nicht nur in diese Dokumentation.

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

`daten/verbunden/strompreise_gemeinden.csv` · 2087 Zeilen · 30 Spalten

| Spalte | Inhalt |
|---|---|
| `gemeinde_nr` | BFS-Gemeindenummer, der Matching-Key |
| `gemeinde` | Gemeindename |
| `netzbetreiber_id`, `netzbetreiber` | Netzbetreiber, bei mehreren der mit der kleinsten id |
| `total_2021`, `total_2024`, `total_2027` | Gesamtpreis in Rappen pro kWh |
| `energie_*`, `netznutzung_*`, `abgaben_*`, `netzzuschlag_*` | die vier Preisbestandteile, je Jahr |
| `messtarif_2027` | Messtarif, gibt es erst ab 2026 |
| `einwohner`, `dichte`, `flaeche_total`, `beschaeftigte`, `anteil_65plus` | die fünf Gemeindemerkmale |
| `kanton`, `kanton_nr` | Kanton, Kürzel und Nummer |
| `sprachregion` | Deutsch, Französisch, Italienisch oder Rätoromanisch |
| `gemeindetyp_9` | Gemeindetypologie 2012, 9 Typen |
| `anz_gemeinden_betreiber` | Anzahl Gemeinden, die dieser Betreiber 2027 bei H4/standard beliefert |

**Wichtig für Metehan und Subraj:** Für Vergleiche über die Zeit **die Spalten
`total_*` verwenden**. Nur sie enthalten in allen drei Jahren dieselben Bestandteile.

Die vier Preisbestandteile liegen bei, weil Unterfrage 1 danach fragt, welcher
Bestandteil die Unterschiede ausmacht. Zwei Regeln dazu:

1. **Innerhalb eines Jahres** ergeben die Bestandteile den Gesamtpreis: 2021 und 2024
   vier, 2027 fünf (mit Messtarif). Nachgerechnet, grösste Abweichung 0.001 Rappen.
2. **Über die Jahre ist `netznutzung` nicht vergleichbar.** Bis 2024 steckten die
   Messkosten darin, ab 2026 stehen sie separat. Für einen Zeitvergleich der
   Netzkosten `netznutzung_2027 + messtarif_2027` rechnen. `energie`, `abgaben` und
   `netzzuschlag` sind unmittelbar vergleichbar.

Eine Summe aus energie, netznutzung, abgaben und netzzuschlag ist über die Jahre
**nicht** vergleichbar: Bis 2024 steckten die Messkosten in der Netznutzung, ab 2026
werden sie separat als `messtarif` ausgewiesen. Eine solche Summe wäre für 2027 um
rund 1.67 Rappen zu tief.

**Korrigiert am 01.11.2026.** Diese Datei enthielt zuvor drei Spalten
`vergleichbar_2021/2024/2027` mit genau dieser falschen Summe, verbunden mit der
Empfehlung, sie für den Zeitvergleich zu verwenden. Die Spalten wurden entfernt, statt
nur umbenannt: Eine Spalte, die niemand verwenden soll, wird früher oder später
verwendet. Hintergrund in Abschnitt 4 der Projektanleitung.

Die Spalte `netzbetreiber_id` liegt bei, weil die Preise laut Abschnitt 5b der
Projektanleitung pro Netzbetreiber gesetzt werden und die Regression zusätzlich auf
dieser Ebene gerechnet werden soll.

---

## 9b. Dritte Quelle: Kanton, Sprachregion und Gemeindetypologie

Weder die ElCom-Preisdaten noch die Regionalporträts enthalten diese drei Merkmale.
Ohne sie ist Unterfrage 1 der Forschungsfrage – die Unterschiede zwischen Kantonen
und Sprachregionen – nicht zu beantworten.

| | |
|---|---|
| Datensatz | Die Raumgliederungen der Schweiz 2019 |
| Herausgeber | Bundesamt für Statistik |
| Bezogen am | 07.11.2026, per `scripts/hole_zusatzdaten.py` |
| Lizenz | OPEN-BY, freie Nutzung mit Quellenangabe |
| Gebietsstand | **01.01.2019** |
| Join-Schlüssel | `BFS Gde-nummer`, Ganzzahl ohne führende Nullen |

Übernommen werden vier Spalten: `kanton`, `kanton_nr`, `sprachregion` und
`gemeindetyp_9` (Gemeindetypologie 2012, 9 Typen). Die Sprachregion steht in der
Datei als Zahl; die Codeliste im selben Dokument lautet 1 = Deutsch,
2 = Französisch, 3 = Italienisch, 4 = Rätoromanisch. In unserer Tabelle steht der
Klartext, nicht der Code.

### Widerspruch: ein Gebietsstand, der zwei Jahre zu alt ist

Die Raumgliederungen haben den Stand 01.01.2019, unsere Analysemenge stammt aus den
Preisdaten von 2021. **Vier unserer 2087 Gemeinden fehlen**, weil sie erst 2020 und
2021 durch Fusion entstanden sind.

Aufgelöst wurde das **nicht von Hand**, sondern über die Mutationstabelle des
historisierten Gemeindeverzeichnisses des BFS. Jede Zeile dort verbindet eine
Vorgängergemeinde (`InitialCode`) mit ihrer Nachfolgerin (`TerminalCode`). Die
Merkmale der Nachfolgerin werden von den Vorgängern übernommen – aber nur, wenn
diese übereinstimmen. Eine Fusion über eine Kantons- oder Sprachgrenze hätte keinen
eindeutigen Wert ergeben; das wird im Code geprüft, nicht angenommen.

| Nr | Gemeinde | Fusion | Vorgänger | Kanton | Sprachregion | Typ 9 |
|---|---|---|---|---|---|---|
| 889 | Thurnen | 01.01.2020 | 873 Kirchenthurnen, 874 Lohnstorf, 876 Mühlethurnen | BE (alle) | Deutsch (alle) | 22 (alle) |
| 2117 | Villaz | 01.01.2020 | 2111 Villaz-Saint-Pierre, 2116 La Folliaz | FR (alle) | Französisch (alle) | 32 (alle) |
| 2237 | Prez | 01.01.2020 | 2185 Corserey, 2213 Noréaz, 2221 Prez-vers-Noréaz | FR (alle) | Französisch (alle) | **uneinheitlich: 32, 23, 23** |
| 2430 | Welschenrohr-Gänsbrunnen | 01.01.2021 | 2423 Gänsbrunnen, 2429 Welschenrohr | SO (alle) | Deutsch (alle) | 32 (alle) |

Bei drei der vier Gemeinden stimmen alle Vorgänger in allen Merkmalen überein; die
Übernahme ist eindeutig.

**Offen bei Prez (2237):** Kanton und Sprachregion sind eindeutig und wurden
übernommen. Die Gemeindetypologie der drei Vorgänger ist es nicht – Corserey hatte
Typ 32, Noréaz und Prez-vers-Noréaz Typ 23. Es gibt keinen sachlich zwingenden Wert,
darum steht dort vorläufig kein Eintrag. Das ist der einzige fehlende Wert in den
vier neuen Spalten, bei 2087 Gemeinden.

### Kontrollen nach dem Verbinden

| Prüfung | Ergebnis |
|---|---|
| Zeilen | 2087, unverändert |
| Fehlende Werte in `kanton`, `kanton_nr`, `sprachregion` | 0 |
| Fehlende Werte in `gemeindetyp_9` | 1 (Prez, siehe oben) |
| Anzahl Kantone | 26 |
| Die zwölf bisherigen Spalten | **0 abweichende Werte**, Spalten- und Zeilenreihenfolge identisch |

### Verteilung über die Sprachregionen

| | unsere 2087 | alle 2212 Gemeinden der Schweiz |
|---|---|---|
| Deutsch | 1365 (65.4 %) | 1421 (64.2 %) |
| Französisch | 595 (28.5 %) | 641 (29.0 %) |
| Italienisch | 111 (5.3 %) | 130 (5.9 %) |
| Rätoromanisch | 16 (0.8 %) | 20 (0.9 %) |

Die Anteile stimmen fast genau mit der Gesamtschweiz überein. Unsere Auswahl ist
sprachregional also **nicht verzerrt** – anders als bei Gemeindegrösse und
Preisniveau, siehe Abschnitt 7.

Ein Hinweis für den Bericht: Gemessen an der **Bevölkerung** ist die Deutschschweiz
rund drei Viertel gross, gemessen an der **Zahl der Gemeinden** nur rund zwei
Drittel. Die Westschweiz hat viele kleine Gemeinden. Wer die Gemeindezahl mit dem
Bevölkerungsanteil verwechselt, hält unsere Zahlen für falsch.

---

## 9c. Gemeindegrenzen für die Karte (Bonus 3)

| | |
|---|---|
| Datensatz | swissBOUNDARIES3D, Ausgabe 2026-01, Ebene `tlm_hoheitsgebiet` |
| Herausgeber | swisstopo |
| Bezogen am | 07.11.2026, per `scripts/hole_geodaten.py` |
| Lizenz | kostenlose Geodaten, Bearbeitung erlaubt, Quellenangabe `©swisstopo` Pflicht |
| Join-Schlüssel | `bfs_nummer`, Ganzzahl, bei uns `gemeinde_nr` |
| Abdeckung | **alle 2087 Gemeinden vorhanden, 0 Lücken** |

Die Rohdatei ist 36 MB gepackt und liegt nicht im Repo. Im Repo liegt nur die
abgeleitete Datei `daten/geo/gemeinden_2087.geojson` mit 1.9 MB: nur unsere
Gemeinden, ohne Höhendimension, mit 100 m Toleranz vereinfacht und von LV95
(EPSG:2056) nach WGS84 (EPSG:4326) umgerechnet. Einzelheiten in
`daten/geo/QUELLE.md`.

### Was die Karten zeigen

Zwei Karten, je als PNG mit 300 dpi für die Präsentation und als interaktive
HTML-Karte: das Preisniveau 2027 und die Veränderung 2021 bis 2027.

Die Veränderungskarte beantwortet die Hypothese aus Abschnitt 5b der
Projektanleitung – folgen die Preisgrenzen den Versorgungsgebieten oder den
Kantonsgrenzen? Gemessener Anteil der Preisstreuung, der zwischen den Gruppen liegt:

| Jahr | Kanton | Netzbetreiber | Sprachregion |
|---|---|---|---|
| 2021 | 60.3 % | **95.0 %** | 3.0 % |
| 2024 | 23.1 % | **94.0 %** | 1.7 % |
| 2027 | 35.2 % | **96.8 %** | 0.4 % |

Auf der Karte sichtbar als grosse einfarbige Flächen über Dutzende von Gemeinden,
die quer über Kantonsgrenzen laufen – am deutlichsten der blaue Block um Zürich,
Zug und den Aargau, wo die Preise 2027 wieder unter dem Niveau von 2021 liegen.

**Einschränkung:** Kanton und Netzbetreiber sind nicht unabhängig. Viele grosse
Versorger sind historisch kantonale Werke. Der Kantonsanteil von 23 bis 60 Prozent
entsteht deshalb grösstenteils dadurch, dass Kantonsgrenze und Betreibergrenze oft
zusammenfallen. Die Karte zeigt, welche Grenze die schärfere ist, nicht welche die
Ursache ist.

**Zur Skalierung beider Karten:** Die Farbskalen sind an den Rändern gekappt, weil
93.8 Prozent der Gemeinden zwischen 20 und 32 Rappen liegen, die Spanne aber bis
45.9 reicht. Bei der Veränderungskarte liegt der Nullpunkt in der Mitte der
Farbskala, die Äste sind unterschiedlich lang (−2.1 gegen +27.7). Eine symmetrische
Skala hätte die 227 günstiger gewordenen Gemeinden unsichtbar gemacht; der Preis
dafür ist, dass gleich kräftiges Blau und Rot nicht gleich viele Rappen bedeuten.
Beides steht so auch im Notebook.

---

## 10. Eine Annahme, die sich als falsch erwies

Vom 27.10. bis zum 01.11.2026 galt in diesem Projekt die Regel, der Messtarif sei ab
2026 neu hinzugekommen und für den Vergleich über die Zeit wegzulassen. Die Regel war
plausibel: Das Feld ist 2021 und 2024 leer und 2027 gefüllt.

Sie war falsch. Die ElCom schreibt zu den Tarifen 2026: «Der Messtarif wird neu separat
ausgewiesen. Er war bislang im Netznutzungstarif integriert.» Die Messkosten gab es
vorher also auch, sie standen nur in einer anderen Spalte.

Die Folge der falschen Regel wäre gewesen, dass 2027 ohne Messkosten gegen 2021 mit
Messkosten verglichen wird – 2027 also um rund 1.67 Rappen zu billig erscheint und der
Preisanstieg unterschätzt wird.

Aufgefallen ist es nur, weil der Kommentar in Metehans Beschaffungsskript etwas anderes
sagte als die Projektanleitung. Zu diesem Zeitpunkt war die Annahme bereits in die
ausgelieferte Tabelle eingebaut und Subraj empfohlen worden.

Betroffene Zahlen, korrigiert:

| | vorher | richtig |
|---|---|---|
| Mittelwert 2027 | 25.58 Rp | **27.25 Rp** |
| Netto 2021 bis 2027 | +4.72 Rp | **+6.39 Rp** |
| Gemeinden unter dem Niveau 2021 | 14.5 % | **10.9 %** |

---

## 11. Offen

- Gemeindetypologie von Prez (2237): Die Vorgänger hatten unterschiedliche Typen,
  siehe Abschnitt 9b. Entweder bleibt der Wert leer, oder die Gruppe legt eine
  nachvollziehbare Regel fest
