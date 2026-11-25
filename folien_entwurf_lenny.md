> **Superseded.** This draft was replaced by the finished slide deck in
> `präsentation_konzept/`. It is kept in German as a record of the working stage
> and is deliberately not translated.

# Folienentwurf, Konzept-Präsentation

**Noch kein Foliendeck. Eine Diskussionsgrundlage für den Call am Dienstag.**

Data Analytics, ZHAW, HS2026 · Gruppe Frei / Metehan / Sub Raj
Entwurf: Lenny, 22. November 2026 · Präsentation: 8. Dezember, 10 Minuten, alle drei reden

---

## Worauf es ankommt

Bewertet werden **acht Kriterien**, jedes einzeln mit einer Note von 1 bis 6, der
Durchschnitt zählt. Vier davon haben nichts mit unseren Daten zu tun und sind reine
Vorbereitungsarbeit:

| Nr | Kriterium | Wo im Entwurf |
|---|---|---|
| 1 | Struktur und Gliederung | Folie 2, und dass wir die Reihenfolge einhalten |
| 2 | Hintergrund und Problem | Folie 3 |
| 3 | Ziel und Forschungsfrage | Folie 4 |
| 4 | Daten | Folien 5 und 6 |
| 5 | Methoden | Folien 7 und 8 |
| 6 | Erwartete Resultate | Folien 9 und 10 |
| 7 | Sprache, frei gesprochen | kein Ablesen, Stichworte statt Sätze auf den Folien |
| 8 | Qualität der Folien | wenig Text, eine Aussage pro Folie, lesbare Grafiken |

**Zeitbudget:** 10 Minuten für die Gruppe, also rund 3:20 pro Person. Elf Folien sind
bei diesem Tempo etwa 50 Sekunden pro Folie. Lieber zehn gute als vierzehn gehetzte.

---

## Der rote Faden, in einem Satz

> Wir wollten wissen, welche Gemeindemerkmale den Strompreis erklären – und haben
> herausgefunden, dass es keine tun. Nicht die Gemeinde bestimmt den Preis, sondern
> ihr Netzbetreiber.

**Das ist unsere Antwort, nicht unser Scheitern.** Der ganze Aufbau der Präsentation
muss das tragen. Wer am Schluss denkt «die hatten ein schlechtes Modell», hat uns
missverstanden. Wer denkt «die haben die falsche Erklärungsebene widerlegt», hat es
verstanden.

---

## Die Folien

### Folie 1 · Titel
**Kernaussage:** Wer wir sind und worum es geht.
**Darauf:** Titel «Strompreise der Schweizer Gemeinden: Was erklärt die
Unterschiede?», alle drei vollständigen Namen, Gruppe 15, Modul, Datum.
**Dazu die Repo-URL** `github.com/AltayMetehan/data-prices-electronic` – klein in der
Fusszeile. Damit ist **Bonus 6** abgedeckt, der verlangt die URL ausdrücklich «in the
project presentation».
**Spricht:** Lenny · ~20 Sekunden

### Folie 2 · Gliederung
**Kernaussage:** Wir haben einen Plan, und ihr wisst, wo wir hinwollen.
**Darauf:** Vier Blöcke – Problem und Frage, Daten, Methoden, erwartete Resultate.
Kein Inhaltsverzeichnis mit zwölf Punkten.
**Spricht:** Lenny · ~15 Sekunden
*Kriterium 1 wird hier und durch das Einhalten der Reihenfolge bewertet.*

### Folie 3 · Hintergrund und Problem
**Kernaussage:** Der Strompreis ist zwischen 2021 und 2024 um die Hälfte gestiegen,
und er ist je nach Wohnort sehr verschieden – aber niemand sagt einem, warum.
**Darauf:** Eine Zahl gross: **20.86 → 31.99 → 27.25 Rp./kWh** (H4, Mittelwert über
die 2087 Gemeinden). Dazu die Spannweite 2027: **10.6 bis 45.9 Rp./kWh** – mehr als
das Vierfache, für dasselbe Produkt.
**Warum das ein Problem ist:** Haushalte in der Grundversorgung können den Anbieter
nicht wechseln.
**Spricht:** Metehan · ~45 Sekunden

