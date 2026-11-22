# AI-Dokumentation – Subraj

Data Analytics, ZHAW, HS2026. Teil von Pflichtanforderung 8.

> Entwurf, von Claude aus dem Verlauf der Arbeitssitzungen zusammengestellt. Subraj prüft
> und ergänzt ihn um eigene Eindrücke, bevor er in die Bündelung geht. Die AI-Reflexion
> ist zusätzlich in den Folien und im Video verlangt (Kriterium 6 der Videobewertung).

---

## Verwendete Werkzeuge

| Werkzeug | Wofür |
|---|---|
| Claude (Anthropic), in der Claude-App mit einer Cloud-Arbeitsumgebung | Aufgabenstellung verstehen, Themenwahl, Forschungsfrage, Prüfung des Projektplans, Code und Interpretation der Notebooks 03 und 04 |

---

## Sitzungsprotokoll

### 10. Oktober 2026 – Aufgabenstellung und Themenwahl

- Die AI hat die Moodle-Aufgabenstellung zusammengefasst und auf drei offene Punkte
  hingewiesen: fehlender Abgabetermin für das Schlussprojekt, unklare Frist für das
  Konzept-PDF und das Verhältnis zwischen SQLite (Pflicht) und PostgreSQL (Bonus).
- Sie hat mehrere Themen vorgeschlagen und geprüft, welche alle sechs Zusatzpunkte
  erlauben. Darunter war das spätere Thema «Strompreise der Gemeinden».
- Bei der ersten Themenliste hat die AI nicht darauf geachtet, ob die Daten per
  Web Scraping oder Web API selbst erhoben werden. Bei mehreren Vorschlägen hätte man einen
  fertigen Datensatz heruntergeladen, was als Hauptquelle verboten ist. Erst auf
  Nachfrage hat sie das als Risiko benannt und neue Themen vorgeschlagen.

### 25. Oktober 2026 – Forschungsfrage und Projektplan

- Die AI hat eine Hauptfrage mit fünf Unterfragen formuliert und jeder Unterfrage eine
  Methode zugeordnet. Der zeitliche Vergleich (2021, 2024, 2027) macht die Frage zu mehr
  als einer reinen Vorhersage, wie es Pflicht 5 verlangt.
- Beim Gegenlesen des Projektplans fand sie vier Fehler, unter anderem:
  - eine falsche Aussage zur Zahl der Netzbetreiber
  - einen t-Test, der für Bonus 4 nicht zählt
  - die Gemeindefusionen, die einen Join über mehrere Jahre verfälschen
- Die AI wollte das EDA-Notebook sofort mit erfundenen Testdaten beginnen. Das habe ich
  gestoppt, weil die echten Daten von Metehan und Lenny noch fehlten.

### 8. November 2026 – Notebook 03: EDA und Tests

- Die AI hat das Repo gelesen, inklusive Projektanleitung und Integrationsdokumentation,
  und das Notebook auf den echten Daten gebaut und ausgeführt.
- **Nicht funktioniert:** `pip install` ging in der Cloud-Umgebung der AI nicht. Jupyter
  und statsmodels waren nicht verfügbar. Die AI hat das Notebook deshalb mit einem
  eigenen Skript ausgeführt und die Ausgaben ins `.ipynb` geschrieben.
- **Nicht funktioniert:** Der Alexander-Govern-Test (ANOVA ohne Annahme gleicher Varianzen)
  lieferte für die Kantone `NaN`. Ursache: In Basel-Stadt und Obwalden haben alle Gemeinden
  denselben Preis. Der erste Korrekturversuch (Gruppen mit Standardabweichung über null)
  griff wegen Rundungsfehlern nicht. Erst ein Test über die Spannweite der Werte löste es.
- **Nicht funktioniert:** In zwei Grafiken überdeckten Legende und Beschriftung den Titel
  oder Datenpunkte. Aufgefallen ist das erst, als die AI die erzeugten Bilder ansah, nicht
  schon beim Schreiben des Codes.
- **Hilfreich:** Die AI hat jeden Test auf Gemeinde- und auf Betreiberebene gerechnet.
  Das hat Befunde aufgedeckt, die nur durch die grossen Netzbetreiber entstehen, zum
  Beispiel den tieferen Preis dichter Gemeinden 2021.

### 17. November 2026 – Abgleich mit dem Repo und Notebook 04

- Die AI hat den neuen Stand im Repo mit dem vom 8. November verglichen. Sie hat geprüft,
  dass Lennys Änderungen an der verbundenen Tabelle keine Werte verändern, sondern nur
  Spalten ergänzen. Ihren Hinweis auf die Datenjahre der Gemeindemerkmale (2016 bis 2019)
  hat sie in Notebook 03 übernommen.
