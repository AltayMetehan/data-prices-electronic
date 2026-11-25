# AI-Dokumentation: Konzeptpräsentation

ZHAW Data Analytics HS2026 · Altay Metehan · Stand 25. November 2026

## Überblick

Für die Konzeptpräsentation (Pflicht 8: AI-Einsatz «for creating the code and the presentation») hat Claude die Folien gestaltet, Diagramme gezeichnet und ein Sprechskript geschrieben. Inhalt und Zahlen stammen aus unserem Repo, die Rahmung als Konzept kam aus dem Team.

| Punkt | Angabe |
| --- | --- |
| Tool | Claude Code (Anthropic), Modell Claude Opus 5.5, in VS Code im Projektordner |
| Folien | Folienvorlage «Slides» auf claude.ai, privates Deck, Export als PDF für Moodle |
| Datum | 24. und 25. November 2026 |
| Projektteil | Live-Präsentation des Projektkonzepts, 10 Minuten, acht Bewertungskriterien |
| Eingaben | Bildschirmfoto der Bewertungskriterien aus Moodle, `README.md`, `folien_entwurf_lenny.md`, `punkteliste.md`, `dokumentation_integration_lenny.md`, `scripts/03_analyse_subraj.ipynb` |
| Ergebnis | 14 Folien mit Navigationsleiste, 3 selbst gezeichnete Diagramme, 4 Grafiken aus dem Repo, Sprechskript in den Vortragsnotizen |

## Einsatzprotokoll

Die Folien entstanden in sechs Runden. Jede Runde war eine kurze Anfrage von mir, danach hat die AI das ganze Deck überarbeitet.

| Nr | Meine Anfrage | Was die AI gemacht hat |
| --- | --- | --- |
| 1 | Folien nach den Kriterien, «stichwortartig und schöner Style» | Gliederung entlang der acht Kriterien, Farbschema und Schriften, Zahlen aus README, Lennys Entwurf und der Integrationsdoku |
| 2 | «sieht sehr mager aus», «kaum Sätze» | Aufzählungen durch Diagramme, Kennzahlen und Schlagworte ersetzt; ganze Sätze in die Vortragsnotizen verschoben |
| 3 | übersichtlicher, Backup-Folien, Grafiken aus Subrajs EDA | Navigationsleiste oben auf jeder Folie, pro Folie eine Grafik mit drei Kernaussagen, Folien zu Rangfolge und Heatmap, acht Backup-Folien |
| 4 | Backup-Folien heraus, Wichtigstes in die Hauptfolien | Backup gelöscht; H4, Ausfall, Datenjahre und Messtarif auf den Folien «Struktur» und «Hintergrund» verdichtet |
| 5 | Sprechskript in die Notizen | ausformulierter Text pro Folie mit Sprecher, Zeit, Übergaben und Antworten für Rückfragen; rund 920 Wörter, 7–8½ Minuten |
| 6 | Rückmeldung aus dem Team zur Rahmung | «Erwartete Resultate» in der Navigationsleiste, ein Satz im Skript, dass die Rechnungen erste Bestätigungen sind, Stand auf der Modellfolie |

## Wo es nicht funktioniert hat oder unsicher ist

Der wichtigste Fehler war nicht technisch: Die AI hat die Folien so gebaut, wie ich gefragt habe, und dabei die Modulbeschreibung nicht beachtet.

1. **Fertige Resultate statt Konzept.** Die Modulbeschreibung sagt zur Live-Präsentation: «This does not cover the finished project work or final results.» Die AI zeigte unsere Rechnungen trotzdem als fertige Resultate. Aufgefallen ist das erst durch eine Rückmeldung aus dem Team. Korrigiert mit «Erwartete Resultate» in der Navigationsleiste und einem Satz im Skript.
2. **Falsche Ausfallzahl.** Auf der Datenfolie stand «202 von 2201 Gemeinden fehlen». 88 dieser 202 Gemeinden sind aber in den 2087 enthalten, ihnen fehlt nur die Beschäftigtenzahl. Die AI hat das beim Abgleich mit der Integrationsdoku (§7) selbst gefunden und die Folie als Trichter 2201 → 2087 → 1999 neu gezeichnet.
3. **Satz passte nicht zur Karte.** Lennys Folienentwurf verortete die günstiger gewordenen Gemeinden um ZH/ZG/AG. Auf der Karte liegen sie vor allem im Raum Bern/Jura. Die AI hatte den Satz zuerst übernommen und ihn erst beim Vergleich mit dem Bild bemerkt. Die Folie ist jetzt neutral formuliert.
4. **Wissen ohne Quelle.** Die Beschreibung des Referenzhaushalts H4 (5-Zimmer-Wohnung, Elektroherd, Tumbler) stammte aus dem Allgemeinwissen der AI, nicht aus unseren Dateien. Die AI hat das selbst markiert. Auf den Folien steht nur «4500 kWh pro Jahr», der Rest ist bei der ElCom zu prüfen.
5. **Layout nicht angesehen.** Mehrere Folien waren zu voll und liefen über den Rand. Die AI hat die Höhen nur nachgerechnet, die Folien aber nicht als Bild angesehen. Die Sichtprüfung musste ich selbst machen.
6. **Zuordnung geraten.** Die Mittelwerte der Sprachregionen (27.2 / 27.5 / 26.8) hat die AI nach der Reihenfolge im Notebook-Text Deutschschweiz, Romandie und Tessin zugeordnet. Das muss Subraj bestätigen. Die Zahlen stehen nur noch in der Spickliste für Rückfragen.
7. **Termin nicht geprüft.** Datum und Uhrzeit der Präsentation (8. Dezember, 11:00) stammen aus unserer Projektanleitung, nicht aus Moodle. Die Begrüssung im Skript hängt davon ab.