### Folie 4 · Ziel und Forschungsfrage
**Kernaussage:** Wir suchen die Erklärung für die Unterschiede, nicht nur deren
Beschreibung.
**Darauf:** Die Forschungsfrage wörtlich, dazu die fünf Unterfragen in einer Zeile
pro Stück. Hervorheben, dass der Zeitvergleich 2021 / 2024 / 2027 die Anforderung
«beyond a standard prediction task» erfüllt.
**Spricht:** Metehan · ~45 Sekunden

### Folie 5 · Daten: drei Quellen
**Kernaussage:** Primärdaten selbst erhoben, angereichert mit zwei amtlichen Quellen.
**Darauf:** Eine Tabelle mit drei Zeilen – ElCom über SPARQL (eigenes Skript),
BFS-Regionalporträts, BFS-Raumgliederungen. Je mit Gebietsstand.
**Nicht vergessen:** Dass die Primärquelle **per Web-API** geholt wurde, ist
Pflicht 1. Ein Screenshot der SPARQL-Abfrage wirkt hier besser als Text.
**Spricht:** Lenny · ~40 Sekunden

### Folie 6 · Daten: was daraus wurde
**Kernaussage:** 2087 Gemeinden, 30 Spalten, drei Jahre – und wir wissen genau, was
dabei verloren ging.
**Darauf:** Die Kennzahlen der verbundenen Tabelle. Dazu **ehrlich** zwei
Einschränkungen in Stichworten:
- Gemeindemerkmale stammen aus 2016 bis 2019, Preise aus 2021 bis 2027
- 202 von 2201 Gemeinden fallen heraus, überdurchschnittlich kleine (belegt mit
  Permutationstest)
**Warum das auf die Folie gehört:** Kriterium 4 bewertet, ob wir die Struktur der
Daten erklären. Eine offen genannte Einschränkung zählt mehr als eine, die der Dozent
selber findet.
**Spricht:** Lenny · ~50 Sekunden

### Folie 7 · Methoden
**Kernaussage:** EDA, Tests mit p-Wert, Regression über drei Jahre, k-means.
**Darauf:** Methodenliste, je mit der Unterfrage, die sie beantwortet. Kurz halten,
die nächste Folie ist die wichtigere.
**Spricht:** Subraj · ~40 Sekunden

### Folie 8 · Die methodische Pointe
**Kernaussage:** Strompreise werden nicht von Gemeinden gesetzt, sondern von
Netzbetreibern. Unsere 2087 Beobachtungen sind deshalb nicht unabhängig.
**Darauf:** Eine Zahl gross: **96.8 %** der Preisstreuung liegen zwischen den
Netzbetreibern, nur 35.2 % zwischen den Kantonen (2027). Dazu: 2087 Gemeinden, aber
nur **485 Betreiber** – die effektive Fallzahl ist rund ein Viertel.
**Und was wir deshalb tun:** geclusterte Standardfehler, gruppierte Kreuzvalidierung.
**Spricht:** Subraj · ~50 Sekunden
*Das ist die Folie, die uns von anderen Gruppen unterscheidet. Hier nicht sparen.*

### Folie 9 · Erwartete Resultate I: die Karte
**Kernaussage:** Man sieht die Betreibergebiete, nicht die Kantone.
**Darauf:** `abbildungen/karte_veraenderung_2021_2027.png`, formatfüllend, wenig Text
daneben. Der blaue Block um Zürich, Zug und den Aargau zeigt die Gemeinden, die 2027
wieder günstiger sind als 2021 – und er läuft quer über die Kantonsgrenzen.
**Ein Satz dazu:** «10.9 Prozent der Gemeinden sind wieder unter dem Niveau von 2021,
und sie liegen nicht zufällig verteilt.»
**Spricht:** Lenny · ~40 Sekunden
*Hier ist auch der Ort, um Bonus 3 sichtbar zu machen, ohne ihn zu erwähnen.*

### Folie 10 · Erwartete Resultate II: das Hauptresultat
**Kernaussage:** Gemeindemerkmale erklären den Preis nicht. Das ist die Antwort auf
unsere Forschungsfrage.
**Darauf:** Drei Zahlen nebeneinander, als Schritt-für-Schritt-Geschichte:

