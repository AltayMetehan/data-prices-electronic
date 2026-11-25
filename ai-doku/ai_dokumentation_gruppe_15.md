# AI-Dokumentation Gruppe 15

Data Analytics, ZHAW, HS2026 · Subraj Singh, Lenny Frei, Metehan Altay · Pflichtanforderung 8

Stand: 21. November 2026. Gebündelt aus den fünf Einzeldokumenten im Ordner `ai-doku/`.
Dort stehen die vollständigen Protokolle mit allen Einzelheiten.

> Moodle verlangt die AI-Reflexion an drei Stellen: als Dokumentation (Pflicht 8), als
> Abschnitt «Reflection on AI usage» im Präsentations-PDF und in Folien und Video
> (Kriterium 6 der Videobewertung). Dieses Dokument ist die Grundlage für alle drei.
> Der Einsatz von AI für die Präsentation selbst fehlt noch (Abschnitt 6).

---

## Kurzfassung

Alle drei haben Claude von Anthropic eingesetzt, für Datenbeschaffung, Datenbanken, Join,
Karten, Analyse, Modell und Dokumentation. Die AI hat Arbeit ermöglicht, die im Unterricht
nicht vorkam (SPARQL, PostgreSQL, geclusterte Standardfehler), und Widersprüche in langen
Dokumenten zuverlässig gefunden.

Ihr grösster Nachteil: Fehler sahen plausibel aus. Code lief ohne Fehlermeldung und lieferte
falsche Zahlen, und Behauptungen über Daten waren konkret formuliert, ohne geprüft zu sein.
Gefunden wurden diese Fehler fast immer erst durch Nachrechnen an den Rohdaten oder durch
eine zweite, unabhängige Rechnung, nie durch die AI allein.

---

## 1. Verwendete Werkzeuge

| Werkzeug | Wer | Wofür |
|---|---|---|
| Claude (Anthropic), Modell Claude Opus 5.5, in der Claude-App mit Websuche und Zugriff auf den eigenen Browser | Metehan | SPARQL-Abfrage und Beschaffungsskript, SQLite-Datenbank, PostgreSQL |
| Claude Code (Claude Opus 5) in VS Code | Lenny | Umgebung einrichten, Daten prüfen, Join, Gemeindefusionen, Karten, Projektanleitung und Punkteliste |
| Claude Code in einer Cloud-Sitzung | Lenny | ein Zwischenschritt am 27./28.10.2026; das Ergebnis ging verloren (Fall L1) |
| eine weitere, externe AI-Prüfung | Lenny | Durchsicht des Projekts; lieferte den Befund zur Netzbetreiberebene |
| Claude (Anthropic), in der Claude-App mit einer Cloud-Arbeitsumgebung | Subraj | Aufgabenstellung und Themenwahl, Forschungsfrage, EDA und Tests, Regression und k-means, Prüfung des ganzen Repos |
| Claude Code (Claude Opus 5.5) in VS Code, mit der Folienvorlage «Slides» auf claude.ai | Metehan | Konzeptpräsentation: Gliederung, Foliengestaltung, Diagramme, Sprechskript (24./25.11.2026, siehe Abschnitt 6) |

---

## 2. Wofür die AI eingesetzt wurde

