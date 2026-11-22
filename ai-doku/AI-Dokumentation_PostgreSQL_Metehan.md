# AI-Dokumentation: PostgreSQL

ZHAW Data Analytics HS2026 · Altay Metehan · Stand 22. November 2026

## Überblick

Für Bonus 2 hat Claude das Notebook `03_postgresql.ipynb` geschrieben. Es überträgt unsere SQLite-Datenbank nach PostgreSQL und wertet sie mit Joins und Aggregationen aus. Die SQL-Befehle wurden zuerst mit einem Ersatzmodul geprüft. Am 22. November 2026 wurde zusätzlich PostgreSQL 17.12 lokal mit dem echten Python-Treiber `psycopg2` 2.9.13 verbunden.

| Punkt | Angabe |
| --- | --- |
| Tool | Claude (Anthropic), Modell Claude Opus 5.5, in der Claude-App |
| Datum | 17. November 2026 |
| Projektteil | PostgreSQL mit Joins und Aggregationen (Bonus 2) |
| Eingaben | `strompreise.db` aus Notebook 02, Projektplan |
| Ergebnis | Notebook mit Schema, Datenübernahme, Views, sechs Auswertungen und Kontrolle gegen SQLite |

## Einsatzprotokoll

Auf die Anfrage «Mach mir die Aufgabe mit PostgreSQL und die AI-Doku dazu» folgten fünf Arbeitsschritte.

| Nr | Was die AI gemacht hat | Ergebnis |
| --- | --- | --- |
| 1 | Geprüft, was in ihrer Umgebung verfügbar ist | PostgreSQL 16 vorhanden, Python-Treiber `psycopg2` nicht installierbar |
| 2 | Lokalen PostgreSQL-Server zum Testen gestartet, Ersatzmodul für `psycopg2` geschrieben | SQL läuft auf echtem Server |
| 3 | Schema aus SQLite übernommen und angepasst: Preise als `NUMERIC(7,3)` statt `REAL` | 5 Tabellen, gleiche Schlüssel |
| 4 | Daten aus `strompreise.db` übertragen, Views nachgebaut, sechs Auswertungen geschrieben (Median, Anteile, Ranking mit `HAVING` und `RANK`, Verlauf mit `LAG`, Korrelation mit `CORR`, Quartile mit `NTILE`) | Alle Zellen ohne Fehler |
| 5 | Ergebnis gegen SQLite verglichen | Gleiche Zeilenzahlen, gleiche 2'087 Gemeinden, Abweichungen nur in der 15. Nachkommastelle |

## Wo es nicht funktioniert hat oder unsicher ist

1. **Originaltest ohne echten Treiber.** In der Cloud-Umgebung der AI liess sich `psycopg2` nicht installieren. Die AI hat deshalb ein Ersatzmodul geschrieben, das jeden Befehl über das Kommandozeilenprogramm `psql` schickt. Diese frühen Notebook-Ausgaben stammen nicht von `psycopg2`.
2. **Lokaler Treiber-Test am 22. November 2026.** PostgreSQL 17.12 wurde lokal installiert, die Datenbank `strompreise` angelegt und die Verbindung mit `psycopg2` 2.9.13 erfolgreich geprüft. Das Notebook verwendet jetzt Umgebungsvariablen statt einer `getpass`-Abfrage und einen Pfad zur Repo-Wurzel.
3. **Die AI hat mehr ausgewertet als verlangt.** Die Korrelationen und der Vergleich «zurück auf 2021» sind erste Übersichten ohne p-Werte. Sie gehören in Subrajs Analyse und dürfen nicht als Ergebnisse zitiert werden, bevor er sie getestet hat.
4. **Abgeleitete BFS-Bezeichnungen übernommen.** Die Tabelle `indikator` kommt unverändert aus SQLite. Die 36 nicht geprüften Bezeichnungen sind also auch hier noch offen. Die Auswertungen verwenden nur die 5 geprüften Kennzahlen.

## Vorteile und Nachteile

Die AI hat eine technische Sperre selbst umgangen und offen gesagt, was dadurch ungetestet bleibt.

**Vorteile**

