# Glossar für die Übersetzung ins Englische

Stand: 24. November 2026 · angelegt von Lenny · **Frist für alle drei: Freitag, 27. November**

Diese Datei ist ein **Arbeitsmittel, keine Abgabe.** Sie darf deutsch bleiben.
Sie existiert, damit wir drei denselben Begriff nicht dreifach verschieden
übersetzen. Wer übersetzt, schaut hier zuerst nach.

**Wenn ein Begriff hier fehlt:** eintragen, als 🟡 markieren, und den anderen
zwei sagen. Nicht einfach entscheiden und weitergehen.

## Statusmarkierungen

| | Bedeutung |
|---|---|
| ✅ | **Geprüft.** Offizielle englische Schreibweise, Quelle steht dabei. So und nicht anders. |
| 🟡 | **Vorschlag.** Sprachlich sinnvoll, aber nicht offiziell belegt. Darf überstimmt werden, dann aber für alle drei. |
| ⚠️ | **Konflikt oder offene Frage.** Vor dem Übersetzen klären. |

---

# 1. Nicht übersetzen

Diese Namen stehen gleichzeitig in der CSV, in SQLite, in PostgreSQL und in der
SPARQL-Abfrage. **Wer sie ändert, bricht das Projekt.** Ein Spaltenname ist kein
Text, auch wenn er wie ein deutsches Wort aussieht.

## 1.1 Spaltennamen der Analysetabelle

Geprüft gegen die Kopfzeile von `daten/verbunden/strompreise_gemeinden.csv`,
alle 30 in der echten Reihenfolge:

```
gemeinde_nr        gemeinde           netzbetreiber_id   netzbetreiber
total_2021         total_2024         total_2027
energie_2021       netznutzung_2021   abgaben_2021       netzzuschlag_2021
energie_2024       netznutzung_2024   abgaben_2024       netzzuschlag_2024
energie_2027       netznutzung_2027   abgaben_2027       netzzuschlag_2027
messtarif_2027
einwohner          dichte             flaeche_total      beschaeftigte
anteil_65plus      kanton             kanton_nr          sprachregion
gemeindetyp_9      anz_gemeinden_betreiber
```

## 1.2 Tabellen und Views in SQLite und PostgreSQL

Geprüft gegen `sqlite_master` in `sql/strompreise.db`:

```
Tabellen:  gemeinde   indikator   kennzahl   netzbetreiber   tarif
Views:     v_analyse  v_preis_h4
```

## 1.3 Ordner und Pfade

```
daten/            daten/strompreise/   daten/bfs/      daten/geo/
daten/verbunden/  daten/raumgliederungen/
scripts/          sql/                 ai-doku/
abbildungen/      karten/
```

⚠️ Drei davon fehlten in der ursprünglichen Liste und sind hier ergänzt:
`daten/raumgliederungen/`, `abbildungen/`, `karten/`.

## 1.4 Dateinamen

Alle. Vollständige Liste der versionierten Dateien:

```
query.txt                                    <- liegt im Repo-Root, nicht in scripts/
requirements.txt                             .gitignore

scripts/strompreise_holen.py                 scripts/hole_zusatzdaten.py
scripts/hole_geodaten.py
scripts/01_daten_bfs_lenny.ipynb             scripts/02_sqlite_metehan.ipynb
scripts/03_analyse_subraj.ipynb              scripts/04_modell_subraj.ipynb
sql/03_postgresql.ipynb                      sql/strompreise.db

daten/strompreise/Daten_Strompreise_2021.csv            (ebenso 2024, 2027)
daten/bfs/gemeindeverzeichnis_2021.csv
daten/bfs/gemeindemutationen_2018_2022.csv
daten/bfs/regionalportraets_2021.csv
daten/raumgliederungen/raumgliederungen_2019.xlsx
daten/geo/gemeinden_2087.geojson
daten/verbunden/strompreise_gemeinden.csv

abbildungen/karte_preisniveau_2027.png
abbildungen/karte_veraenderung_2021_2027.png
karten/karte_preisniveau_2027.html
karten/karte_veraenderung_2021_2027.html

daten/bfs/QUELLE.md   daten/geo/QUELLE.md   daten/raumgliederungen/QUELLE.md
```