| Aufgabe | Wer | Was die AI gemacht hat | Wie das Ergebnis geprüft wurde |
|---|---|---|---|
| Aufgabenstellung, Themenwahl, Forschungsfrage | Subraj | Aufgabe zusammengefasst, Themen auf alle Zusatzpunkte geprüft, Hauptfrage mit fünf Unterfragen und Methoden formuliert | Abgleich mit dem Wortlaut auf Moodle |
| Projektanleitung und Punkteliste | Lenny | Anleitung auf Widersprüche geprüft (fünf gefunden), Punkteliste gegen die Moodle-Seite abgeglichen (acht Abweichungen gefunden) | Zeilenweiser Abgleich mit dem Original |
| Datenbeschaffung (Pflicht 1) | Metehan | Endpunkt gefunden, Datenmodell des ElCom-Cubes ausgelesen, SPARQL-Abfrage und Python-Skript geschrieben | Summenkontrolle über alle 143 837 Zeilen, Stichprobe von Hand |
| Join (Pflicht 2) | Lenny | BFS-Quelle vor dem Download geprüft, Regionalporträts ins Breitformat gedreht, Join über die Gemeindenummer, Fusionen über die Mutationstabelle aufgelöst | Trefferquote, Permutationstest auf Auswahlverzerrung, Vergleich mit der Gesamtschweiz |
| SQLite (Pflicht 3) | Metehan | Datenmodell mit 5 Tabellen und 2 Views entworfen, Notebook geschrieben | 0 Abweichungen gegenüber Lennys Join in allen 8 Spalten |
| Karten (Bonus 3) | Lenny | Lizenz geklärt, Abdeckung geprüft, zwei Karten als Bild und interaktiv gebaut | fertige Bilder angesehen (Fall L11) |
| PostgreSQL (Bonus 2) | Metehan | Schema übertragen, Views nachgebaut, sechs Auswertungen mit Joins, Aggregationen und Fensterfunktionen | gleiche Zeilenzahlen und Werte wie SQLite, Abweichung höchstens 7 × 10⁻¹⁵ |
| EDA und Tests (Pflicht 4, Bonus 4) | Subraj | Notebook 03 auf den echten Daten gebaut, jeder Test auf Gemeinde- und Betreiberebene | jede Zahl im Text gegen die Ausgabe im Notebook geprüft |
| Regression, Modellgüte, k-means (Pflicht 5 bis 7, Bonus 5) | Subraj | Notebook 04, mit selbst programmierten geclusterten Standardfehlern und gruppierter Kreuzvalidierung | Koeffizienten gegen scikit-learn geprüft (identisch), Gegenprobe gegen statsmodels vorbereitet |
| Prüfung des ganzen Repos | Subraj | Rohdaten, Join und Datenbank unabhängig nachgerechnet, Kreativitätsbelege gegen die Kurs-Repos geprüft | Join exakt nachgebaut, Datenbank neu gebaut und Tabelle für Tabelle verglichen |

---

## 3. Vorteile

1. SPARQL, PostgreSQL und geclusterte Standardfehler kamen im Unterricht
   nicht vor. Die AI hat das Datenmodell des ElCom-Cubes direkt am Endpunkt ausgelesen und die
   Formel für die Standardfehler mit Kontrolle umgesetzt (Metehan, Subraj).
2. Fünf Fehler in der Projektanleitung, acht
   Abweichungen der Punkteliste von der Aufgabenstellung und vier Fehler im Projektplan hätte
   beim Durchlesen niemand gefunden. Ein Abgleich Zeile für Zeile hält eine AI besser durch als
   ein Mensch (Lenny, Subraj).
3. Die AI hat Abfragen und Code nicht nur geschrieben, sondern
   ausgeführt und Zeilenzahlen, Mediane und Summen ausgegeben. Ob die ElCom die Tarife 2027
   schon publiziert hatte, war offen; die AI hat es nachgeprüft (Metehan).
4. Die AI hat Kontrollen eingebaut: Summenkontrolle, Fremdschlüssel, Vergleich zweier Datenbanken,
   `assert`-Prüfungen beim Verbinden der Daten. Sie laufen bei jedem Durchgang mit (alle).
5. Die AI hat 36 nicht geprüfte BFS-Bezeichnungen als
   «abgeleitet» gekennzeichnet, nicht reproduzierbare Zahlen einer anderen AI als solche benannt
   und gesagt, was mit einem Ersatzmodul statt dem echten Treiber getestet wurde (Metehan, Lenny).
6. Die Preise werden pro Netzbetreiber gesetzt, nicht pro
   Gemeinde. Daraus folgten die geclusterten Standardfehler, die Rechnungen auf Betreiberebene
   und die gruppierte Kreuzvalidierung. Ohne sie hätten wir die Modellgüte deutlich überschätzt
   (Lenny, Subraj).
