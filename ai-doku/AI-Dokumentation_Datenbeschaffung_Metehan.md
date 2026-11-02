# AI-Dokumentation: Datenbeschaffung Strompreise

ZHAW Data Analytics HS2026 · Altay Metehan · Stand 1. November 2026

## Überblick

Für die Datenbeschaffung (Pflicht 1) habe ich Claude von Anthropic eingesetzt, die Claude-App mit Websuche und Zugriff auf den Browser auf meinem Computer. Die AI hat den Endpoint gefunden, die SPARQL-Abfrage geschrieben und getestet und daraus das Python-Script `strompreise_holen.py` gemacht.

| Punkt | Angabe |
| --- | --- |
| Tool | Claude (Anthropic), Modell Claude Opus 5.5, in der Claude-App |
| Zeitraum | 26. und 27. Oktober 2026 |
| Projektteil | Strompreise der Gemeinden von der ElCom holen, Jahre 2021, 2024, 2027 |
| Datenquelle | ElCom-Tarifdaten auf LINDAS, Endpoint `https://ld.admin.ch/query` |
| Ergebnis | SPARQL-Abfrage, Python-Script, CSV mit 143'837 Zeilen |

## Einsatzprotokoll

Die AI kam in fünf Schritten zum Einsatz, die meisten Probleme zeigten sich erst beim Nachrechnen.

| Nr | Datum | Meine Anfrage | Was die AI gemacht hat | Ergebnis |
| --- | --- | --- | --- | --- |
| 1 | 26.10. | Wo man die ElCom-Daten per SPARQL abfragt | Websuche, Endpoints und Graph-URIs von LINDAS zusammengestellt, Beispielabfrage geschrieben | Brauchbar. Die Beispielabfrage war ungetestet |
| 2 | 26.10. | «Ich brauch die Strompreise» | Abfrage für eine einzelne Gemeinde geschrieben, ohne nachzufragen. Ausführung in der Cloud scheiterte an einer Netzwerksperre | Nicht funktioniert |
| 3 | 26.10. | Jahre 2021, 2024, 2027, alle Preise, dazu unser Projektplan als PDF | Plan gelesen, Abfrage über meinen Browser direkt auf LINDAS getestet, Datenstruktur untersucht, geprüft ob 2027 schon vorliegt, Python-Script geschrieben | Funktioniert. 2027 ist vollständig vorhanden |
| 4 | 27.10. | Beim Total fehlen rund 1.8 Rappen | Alle Zeilen nachgerechnet, Ursache gefunden: Messtarif fehlte in der Abfrage. Script korrigiert und Summenkontrolle eingebaut | Behoben, Summe geht bei allen Zeilen auf |
| 5 | 27.10. | Fertige Abfrage für den LINDAS-Editor | Vollständige Query mit Messtarif und Anleitung für den Web-Editor | Funktioniert |

## Wo es nicht funktioniert hat

Der grösste Fehler war inhaltlich: Die erste Abfrage lieferte für 2027 ein falsches Total, und die AI hat das nicht selbst bemerkt.

1. **Fehlender Preisbestandteil.** Die erste Abfrage enthielt nur Energie, Netznutzung, Abgaben und Netzzuschlag. Seit 2026 weist die ElCom den Tarif für das Messwesen (`strom:meteringrate`) separat aus. Bei 2027 fehlten deshalb im Median 1.74 Rp./kWh. Im Script stand sogar die falsche Formel als Kommentar. Gefunden habe ich den Fehler selbst beim Nachrechnen, nicht die AI.
2. **Falsche erste Vermutung.** Auf meinen Hinweis tippte die AI zuerst auf die Fixkosten. Erst die Kontrolle aller Zeilen zeigte: 2021 und 2024 stimmen exakt, nur ab 2026 fehlt der Messtarif. Meine eigene Annahme, dass 2021 betroffen ist, war ebenfalls falsch.
3. **Geraten statt gefragt.** Auf «Ich brauch die Strompreise» schrieb die AI eine Abfrage für eine einzelne Gemeinde, die ich nie genannt hatte. Richtig wäre gewesen, zuerst nach Jahren und Umfang zu fragen.
4. **Netzwerksperre.** Die AI läuft in einer Cloud-Umgebung, die LINDAS nicht erreichen durfte. Die Abfragen liefen deshalb über den Browser auf meinem Computer.
5. **Script nicht in Python ausgeführt.** Wegen der Sperre hat die AI das Python-Script nur auf Syntaxfehler geprüft. Die Abfrage selbst war getestet, das Script als Ganzes musste ich selbst laufen lassen.