Der **Dateiname** bleibt. Der **Inhalt** der drei `QUELLE.md` wird übersetzt.

## 1.5 Funktionsnamen

⚠️ Die ursprüngliche Liste nannte nur `finde_wurzel` und `ols_geclustert`.
Tatsächlich im Projekt definiert:

```
In Lennys Dateien:    finde_wurzel   bereinige   hole_jahr   zeichne
                      interaktiv     permutationstest   anteil_zwischen   main
In Subrajs Dateien:   ols_geclustert
```

`finde_wurzel` steht zusätzlich als Name in der Prosa von `README.md` und in den
Dokumentationen. Dort bleibt er in Rückwärtsstrichen stehen, der Satz drumherum
wird englisch.

## 1.6 Die SPARQL-Abfrage

Die Abfrage selbst bleibt unverändert, inklusive aller 20 Variablen. Sie steht in
`query.txt` und in `scripts/strompreise_holen.py`:

```
?abgaben   ?c        ?energie    ?gemeinde      ?gemeinde_nr   ?jahr
?kategorie ?m        ?messtarif  ?messtarif_chf_jahr
?netzbetreiber   ?netzbetreiber_id   ?netznutzung   ?netzzuschlag
?obs       ?op       ?p          ?period        ?produkt       ?total
```

## 1.7 Datenwerte

Werte **in** den Daten sind keine Prosa. Wer sie übersetzt, bricht jeden `groupby`
und jeden Join.

| Spalte | Werte | |
|---|---|---|
| `sprachregion` | `Deutsch` · `Französisch` · `Italienisch` · `Rätoromanisch` | ⚠️ Das sind deutsche Wörter **als Daten**. Nicht anfassen. |
| `gemeinde` | 2087 Gemeindenamen | bleiben |
| `netzbetreiber` | 485 Betreibernamen | bleiben |
| `kanton` | 26 Kürzel, `AG` bis `ZH` | bleiben |
| `gemeindetyp_9` | Zahlencodes `11`–`33`, keine Texte | bleiben |

Wenn die Werte der Sprachregion in einer **Grafik** erscheinen sollen, nicht die
Daten ändern, sondern beim Zeichnen übersetzen, zum Beispiel über ein Dictionary
`{"Deutsch": "German", ...}` direkt vor dem Plot.

---

# 2. Offizielle Namen der Quellen

Hier habe ich auf den englischen Seiten der Behörden selbst nachgeschaut, nicht
übersetzt.

| Deutsch | Englisch | Status | Quelle |
|---|---|---|---|
| Eidgenössische Elektrizitätskommission ElCom | **Federal Electricity Commission ElCom** | ✅ | `elcom.admin.ch/elcom/en/home.html`, Logo und Titel. Im Fliesstext derselben Seite auch «Swiss Federal Electricity Commission (ElCom)». Kürzel **ElCom** bleibt. |
| Bundesamt für Statistik BFS | **Federal Statistical Office**, Kürzel **FSO** | ✅ | `bfs.admin.ch/en/`. ⚠️ «BFS» kommt auf der englischen Seite nicht vor. Im englischen Text also **FSO**, nicht BFS. |
| Bundesamt für Landestopografie swisstopo | **Federal Office of Topography swisstopo** | ✅ | `swisstopo.admin.ch/en`. Klein geschrieben, auch am Satzanfang. |
| Regionalporträts | **Regional portraits** | ✅ | Produkttitel «Regional portraits 2021: communes», `statistik.admin.ch/en/asset/15864458` |
| Raumgliederungen (der Schweiz) | **Spatial divisions** | ✅ | Seitentitel der englischen BFS-Seite `.../regional-analyses/spatial-divisions.html` |
| LINDAS | *ungeprüft* | ⚠️ | `lindas.admin.ch` weist die Verbindung ab (`ECONNREFUSED`). Ich habe **keine** geprüfte englische Auflösung. Vorläufig: «LINDAS, the Linked Data Service of the Swiss federal administration» 🟡 — wer es belegen kann, trägt es ein. |
| swissBOUNDARIES3D | **swissBOUNDARIES3D** | ✅ | Produktname, schon englisch |