7. Ein 21 546 Pixel hoher Screenshot der Moodle-Seite und
   ein PDF mit 1795 Seiten wurden zerlegt und durchsucht (Lenny).

---

## 4. Nachteile

1. Die erste SPARQL-Abfrage lief fehlerfrei und lieferte
   sinnvolle Zahlen, aber ohne Messtarif. Auch falsche Vermutungen kamen überzeugend formuliert
   (alle).
2. Die AI hat Datenquellen beschrieben, ohne sie zu öffnen, und
   Belege angegeben, ohne sie aufzurufen. Eine Markierung «Geklärt am …» erzeugte Vertrauen,
   obwohl der Link tot war (Lenny).
3. Auf eine knappe Anfrage wählte die AI selbst eine Gemeinde, statt nach
   Jahren und Umfang zu fragen. In einem anderen Fall wollte sie mit erfundenen Testdaten
   beginnen, bevor die echten vorlagen (Metehan, Subraj).
4. Die AI hat ungefragt Auswertungen gemacht, etwa Korrelationen in der
   PostgreSQL-Datenbank. Ungetestet verleiten solche Zahlen zu vorschnellen Schlüssen (Metehan).
5. Die Cloud-Umgebungen der AI konnten Pakete nicht installieren
   (Jupyter, statsmodels, psycopg2) oder Schnittstellen nicht erreichen (LINDAS). Was dort nicht
   lief, war nicht getestet (alle).
6. Jede neue Sitzung beginnt ohne Vorwissen. Entscheide
   müssen deshalb schriftlich im Repo stehen (Lenny).

---

## 5. Wo etwas mit AI nicht funktioniert hat

Die wichtigsten Fälle aus allen drei Teilen. Die L-Nummern entsprechen den Fällen in Lennys
Dokument. Die M- und S-Nummern sind für diese Übersicht vergeben; die Einzelheiten stehen in
den Dokumenten von Metehan und Subraj.