## Vorteile und Nachteile

Die AI hat SPARQL für mich schnell zugänglich gemacht, verlässlich wurden die Daten aber erst durch mein Nachrechnen.

**Vorteile**

- **Schneller Einstieg in SPARQL.** SPARQL kam im Unterricht nicht vor. Die AI hat das Datenmodell des ElCom-Cubes direkt am Endpoint ausgelesen, statt dass ich die Dokumentation durcharbeiten musste.
- **Prüft gegen echte Daten.** Die AI hat nicht nur Code geschrieben, sondern die Abfrage laufen lassen und Zeilen, Gemeinden und Mediane pro Jahr ausgegeben.
- **Offene Frage geklärt.** Ob 2027 schon vorliegt, war im Projektplan offen. Die AI hat es geprüft: Ja, mit 41'440 Zeilen.
- **Hinweise für die Gruppe.** Die AI hat auf 120 Zeilen ohne Gemeindenamen in 2021 hingewiesen (fusionierte Gemeinden). Das ist wichtig für Lennys Join.

**Nachteile**

- **Fehler wirken plausibel.** Die unvollständige Abfrage lief fehlerfrei und lieferte sinnvolle Zahlen. Ohne Nachrechnen wäre der Fehler in die Analyse gegangen.
- **Annahmen ohne Rückfrage.** Bei einer knappen Anfrage hat die AI selbst eine Gemeinde gewählt, statt nachzufragen.
- **Technische Hürden.** Die Netzwerksperre kostete Zeit und erforderte den Umweg über meinen Browser.
- **Selbstbewusste Erklärungen.** Auch die falsche Vermutung (Fixkosten) kam überzeugend formuliert.

## Wie die Resultate überprüft wurden

Jede Zeile wurde nachgerechnet: Bei allen 143'837 Zeilen ergibt die Summe der Bestandteile das Total.

- **Summenkontrolle.** total = energie + netznutzung + abgaben + netzzuschlag + messtarif, Abweichung unter 0.01 Rp./kWh. Das Script gibt nach jedem Download die Anzahl Zeilen aus, die nicht aufgehen. Erwartet ist 0.
- **Stichprobe.** Windisch 2027, H4: 12.2 + 7.617 + 1.13 + 2.3 + 1.333 = 24.58 Rp./kWh, wie im Total.
- **Plausibilität.** Median H4 (Standardprodukt): 20.56 Rp./kWh (2021), 32.14 (2024), 26.91 (2027). Das passt zum bekannten Verlauf: tief vor der Krise, Höhepunkt 2024, danach tiefer, aber nicht auf dem alten Niveau.
- **Vollständigkeit.** Anzahl Zeilen pro Jahr: 54'210 (2021), 48'187 (2024), 41'440 (2027).

Offen ist noch: das Python-Script einmal komplett auf meinem Rechner laufen lassen und die Ausgabe mit diesen Zahlen vergleichen.

## Fazit und Lehren

Ohne AI hätte ich SPARQL von Grund auf lernen müssen, ohne Nachrechnen hätten wir falsche Preise für 2027 analysiert.

- **Immer nachrechnen.** Code, der ohne Fehler läuft, liefert nicht automatisch richtige Daten. Eine eingebaute Kontrolle (hier die Summenkontrolle) findet solche Fehler sofort.
- **Präzise fragen.** Jahre, Umfang und Ziel gleich in der ersten Anfrage nennen. Mit dem Projektplan als PDF wurden die Antworten deutlich besser.
- **Datenmodell prüfen, nicht annehmen.** Der Messtarif zeigt, dass sich die Datenstruktur zwischen den Jahren ändern kann. Das ist auch für die Analyse wichtig: Für einen fairen Vergleich der Netznutzung muss man ab 2026 netznutzung + messtarif zusammenzählen.
- **Für die Gruppe.** Diese Punkte gelten auch für Lennys Join und Subrajs Modell, wenn sie mit AI arbeiten.

## Quellen

- [ElCom: Tarifdaten und Visualisierungen](https://www.elcom.admin.ch/en/tariff-data-and-visualisations)
- [opendata.swiss: Strompreis per Stromnetzbetreiber](https://ckan.opendata.swiss/en/perma/electricityprice@elcom)
- [LINDAS SPARQL-Editor](https://lindas.admin.ch/sparql/)