## 2.1 Grundregel: eigene Prosa gegen zitierter Titel

Behörden benennen ihre Produkte anders, als man im Fliesstext schreiben würde.
Darum gilt im ganzen Projekt **eine** Regel, nicht pro Begriff eine Ausnahme:

> **In unserer eigenen Prosa verwenden wir den verständlicheren Begriff.
> Wo wir einen offiziellen Titel zitieren, zitieren wir ihn wörtlich.**

Zwei Fälle, in denen das auseinandergeht:

| | unsere Prosa | wörtlich zitierter Titel |
|---|---|---|
| Gemeinde | **municipality** | «Regional portraits 2021: **communes**» |
| Sprachregion | **language region** | «**Language areas** 2020» |

Ein zitierter Titel steht in Anführungszeichen und bleibt unangetastet. Alles
andere ist unsere Prosa und folgt diesem Glossar. Die Regel gilt auch für
künftige Begriffe, die uns noch auffallen — dann nicht neu diskutieren, sondern
hier anwenden.

⚠️ **Die BFS-Website steckt in einer Migration.** Alle englischen Produktseiten
leiten derzeit über `statistik.admin.ch` auf eine Sprachauswahl um oder antworten
mit 404. Die zwei ✅ oben stammen aus indexierten Seitentiteln, nicht aus einer
gelesenen Seite. Das ist gut, aber eine Stufe schwächer als die anderen drei.

---

# 3. Grundstock

Von Lenny vorgegeben, unverändert übernommen. ✅ heisst hier «von uns verbindlich
gesetzt», nicht «von der Behörde belegt» — ausser wo eine Quelle dabeisteht.

| Deutsch | Englisch | Status |
|---|---|---|
| Netzbetreiber | grid operator | ✅ gesetzt |
| Gemeinde | municipality | ✅ gesetzt, siehe Hinweis in Abschnitt 2 |
| Versorgungsgebiet | supply area | ✅ gesetzt |
| Grundversorgung | basic supply | ⚠️ siehe unten |
| Strompreis | electricity price | ✅ gesetzt |
| Energie | energy | ✅ gesetzt |
| Netznutzung | grid usage | ⚠️ siehe unten |
| Abgaben | levies | ⚠️ siehe unten |
| Netzzuschlag | grid surcharge | ⚠️ siehe unten |
| Messtarif | metering tariff | ⚠️ siehe unten |
| Rp./kWh | cts./kWh | ✅ gesetzt |
| Sprachregion | language region | ✅ entschieden, siehe Abschnitt 2.1 |
| Gemeindetypologie | municipality typology | 🟡 |
| Einwohner | population | ✅ gesetzt |
| Dichte | population density | ✅ gesetzt |
| Fläche | area | ✅ gesetzt |
| Anteil 65+ | share aged 65+ | ✅ gesetzt |
| Beschäftigte | jobs | ✅ gesetzt |
| Gemeindefusion | municipal merger | ✅ gesetzt |
| Varianzzerlegung | variance decomposition | ✅ gesetzt |
| Kreuzvalidierung | cross-validation | ✅ gesetzt |
| cluster-robuste Standardfehler | cluster-robust standard errors | ✅ gesetzt |