| Nr | Datum | Was nicht funktioniert hat | Wie es auffiel | Folge |
|---|---|---|---|---|
| M1 | 26./27.10. | Die erste SPARQL-Abfrage liess den Messtarif weg. 2027 fehlten im Median 1.74 Rp./kWh. Die AI bemerkte es nicht und tippte auf Metehans Hinweis zuerst auf die Fixkosten | Metehan beim Nachrechnen | Abfrage korrigiert, Summenkontrolle ins Skript eingebaut |
| L7 | 27.10. bis 01.11. | Die AI legte fest, den Messtarif beim Zeitvergleich wegzulassen. Die Regel stand in der Anleitung und in drei Spalten der verbundenen Tabelle, die an zwei Teammitglieder gehen sollte. 2027 wäre um 1.67 Rp. zu billig gewesen | Widerspruch zwischen Anleitung und Kommentar im Skript, geklärt an der Primärquelle der ElCom | Spalten entfernt, Zahlen korrigiert |
| L1 | 27./28.10. | Eine Cloud-Sitzung konnte nicht pushen; vier Commits und acht Dateien gingen verloren | Suche auf dem eigenen Rechner | rund zwei Stunden Arbeit neu gemacht |
| L2 | 30.10. | Eine externe AI lieferte Zahlen zu den Netzbetreibern, die sich nicht nachrechnen liessen; sie hingen an der zufälligen Zeilenreihenfolge | eine zweite AI konnte sie nicht reproduzieren | dokumentierte Regel: Betreiber mit der kleinsten ID |
| L6 | 27.10. bis 30.10. | Die AI behauptete, im Kurs-Repo lägen brauchbare Gemeindegrenzen. Die Datei deckt nur den Kanton Zürich ab | Blick in die Datei | Grenzen von swisstopo geholt |
| L9 | 27.10. bis 07.11. | Die Anleitung beschrieb die BFS-Daten mit Kanton und Sprachregion, die darin nicht enthalten sind. Unterfrage 1 und die ANOVA wären nicht rechenbar gewesen | Vorbereitung der Karte, eine Woche später | dritte Datenquelle eingebaut |
| L8 | 07.11. | Metehans AI sortierte die Dateien in Unterordner, ohne die Pfade nachzuziehen. Beide Notebooks brachen ab, die eingecheckten Ausgaben sahen aber korrekt aus | Lauf auf einem frischen Klon | Pfade von der Repo-Wurzel abgeleitet, Regel im README |
| L11 | 07.11. | Die Farbskala der Veränderungskarte war nach Lehrbuch gewählt und versteckte genau die Gemeinden, um die es ging | Ansehen des fertigen Bildes | Skala mit ungleich langen Ästen |
| L12 | 08.11. | Ein Beleg in der Anleitung führte auf eine tote Adresse, eine Aussage («etwas teurer») hielt einem Test nicht stand | Audit gegen Primärquellen und Rohdaten | Belege ersetzt, Aussage abgeschwächt |
| M2 | 02.11. | 36 von 41 BFS-Bezeichnungen hat die AI nur aus Plausibilität erschlossen | von der AI selbst markiert | nur die 5 geprüften Kennzahlen verwendet |
| M3 | 02.11., 17.11. und 22.11. | Jupyter und psycopg2 liessen sich in der ursprünglichen Cloud-Umgebung nicht installieren. Das PostgreSQL-Notebook lief zuerst mit einem Ersatzmodul auf einem Testserver | von der AI selbst benannt; am 22.11. lokale PostgreSQL-17.12-/psycopg2-Verbindung geprüft | echtes psycopg2 eingebunden, interaktive Passwortabfrage entfernt, Repo-Pfad ergänzt |
| S1 | 10.10. | Die erste Themenliste prüfte nicht, ob die Daten per Scraping oder API selbst erhoben würden; bei mehreren Themen wäre ein fertiger Datensatz die Hauptquelle gewesen | Nachfrage von Subraj | neue Themen mit eigener Datenerhebung |
| S2 | 08.11. und 17.11. | statsmodels liess sich nicht installieren; die geclusterten Standardfehler wurden selbst programmiert | Umgebung | Gegenprobe gegen statsmodels im Notebook vorbereitet |
| S3 | 17.11. | In der eigenen Interpretation standen drei Aussagen, die stärker waren als die Zahlen | Gegenlesen jeder Zahl gegen die Ausgabe | korrigiert |
| S4 | 21.11. | In Notebook 03 fehlte die Korrelation mit der Grösse des Netzbetreibers, obwohl Unterfrage 2 sie ausdrücklich nennt | Abgleich mit dem Projektplan | als Abschnitt 8.6 nachgetragen; stärkster Zusammenhang im Projekt |
| S5 | 21.11. | Sieben Gemeinden haben 2021 bei einem von zwei Netzbetreibern einen leeren Tarif von 0.00 Rp. Datenbank und Join bilden den Mittelwert, ihr Preis 2021 ist deshalb halbiert. Alle bisherigen Kontrollen liefen durch, weil auch ein leerer Tarif die Summenkontrolle besteht (0 = 0 + 0 + …) | unabhängiges Nachrechnen der Rohdaten | Bereinigung in Notebook 01 und 02 offen; nachgerechnet kippt keine Aussage, ein Befund wird stärker |
| S6 | 21.11. | Die Punkteliste beanspruchte die Karte in Python als kreativ. Die Übungen zu Woche 5 machen genau das | Abgleich mit den Kurs-Repos | Beleg gestrichen |

---

## 6. AI-Einsatz für die Präsentation

Pflicht 8 verlangt den AI-Einsatz «for creating the code and the presentation». Die Folien
entstehen ab dem 24. November 2026. Festzuhalten ist dann, wofür AI bei Gliederung, Texten,
Grafiken und Video eingesetzt wurde, was übernommen wurde und was verworfen oder korrigiert
werden musste. Dieser Abschnitt wird danach ergänzt.