- **Nicht funktioniert:** statsmodels war weiterhin nicht installierbar. Die AI hat die
  nach Netzbetreiber geclusterten Standardfehler deshalb selbst programmiert, mit der
  Formel im Notebook. Die Koeffizienten hat sie gegen scikit-learn geprüft (identisch).
  Die Gegenprobe der Standardfehler gegen statsmodels steht im Notebook, läuft aber
  erst auf einem Rechner, auf dem statsmodels installiert ist. **Noch offen: lokal
  ausführen und prüfen, ob die Gegenprobe durchläuft.**
- **Nicht funktioniert:** Die AI konnte nicht ins GitHub-Repo pushen, weil kein GitHub-Konto
  mit ihr verbunden war. Die Dateien wurden von Hand hochgeladen.
- **Hilfreich, aber nur durch Nachprüfen:** Beim Gegenlesen ihrer eigenen Interpretation
  fand die AI drei Aussagen, die stärker waren als die Zahlen. Die wichtigste: Sie hatte
  geschrieben, die Veränderung beim Zusammenhang zwischen Dichte und Preis halte auch auf
  Betreiberebene. Dort lag der p-Wert aber bei 0.059.
- **Hilfreich:** Die AI hat vorgeschlagen, die Kreuzvalidierung nach Netzbetreiber zu
  gruppieren statt zufällig. Mit zufälligen Folds sah das Modell gut aus (R² bis 0.29),
  mit gruppierten Folds war es schlechter als der Mittelwert. Ohne diesen Vergleich hätten
  wir die Modellgüte deutlich überschätzt.

### 21. November 2026 – Abgleich mit dem Projektplan

- **Nicht funktioniert:** Beim Abgleich mit dem Projektplan zeigte sich, dass die AI in
  Notebook 03 einen Teil von Unterfrage 2 übersehen hatte: die Korrelation mit der
  Grösse des Netzbetreibers. Im Modell (Notebook 04) war sie enthalten, als Korrelation
  mit p-Wert fehlte sie. Nachgetragen als Abschnitt 8.6. Sie ist auf Gemeindeebene der
  stärkste Zusammenhang im Projekt (rho bis 0.44). Zwei Sätze, die vorher «höchstens 0.28»
  sagten, mussten präzisiert werden.
- **Nicht funktioniert:** Im neuen Text stand zuerst, der Zusammenhang mit dem Preis 2024
  verfehle die Bonferroni-Schwelle. Die AI hatte mit der Schwelle aus Abschnitt 8.5 (25 Tests)
  statt der aus 8.6 (5 Tests) gerechnet. Beim Gegenlesen korrigiert.
- **Nicht funktioniert:** Der Push ins Gruppen-Repo scheiterte zweimal, zuerst an fehlenden
  Schreibrechten, dann an der fehlenden Claude-App für GitHub auf dem Repo.

---

## Was gut funktioniert hat

- Die Aufgabenstellung in konkrete Arbeitsschritte übersetzen und prüfen, welche Punkte
  ein Thema überhaupt erlaubt.
- Methodische Fallen erkennen, die im Unterricht nicht vorkamen: abhängige Beobachtungen
  innerhalb eines Netzbetreibers, Gewichtung der Gemeinden gegenüber den Betreibern,
  Kreuzvalidierung mit Gruppen.
- Code schreiben, der sofort läuft, inklusive Kontrollen mit `assert`, die Fehler beim
  Verbinden der Daten sofort anzeigen.

## Was mühsam war oder nicht funktioniert hat

- Die AI arbeitet in einer eigenen Umgebung ohne Internetzugang für Pakete. Was dort
  nicht installiert ist, kann sie nicht testen.
- Sie neigt dazu, sofort loszulegen, auch wenn die Grundlage noch fehlt (Testdaten statt
  echter Daten).
- Ihre Interpretationen klingen sicher, auch wo die Zahlen das nicht hergeben. Jede
  Aussage mit einer Zahl muss man gegen die Ausgabe im Notebook prüfen.
- Grafiken kontrolliert sie erst, wenn sie die Bilder tatsächlich ansieht.

## Was ich daraus mitnehme

AI ist ein Werkzeug und ersetzt das Verständnis nicht. Für die Präsentation muss ich
jede Methode in den Notebooks 03 und 04 selbst erklären können: warum geclusterte
Standardfehler, warum das Anstiegsmodell die Veränderung testet und warum das R² bei
gruppierter Kreuzvalidierung negativ ist.