**⚠️ Ehrlich dazugesagt: die fünf Preisbestandteile sind nicht offiziell belegt.**
ElCom hat keine englische Version seiner Strompreis-Seite. Die englische
ElCom-Startseite verlinkt auf `strompreis.elcom.admin.ch`, und diese Seite ist
ausschliesslich deutsch. Dasselbe gilt für «Grundversorgung». Die Übersetzungen
oben sind also **unsere Setzung**, sprachlich einwandfrei, aber nicht zitierfähig
als ElCom-Terminologie. Wo wir in der Dokumentation eine ElCom-Quelle angeben,
schreiben wir den deutschen Originalbegriff in Klammern dahinter, zum Beispiel:
*grid surcharge (German: «Netzzuschlag»)*. Einmal pro Dokument beim ersten
Vorkommen genügt.

---

# 4. Ergänzte Begriffe aus Lennys Dateien

Maschinell gezählt über alle sieben Dateien: Markdown-Zellen, Kommentare,
`print()`-Texte und Grafikbeschriftungen. Aufgenommen ist, was **mehr als zweimal**
vorkommt und ein Fachbegriff ist. Allgemeinsprache und Eigennamen sind
herausgefiltert. Alles hier ist 🟡 **Vorschlag**, sofern nicht anders markiert.

## 4.1 Strommarkt und Tarife

| Deutsch | n | Vorschlag |
|---|---|---|
| Bestandteile (des Preises) | 11 | price components |
| Gesamtpreis | 6 | total price |
| Messkosten | 9 | metering costs |
| Preisniveau | 6 | price level |
| Preisstreuung | 7 | price dispersion |
| Preisdaten | 7 | price data |
| Betreiber (Kurzform) | 16 | operator |
| Tarifjahr | 8 | tariff year |
| Rappen | 25 | centimes |
| Verbrauchsprofil H4 | – | consumption profile H4 ✅ *H4 ist ein Code, bleibt* |

## 4.2 Gemeinden, Raum und Geodaten

| Deutsch | n | Vorschlag |
|---|---|---|
| Gemeindenummer | 10 | municipality number |
| Gemeindeverzeichnis | – | register of municipalities |
| Gemeindemutationen | – | municipality changes |
| Gebietsstand | 7 | territorial status as at *(DD.MM.YYYY)* ⚠️ nicht belegt |
| Gemeindegrenzen | 6 | municipal boundaries |
| Kantonsgrenzen | 6 | cantonal boundaries |
| Gemeindemerkmale | 8 | municipal characteristics |
| Fusionsgemeinden | 11 | merged municipalities |
| Fusion | 8 | merger |
| Einwohnerzahlen | 6 | population figures |
| Kanton · Kantone | – | canton · cantons |
| Sprachregionen *(Plural)* | 9 | siehe Abschnitt 6 |

## 4.3 Statistik und Methode

| Deutsch | n | Vorschlag |
|---|---|---|
| Mittelwert | 12 | mean |
| Median | 16 | median |
| Spannweite | – | range |
| Permutationstest | 7 | permutation test |
| Regression | 8 | regression |
| Korrelation | 6 | correlation |
| Rangkorrelation | – | rank correlation |
| Verzerrung | 6 | bias |
| Trefferquote | 6 | match rate |
| Kennzahl · Kennzahlen | 19 | key figure · key figures |
| Fehlende Werte | 8 | missing values |
| Ganzzahl | 8 | integer |
| Breitformat · Langformat | 6 | wide format · long format |
| Annahme | 7 | assumption |
| Einschränkung | 7 | limitation |
| Gruppen · gruppiert | 13 | groups · grouped |
| Streuung | – | dispersion |

## 4.4 Technik und Repo

| Deutsch | n | Vorschlag |
|---|---|---|
| Repo-Wurzel | 9 | repository root |
| Endpunkt | 6 | endpoint |
| Abfrage | 7 | query |
| Klon | 7 | clone |
| virtuelle Umgebung | 12 | virtual environment |
| Umgebungsvariable | 6 | environment variable |
| Ausgabe · Ausgaben | 12 | output |
| Skript | 7 | script |
| Zelle | – | cell |
| Herkunftsnachweis | – | provenance record |