### 6.1 Konzeptpräsentation (Metehan, 24./25.11.2026)

**Werkzeug.** Claude Code mit dem Modell Claude Opus 5.5 in VS Code, im Projektordner. Die
Folien entstanden mit der Folienvorlage «Slides» auf claude.ai, als privates Deck, das im
Browser angezeigt und als PDF exportiert wird.

**Eingaben.** Ein Bildschirmfoto der Bewertungskriterien aus Moodle (acht Kriterien, 10 Minuten),
dazu die Dateien aus dem Repo: `README.md`, `folien_entwurf_lenny.md`, `punkteliste.md`,
`dokumentation_integration_lenny.md` und das Notebook `scripts/03_analyse_subraj.ipynb`. Die
Zahlen auf den Folien stammen aus diesen Dateien, die Grafiken zu Rangfolge, Heatmap, Kantonen,
Boxplots und die Karte sind die Bilder aus Subrajs Notebook und Lennys Karte.

**Ablauf in sechs Runden.**

| Runde | Auftrag | Ergebnis |
|---|---|---|
| 1 | Folien nach den Kriterien, «stichwortartig und schöner Style» | Gliederung entlang der acht Kriterien, eigenes Farbschema |
| 2 | «sieht sehr mager aus», «kaum Sätze» | Aufzählungen durch Diagramme, Kennzahlen und Schlagworte ersetzt; Sätze in die Sprechernotizen verschoben |
| 3 | übersichtlicher, Backup-Folien, Grafiken aus Subrajs EDA | Navigationsleiste, je Folie eine Grafik mit drei Kernaussagen, zwei neue EDA-Folien, acht Backup-Folien |
| 4 | Backup-Folien wieder heraus, Wichtigstes in die Hauptfolien | 14 Folien; Kernpunkte (H4, Ausfall, Datenjahre, Messtarif) auf «Struktur» und «Hintergrund» verdichtet |
| 5 | Sprechskript in die Notizen | ausformulierter Text pro Folie mit Sprecher, Zeit und Hinweisen für Rückfragen |
| 6 | Rückmeldung aus dem Team zur Rahmung | Navigationsleiste «Erwartete Resultate», ein Satz im Skript, dass die Rechnungen erste Bestätigungen sind |

**Übernommen.** Aufbau nach den Bewertungskriterien, das Layout «eine Grafik, drei Kernaussagen»,
die selbst gezeichneten Diagramme (Preisbestandteile, R² nach Validierungsart, Ausfalltrichter),
das Sprechskript als Vorlage, die wir noch in eigene Worte bringen.

**Verworfen.** Die erste Fassung mit vielen ganzen Sätzen auf den Folien (zu textlastig). Die
acht Backup-Folien, weil sie das Deck aufblähten; nur ihre Kernaussagen blieben.

**Wo es nicht funktioniert hat.**