| | R² |
|---|---|
| in der Stichprobe | 0.22 |
| Kreuzvalidierung mit zufälligen Folds | 0.21 |
| Kreuzvalidierung mit **nach Betreiber gruppierten** Folds | **−0.10** |

**Wie man es erzählt – das ist der heikle Teil:**

> «Unser Modell erklärt 22 Prozent der Streuung. Das klingt wenig, ist aber noch
> nicht die interessante Zahl. Wenn wir ganze Versorgungsgebiete zurückhalten und das
> Modell auf unbekannte Betreiber loslassen, wird R² negativ. Das Modell ist dann
> schlechter als der blosse Mittelwert. Das heisst: Was es gelernt hat, war nicht
> ‹grosse Gemeinden sind teurer›, sondern ‹diese Gemeinden gehören zu diesem
> Betreiber›. Die Gemeindemerkmale tragen keine übertragbare Information. Den Preis
> macht der Versorger.»

**Was man nicht sagt:** «Leider war unser R² niedrig.» **Was man sagt:** «Das
negative R² ist das Resultat, nicht das Problem.»
**Spricht:** Subraj · ~60 Sekunden

### Folie 11 · Was daraus folgt
**Kernaussage:** Die nächste Frage ist nicht «welche Gemeinde», sondern «welcher
Betreiber, und warum».
**Darauf:** Drei Stichworte – Analyse auf Betreiberebene, Beschaffungsstrategie als
Erklärung, und was bis Januar noch kommt.
**Spricht:** Metehan · ~30 Sekunden

---

## Backup-Folien, nur auf Nachfrage

Nicht vortragen, aber bereithalten. Erfahrungsgemäss kommt mindestens eine dieser
Fragen:

| Frage | Backup-Folie |
|---|---|
| «Warum H4 und standard?» | 4500 kWh ist die ElCom-Referenz; `cheapest` deckt je nach Jahr nur 742 bis 1207 Gemeinden ab |
| «Warum nur 2087 Gemeinden?» | Fusionen, und der Permutationstest zur Verzerrung |
| «Was ist mit dem Messtarif?» | Ab 2026 separat ausgewiesen, vorher in der Netznutzung; darum `total` für den Zeitvergleich |
| «Wie alt sind Ihre Merkmale?» | Die Tabelle der Zeitebenen aus der Integrationsdoku §7b |
| «Sprachregion?» | ANOVA signifikant, erklärt aber 0.4 bis 3.0 Prozent – Signifikanz ist nicht Relevanz |

---

## Was wir am Dienstag entscheiden müssen

1. **Stimmt die Aufteilung?** Lenny 4 Folien, Metehan 3, Subraj 3. Metehan hat die
   kürzeste Redezeit, obwohl er zwei Pflichtpunkte und einen Bonus geliefert hat.
2. **Folie 10 ist die schwierigste.** Wer sie vorträgt, muss negatives R² in drei
   Sätzen verständlich machen. Das sollten wir im Call einmal laut durchspielen.
3. **Zeigen wir die interaktive Karte live?** Dafür: Es beeindruckt. Dagegen: Es
   kostet Zeit, und wenn das WLAN streikt, steht man da. Mein Vorschlag: nein, nur
   das PNG, und die HTML-Datei als Backup auf dem Rechner.
4. **Werkzeug für die Folien.** PowerPoint, Google Slides oder LaTeX – wir brauchen
   am Schluss ein PDF. Wer baut das Deck?
5. **Termin bestätigen.** 8. Dezember, 11:00, SW301 steht in unserer Projektanleitung,
   stammt aber aus unserer Registrierung und nicht aus Moodle. Bitte nachschauen.
6. **Probedurchlauf.** Mein Vorschlag: einmal vollständig am 3. oder 4. Dezember, mit
   Stoppuhr.

---

## Was nach der Präsentation ansteht

Die Folien sind nicht nur für den 8. Dezember. Das PDF wird bis zum 10. Januar auf
Moodle abgegeben und braucht dann zusätzlich:

- den **Anhang mit der Punkteliste**, Screenshots und Code-Ausschnitten zu jedem
  beanspruchten Punkt (`punkteliste.md` ist die Vorlage)
- die **Reflexion zur AI-Nutzung** – die verlangt die Aufgabenstellung sowohl im PDF
  als auch im Video, siehe Kriterium 6 der Videobewertung