## 4.5 Projekt und Abgabe

| Deutsch | n | Vorschlag |
|---|---|---|
| Forschungsfrage | 11 | research question |
| Unterfrage | 10 | sub-question |
| Pflichtanforderung | 30 | mandatory requirement |
| Bonuspunkt | 27 | bonus point |
| Punkteliste | – | requirements checklist |
| Abschnitt | 37 | section |
| Folie · Folien | 22 | slide · slides |
| Kernaussage | 11 | key message |
| Aufgabenstellung | 6 | assignment |
| Anforderung | 7 | requirement |
| Beleg | 10 | evidence |
| Abgleich | 10 | cross-check |
| Prüfung | 12 | check |
| Behauptung | 6 | claim |
| Kriterium | 8 | criterion |
| Primärquelle | 6 | primary source |
| Datenquelle | 6 | data source |

---

# 5. Zwei Regeln für den Stil

**Zahlen.** Englisch schreibt den Dezimalpunkt und das Tausender-Komma:
deutsch `20.86` bleibt `20.86`, aber deutsch `2'087` wird `2,087`.
In **Code und Daten** nichts ändern.

**Datum.** Deutsch `24.11.2026` wird englisch `24 November 2026` im Text und
`2026-11-24` in Dateinamen und Tabellen. Keine Form wie `11/24/2026`, die liest in
Europa jeder falsch.

---

# 6. Offene Fragen, bitte vor dem Übersetzen klären

**✅ 1. Sprachregion heisst «language region». Entschieden am 24.11. von Lenny.**
Das BFS verwendet in seinen englischen Verzeichnissen «Language areas», und die
Quelldaten heissen auf Deutsch «Sprachgebiet», nicht «Sprachregion». Wir schreiben
trotzdem *language region*: im Fliesstext verständlicher, und unsere Spalte heisst
ohnehin `sprachregion`. Das ist **kein Sonderfall**, sondern die Grundregel aus
Abschnitt 2.1. Wer einen BFS-Produkttitel zitiert, schreibt dort weiterhin
«Language areas».

**✅ 2. Die geteilten Dateien sind verteilt. Festgelegt am 24.11.**
Drei Dateien gehören niemandem allein. Damit es kurz vor der Frist keinen
Merge-Konflikt in der wichtigsten Datei des Repos gibt, übersetzt jede geteilte
Datei **genau eine Person ganz**.

| Datei | wer hat daran gearbeitet | **wer übersetzt** |
|---|---|---|
| `README.md` | alle drei, die PostgreSQL- und macOS-Teile sind Metehans | **Lenny**, die ganze Datei |
| `punkteliste.md` | alle drei | **Lenny**, die ganze Datei |
| `requirements.txt` | alle drei | ⚠️ **noch offen**, nur Kommentare. Wer es macht, sagt es vorher in der Gruppe. |
| `glossar.md` | diese Datei | bleibt deutsch, ist Arbeitsmittel |

**Metehan und Subraj: `README.md` und `punkteliste.md` bitte nicht anfassen.**
Wenn euch dort beim Übersetzen eurer eigenen Dateien etwas auffällt, sagt es
Lenny, statt es selber zu ändern.

**⚠️ 3. Müssen Commit-Nachrichten englisch werden?**
Die bisherige Historie ist deutsch. Nachträglich umschreiben wäre ein
`rebase` über die ganze Historie und damit gefährlich. Vorschlag: Historie bleibt,
**neue** Commits ab jetzt englisch.

**⚠️ 4. Bleiben unsere Vornamen in den Dateinamen?**
`01_daten_bfs_lenny.ipynb`, `03_analyse_subraj.ipynb` und so weiter. Umbenennen
bricht alle Pfade und alle Querverweise in der Dokumentation. Vorschlag:
**Dateinamen bleiben**, siehe Abschnitt 1.4.