## Vorteile und Nachteile

Die AI war schnell und hat Zahlen sauber aus unseren Dateien übernommen. Was gut aussah, musste ich trotzdem gegen Quelle und Aufgabe prüfen.

**Vorteile**

- **Aufbau nach Kriterien.** Die Gliederung folgt genau den acht Bewertungskriterien, auf jeder Folie zeigt die Navigationsleiste, wo wir sind.
- **Grafiken statt Text.** Preisbestandteile, R² nach Validierungsart und der Ausfalltrichter wurden direkt aus unseren Zahlen gezeichnet.
- **Widersprüche gefunden.** Die falsche Ausfallzahl und der Satz zur Karte fielen beim Abgleich mit Integrationsdoku und Kartenbild auf.
- **Skript als Vorlage.** Das Sprechskript mit Zeiten und Übergaben hilft beim Üben. Die Spickliste auf der Schlussfolie deckt die wahrscheinlichsten Rückfragen ab.

**Nachteile**

- **Optimiert auf meine Anfrage.** Die AI hat gemacht, was ich gefragt habe, nicht was die Aufgabe verlangt. Die Rahmung als Konzept musste das Team einbringen.
- **Viele Runden.** Die erste Fassung war zu textlastig, die Backup-Folien wurden gebaut und wieder entfernt. Ein klarer Auftrag am Anfang hätte Runden gespart.
- **Kein Blick aufs Ergebnis.** Die AI hat die Folien nicht als Bild angesehen. Überlaufende Inhalte musste ich selbst finden.
- **Fremde Stimme.** Das Skript klingt nach AI. Wir müssen es in eigene Worte bringen und selbst erklären können.

## Wie die Resultate überprüft wurden

Jede Zahl auf den Folien lässt sich auf eine Datei im Repo zurückführen.

| Prüfung | Ergebnis |
| --- | --- |
| Preise und Bestandteile 2021 / 2024 / 2027 | gleich wie in Notebook 03: 20.86 / 31.99 / 27.25 Rp./kWh |
| Ausfall der Gemeinden | gleich wie in der Integrationsdoku §7: 2201 → 2087 → 1999, p = 0.91 beim Preis |
| Rangkorrelation, Heatmap, Varianzanteile | gleich wie in Notebook 03 |
| Grafiken | Bilder aus Notebook 03 und Lennys Karte, nicht neu erzeugt |
| Text über die Karte | gegen das Kartenbild geprüft, korrigiert (Punkt 3) |
| Rahmung | gegen die Modulbeschreibung geprüft, korrigiert (Punkt 1) |

Offen ist noch: alle Folien im Präsentationsmodus durchklicken, H4-Beschreibung bei der ElCom prüfen, Zuordnung der Sprachregionen mit Subraj klären, Termin in Moodle bestätigen, Probedurchlauf mit Stoppuhr.

## Fazit und Lehren

Die AI ist gut darin, unsere Zahlen übersichtlich darzustellen. Ob die Folien zur Aufgabe passen, muss das Team entscheiden.

- **Die Aufgabe mitgeben, nicht nur die Kriterien.** Mit der Modulbeschreibung von Anfang an wäre Punkt 1 nicht passiert.
- **Jede Zahl braucht eine Quelle im Repo.** Was die AI aus Allgemeinwissen ergänzt, ist eine Vermutung (Punkt 4).
- **Text gegen Grafik prüfen.** Ein Satz über eine Karte stimmt nur, wenn jemand die Karte ansieht (Punkt 3).
- **Folien als Bild ansehen.** Nachgerechnete Höhen ersetzen keinen Blick auf die fertige Folie (Punkt 5).
- **Feedback aus dem Team einholen.** Der wichtigste Fehler wurde von einer anderen Person gefunden, nicht von der AI und nicht von mir.

## Quellen

- Moodle: Bewertungskriterien der Konzeptpräsentation und Modulbeschreibung Data Analytics HS2026
- `ai-doku/ai_dokumentation_gruppe_15.md`, Abschnitt 6.1 (Kurzfassung derselben Arbeit)