- **Echter Server statt Annahmen.** Statt das SQL nur zu schreiben, hat die AI einen PostgreSQL-Server gestartet und jeden Befehl ausgeführt. Fehler im SQL wären aufgefallen.
- **Unterschiede zu SQLite erklärt.** Das Notebook zeigt in einer Tabelle, was PostgreSQL mehr kann: exakte Dezimalzahlen, Median, Korrelation, Fensterfunktionen. Das hilft beim Video.
- **Gleiche Daten wie SQLite.** Weil die Daten aus `strompreise.db` kommen, rechnen beide Datenbanken nachweislich mit denselben Zahlen.
- **Passwort nicht im Code.** Es wird aus einer Umgebungsvariable gelesen oder abgefragt. So landet es nicht auf GitHub.

**Nachteile**

- **Früher Ersatzteil.** Das Ersatzmodul verhält sich ähnlich wie `psycopg2`, aber nicht gleich. Die lokale Verbindung mit dem echten Treiber beseitigt diese Unsicherheit für die Datenbankanbindung.
- **Lokale Einrichtung erforderlich.** PostgreSQL, die Datenbank `strompreise`, der Benutzer und `PGPASSWORD` müssen auf jedem Rechner eingerichtet werden. Die Anleitung dafür steht in `README.md`.
- **Ungefragte Ergebnisse.** Die Auswertungen zeigen interessante Zahlen, zum Beispiel dass nur 227 von 2'087 Gemeinden 2027 wieder auf dem Niveau von 2021 sind. Ungetestet verleiten solche Zahlen aber zu vorschnellen Schlüssen.

## Wie die Resultate überprüft wurden

PostgreSQL und SQLite enthalten nachweislich dieselben Daten und liefern dieselbe Analysetabelle.

| Prüfung | Ergebnis |
| --- | --- |
| Zeilen pro Tabelle, PostgreSQL gegen SQLite | In allen 5 Tabellen gleich (z. B. tarif 143'837) |
| Preiszeilen, bei denen die Bestandteile nicht das Total ergeben | 0 in allen drei Jahren |
| Gemeinden in `v_analyse`, PostgreSQL gegen SQLite | 2'087 / 2'087, gleiche Nummern |
| Grösste Abweichung der Preise in `v_analyse` | 7.1 × 10⁻¹⁵ Rp./kWh, nur Rundung von Gleitkommazahlen in SQLite |
| Median H4 pro Jahr in PostgreSQL gegen pandas in Notebook 02 | 20.63 / 32.15 / 26.91, identisch |

Erledigt: die echte `psycopg2`-Verbindung wurde auf PostgreSQL 17.12 lokal getestet. Offen bleibt nur die vollständige Wiederholung aller Notebook-Zellen auf jedem neuen Entwicklungsrechner.

## Fazit und Lehren

Das SQL und die echte lokale Python-Anbindung sind geprüft. Bei der anfänglichen Aufgabe hat die AI den Unterschied zwischen Ersatzmodul und echtem Treiber offen benannt.

- **Nachfragen, wie getestet wurde.** «Läuft ohne Fehler» bedeutete zuerst: Ersatzmodul auf einem Testserver. Der lokale Lauf mit echtem `psycopg2` wurde danach separat geprüft.
- **Zweite Quelle als Kontrolle.** Wie bei SQLite war der Vergleich mit einer unabhängigen Rechnung der stärkste Test.
- **Passwörter nie in den Code.** Die AI hat das von sich aus so gelöst. Das sollte für das ganze Repo gelten.
- **Ergebnisse an den Besitzer weitergeben.** Die ungefragten Auswertungen gebe ich an Subraj weiter, statt sie selbst zu interpretieren.

## Quellen

- [PostgreSQL 16: Aggregatfunktionen (percentile\_cont, corr, FILTER)](https://www.postgresql.org/docs/16/functions-aggregate.html)
- [PostgreSQL 16: Fensterfunktionen (LAG, RANK, NTILE)](https://www.postgresql.org/docs/16/functions-window.html)
- [psycopg2: execute\_values](https://www.psycopg.org/docs/extras.html#fast-execution-helpers)