| Nr | Was nicht funktioniert hat | Wie es auffiel | Folge |
|---|---|---|---|
| P1 | Die Datenfolie behauptete «202 von 2201 Gemeinden fehlen». 88 dieser 202 sind aber Teil der 2087, ihnen fehlt nur die Beschäftigtenzahl | Abgleich mit der Integrationsdoku (§7) bei der Überarbeitung | als Trichter 2201 → 2087 → 1999 neu dargestellt |
| P2 | Lennys Folienentwurf verortete die günstiger gewordenen Gemeinden um ZH/ZG/AG. Auf der Karte liegen sie vor allem im Raum Bern/Jura. Die AI hatte den Satz zuerst übernommen | Vergleich des Textes mit dem Kartenbild | Aussage auf der Folie neutral formuliert |
| P3 | Die Beschreibung des Referenzhaushalts H4 (5-Zimmer-Wohnung, Elektroherd, Tumbler) stammte aus dem Allgemeinwissen der AI, nicht aus unseren Quellen | von der AI selbst markiert | nur «4500 kWh pro Jahr» übernommen; Rest an der ElCom zu prüfen |
| P4 | Mehrere Folien waren zu voll und liefen über den Rand. Die AI hat das Layout nicht als Bild angesehen, sondern die Höhen nur nachgerechnet | Überarbeitung, Durchklicken durch das Team | Inhalte gekürzt; Sichtprüfung bleibt beim Team |
| P5 | Die AI zeigte die Rechnungen als fertige Resultate, ohne die Modulbeschreibung zu prüfen: Die Live-Präsentation «does not cover the finished project work or final results» | Rückmeldung aus dem Team | «Erwartete Resultate» in der Navigationsleiste, Hinweis im Skript, Stand auf der Modellfolie |
| P6 | Die Zuordnung der Sprachregionen-Mittelwerte (27.2 / 27.5 / 26.8) zu Deutschschweiz, Romandie und Tessin folgte nur der Reihenfolge im Notebook-Text | von der AI selbst markiert | von Subraj zu bestätigen; Folie entfernt, Zahlen nur noch in der Spickliste |

**Gelernt.** Auch bei Folien gilt Abschnitt 7: Jede Zahl auf einer Folie braucht eine Quelle im
Repo (P1, P3), ein Text über eine Grafik muss gegen die Grafik geprüft werden (P2), und eine
Folie muss man als fertiges Bild ansehen (P4). Die AI optimiert auf den Auftrag, den sie bekommt;
die Rahmenbedingungen der Modulbeschreibung musste das Team selbst einbringen (P5).

---

## 7. Was wir daraus gelernt haben

1. Code ohne Fehlermeldung liefert nicht automatisch richtige
   Zahlen (M1, L7, S5). Eine eingebaute Kontrolle findet viele Fehler sofort, aber nicht alle:
   Die Summenkontrolle bestand auch leere Tarife.
2. Die stärksten Tests waren zwei Wege zum selben
   Ergebnis: Datenbank gegen Join, PostgreSQL gegen SQLite, eine zweite AI gegen die erste
   (L2, M2, S5).
3. Eine Beschreibung von Daten oder ein Beleg, den niemand
   geöffnet hat, ist eine Vermutung (L6, L9, L12, S6).
4. Eine Grafik muss man als fertiges Bild ansehen, ein Notebook auf einem
   frischen Klon laufen lassen. Eingecheckte Ausgaben sind ein Foto von gestern (L8, L11).
5. Mit Projektplan und Dateien von Anfang an musste die AI
   nichts annehmen (M1, M2).
6. Was nicht gepusht ist, existiert nicht (L1).
7. Jede Methode in den Notebooks müssen wir im Video selbst
   erklären können.

---

## 8. Vorschlag für Folien und Video

Kriterium 6 verlangt die Reflexion in Folien und Video. Pro Person ein Beispiel, das zeigt, wo
AI nicht funktioniert hat und wie der Fehler gefunden wurde:

| Wer | Beispiel | Warum gut fürs Video |
|---|---|---|
| Metehan | M1, der fehlende Messtarif | zeigt plausible, aber falsche Daten und die Summenkontrolle als Gegenmittel |
| Lenny | L7, die falsche Annahme in der verbundenen Tabelle | zeigt, wie sich ein Fehler über Dokument und Daten ausbreitet und an der Primärquelle geklärt wird |
| Subraj | S5, die leeren Tarife, die alle Kontrollen bestanden | zeigt, dass auch eine gute Kontrolle blinde Flecken hat und erst eine unabhängige Rechnung hilft |

---

## Einzeldokumente

- `ai-doku/AI-Dokumentation_Datenbeschaffung_Metehan.md`
- `ai-doku/AI-Dokumentation_SQLite_Metehan.md`
- `ai-doku/AI-Dokumentation_PostgreSQL_Metehan.md`
- `ai-doku/ai_dokumentation_lenny.md`
- `ai-doku/ai_dokumentation_subraj.md`
