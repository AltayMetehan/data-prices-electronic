# AI-Dokumentation – Lenny Frei

Data Analytics, ZHAW, HS2026. Teil von Pflichtanforderung 8.

Dieses Dokument wird **laufend** nachgeführt, am Ende jeder Arbeitssitzung. Es hält
fest, welche AI-Werkzeuge für welche Aufgaben eingesetzt wurden, welche Vorteile und
Nachteile dabei aufgefallen sind und – besonders – **wo etwas mit AI nicht
funktioniert hat**.

Der letzte Punkt ist der wichtigste. Er lässt sich am Schluss nicht rekonstruieren,
weil man die Fehlschläge vergisst, sobald das Resultat stimmt.

> Hinweis für die Abgabe: Die AI-Reflexion ist zweimal verlangt. Einmal als
> Dokumentation (Pflicht 8) und einmal **in den Folien und im Video** (Kriterium 6 der
> Videobewertung). Dieses Dokument ist die Grundlage für beides.

---

## Verwendete Werkzeuge

| Werkzeug | Wofür |
|---|---|
| Claude Code (Claude Opus 5) in VS Code | Einrichtung der Umgebung, Prüfung der Daten, Korrektur der Projektanleitung, Nachrechnen von Kennzahlen |
| Claude Code in einer Cloud-Sitzung | ein Zwischenschritt am 27./28.10.2026, Resultat verloren (siehe unten) |
| eine weitere, externe AI-Prüfung | Durchsicht des Projekts, lieferte den Befund zur Netzbetreiberebene |

---

## Sitzungsprotokoll

### 27. Oktober 2026 – Einrichtung und erste Prüfung der Daten

- Umgebung geprüft: Python 3.11.4, git 2.50.1, pip vorhanden.
- Repo geklont, virtuelle Umgebung `.venv` angelegt, sieben Pakete installiert
  (pandas, matplotlib, jupyter, requests, openpyxl, geopandas, folium),
  `requirements.txt` von Hand geschrieben statt mit `pip freeze`, damit nur die
  sieben wirklich benötigten Pakete drinstehen und nicht 120 Hilfspakete.
- Die AI hat die Projektanleitung `CLAUDE Data Analytics.md` gelesen und **fünf
  Widersprüche** gefunden, die mir selbst nicht aufgefallen waren: ein fehlender
  Abschnitt 12, der Widerspruch zwischen "nur Codespaces" und einer lokalen
  Installation, eine veraltete Spaltenliste, ein doppelt vergebener Pflichtpunkt 9
  und eine geratene Behauptung über eine angebliche falsche Abgabefrist.
- Nachgerechnet, ob `energie + netznutzung + abgaben + netzzuschlag + messtarif`
  den Gesamtpreis ergibt. Resultat: ja, in allen drei Jahren, grösste Abweichung
  0.001 Rappen. Damit war die vorher ungeklärte Lücke von 1.675 Rappen in den
  2027er-Daten erklärt: Es war der ab 2026 neu ausgewiesene Messtarif.

### 30. Oktober 2026 – Abgleich mit dem Original und methodischer Vorbehalt

- Die Moodle-Seite mit der Aufgabenstellung lag nur als Bild vor (3298 × 21 546
  Pixel, keine Textebene). Die AI hat das Bild in Streifen zerlegt und gelesen.
- Abgleich unserer Punkteliste mit dem Original: **acht Abweichungen**, alle von
  mir verursacht, weil ich die Moodle-Seite zu stark verdichtet zusammengefasst
  hatte. Die wichtigsten: In Pflicht 2 fehlte "Widersprüche auflösen" – das ist
  meine eigene Aufgabe. Und die Videobewertung besteht aus sieben Kriterien, nicht
  aus einer Zeile über die Länge; eines davon verlangt die AI-Reflexion in den
  Folien und im Video.
- Dabei fiel ein **Fehler auf der Moodle-Seite selbst** auf: Die Abgabe des
  Endprojekts trägt im Titel den 10.01.2027, im Fälligkeitsfeld aber den
  11.01.2026. Wird bei den Dozenten nachgefragt.
- Die Referenzwerte der Gruppe (Mittelwerte, Streuungsanteile, 2087 gemeinsame
  Gemeinden) wurden an den CSV-Dateien nachgerechnet und bestätigt. Ergänzt wurde
  die fehlende Zeile für den Netzzuschlag, ohne die eine Spalte nur auf 99.2 Prozent
  statt 100 Prozent kam.
- Neuer Abschnitt 5b zum methodischen Vorbehalt auf Betreiberebene (siehe unten).

### 1. November 2026 – Zweite Datenquelle, Join, und ein Abgleich von Code und Doku

- Die BFS-Quelle **vor** dem Herunterladen geprüft: Die AI hat zuerst die
  Metadaten-Beilage ausgelesen und die Indikatorenliste gezeigt. Dabei stellte sich
  heraus, dass Gemeindetypologie und Sprachregion **nicht** enthalten sind und dass die
  Kennzahlen aus verschiedenen Jahren stammen, von 2016 bis 2019. Zwei Kennzahlen mit
  Bezug 2004/2009 wurden daraufhin ausgeschlossen.
- Die Geodaten aus dem Kurs-Repo geprüft, bevor sie verwendet wurden: Sie decken nur
  den Kanton Zürich ab. Siehe Fall 6 unten.
- Join gebaut: Regionalporträts 2021 ins Breitformat gedreht, über die
  BFS-Gemeindenummer mit den Preisdaten verbunden. **Trefferquote 100 Prozent**, kein
  Datensatz verloren.
- Bei der Prüfung der fehlenden Werte fiel auf, dass das ursprünglich geplante Merkmal
  «Arbeitsstätten» bei 269 Gemeinden fehlt, «Beschäftigte» dagegen nur bei 88, bei einer
  Korrelation von 0.986. Der Tausch brachte 181 Gemeinden zurück ins Modell.
- Notebook `02_daten_bfs_lenny.ipynb` erstellt und ausgeführt, Dokumentation zu
  Pflicht 2 geschrieben.
- Eine eigene Zahl korrigiert: Der Anteil der herausfallenden Gemeinden war mündlich
  mit «gut 17 Prozent» angegeben worden; das galt für die alte Merkmalswahl. Richtig
  sind **gut 9 Prozent**.
- Am selben Tag kam heraus, dass eine seit dem 27.10. geltende Regel zum Messtarif
  falsch herum war. Sie steckte bereits in der ausgelieferten CSV. Siehe Fall 7.
  Abschnitt 4 und 5 der Projektanleitung, das Notebook, die Integrationsdokumentation
  und die Tabelle wurden korrigiert.

---

## Wo etwas mit AI nicht funktioniert hat

### 1. Eine ganze Arbeitssitzung in der Cloud ging verloren (27./28.10.2026)

Zwischen den beiden lokalen Sitzungen habe ich in einer Cloud-Sitzung
weitergearbeitet. Dort entstanden rund vier Commits und acht Dateien, unter anderem
`punkteliste.md`, `folien_entwurf_lenny.md`, `ai_dokumentation_lenny.md` und ein
erster Entwurf des Notebooks.

**Nichts davon existiert mehr.** Die Cloud-Umgebung war nicht als ich bei GitHub
angemeldet und konnte deshalb nicht pushen. Der Container wurde danach gelöscht.
Am 30.10. habe ich den ganzen Benutzerordner durchsuchen lassen: Keine dieser
Dateien ist auf meinem Rechner vorhanden. `git log origin/main..HEAD` zeigte null
lokale Commits, lokaler Stand und GitHub waren identisch.

**Lehre:** Arbeit, die nicht gepusht ist, existiert nicht. Eine Cloud-Sitzung sieht
den eigenen Rechner nicht und muss ihr Ergebnis selbst ins Repo schreiben können.
Vor dem Start einer Cloud-Sitzung prüfen, ob sie Schreibrechte hat.

**Aufwand:** rund zwei Stunden, die neu gemacht werden mussten.

### 2. Eine AI lieferte Zahlen, die eine andere AI nicht reproduzieren konnte (30.10.2026)

Eine externe AI-Prüfung lieferte den – inhaltlich richtigen und wichtigen – Befund,
dass Strompreise nicht pro Gemeinde, sondern pro Netzbetreiber gesetzt werden. Dazu
kamen konkrete Zahlen: 544, 504 und 481 Netzbetreiber in den drei Jahren.

Beim Nachrechnen kam Claude auf 512, 496 und 485. Es wurden **acht verschiedene
Rechenwege** durchprobiert – vier Zuordnungsregeln für Gemeinden mit mehreren
Betreibern, jeweils über zwei Grundmengen. Keiner ergab die gelieferten Zahlen.
Claude hat das gesagt, statt die Zahlen zu übernehmen oder eine Erklärung zu
erfinden.

Die Auflösung: Bei Gemeinden mit mehreren Netzbetreibern hatte die erste AI
denjenigen genommen, der in der CSV-Datei **zufällig zuerst steht**. Dieses Ergebnis
hängt an der Zeilenreihenfolge und ändert sich, sobald Metehan die SPARQL-Abfrage
erneut laufen lässt. Die Zahlen waren damit nicht falsch im Sinne von unplausibel,
aber nicht reproduzierbar.

Im Dokument stehen jetzt die nachgerechneten Zahlen mit der dokumentierten Regel
"der Betreiber mit der kleinsten `netzbetreiber_id`". Die Aussage selbst blieb
unverändert bestehen: Zwischen 95.6 und 98.0 Prozent der Preisstreuung liegen
zwischen den Betreibern, die effektive Fallzahl beträgt rund 500 statt 2087.

**Lehre:** Eine Zahl ohne dokumentierte Methode ist keine Zahl. Dass der Fehler
überhaupt auffiel, lag allein daran, dass eine zweite AI sie nachrechnen wollte und
nicht konnte. Plausibel aussehende Zahlen sind das gefährlichste Ergebnis, weil
niemand sie hinterfragt.

### 3. Eine Datei, die nicht war, was ihr Name sagte (27.10.2026)

Ich hatte eine Datei `pdf24_zusammengefügt.pdf` als "Zusammenfassung aller Daten" in
den Repo-Ordner gelegt. Die AI hat sie vor der Verwendung geprüft: 1795 Seiten,
309 MB, und inhaltlich keine Datenzusammenfassung, sondern Vorlesungsfolien,
Übungsblätter – und **drei eingescannte, korrigierte Prüfungen mit Namen,
Matrikelnummern und Noten von drei fremden Studierenden**.

Unser Repo ist öffentlich. Die Datei wurde aus dem Repo-Ordner entfernt und
zusätzlich über die `.gitignore` abgesichert. Sie war zu keinem Zeitpunkt committet.

**Lehre:** Vor dem Commit prüfen, was in einer Datei wirklich drinsteht, besonders
bei zusammengefügten PDFs und in einem öffentlichen Repo.

### 4. Veraltetes Material eines Klassenkollegen (30.10.2026)

Eine als "Zusammenfassung" weitergegebene Datei eines Klassenkollegen erwies sich
als die offiziellen Kursunterlagen des **Herbstsemesters 2024**. Die AI hat sie mit
der aktuellen Modulbeschreibung verglichen und vier Stellen gefunden, an denen die
Spielregeln seither geändert haben, unter anderem die Notengewichtung (70/30 statt
60/40) und die Pflicht, zehn wöchentliche Übungen abzugeben, die es in HS2026 nicht
mehr gibt.

Eine zweite Datei desselben Kollegen bestand nur aus Bildern ohne Textebene und war
ohne Texterkennung nicht lesbar.

**Lehre:** Unterlagen aus früheren Jahrgängen taugen für den Stoff, nicht für die
Regeln. Verbindlich ist nur die aktuelle Modulbeschreibung auf Moodle.

### 5. Grenzen, die die AI selbst benannt hat

Mehrfach hat die AI gesagt, dass sie etwas nicht wisse, statt zu raten:

- Die 22-Punkte-Liste konnte zunächst nicht geprüft werden, weil die Quelle nur ein
  Screenshot auf Moodle war. Die AI hat das als ungeprüft markiert, statt sie zu
  bestätigen. Erst mit dem exportierten PDF wurde der Abgleich möglich – und ergab
  dann acht Abweichungen.
- Der Termin "8. Dezember, 11:00, SW301" liess sich aus der Moodle-Seite nicht
  bestätigen, weil dort steht, dass die Termine erst nach der Gruppenregistrierung
  festgelegt werden.
- Zur Frage, wie sich das Cloud-Guthaben aktivieren lässt, hat die AI gesagt, sie
  kenne den genauen Befehl nicht, statt einen zu erfinden.

### 6. Dokumentation und Code liefen auseinander (01.11.2026)

Beim Abgleich der Projektanleitung mit Metehans Beschaffungsskript kamen **drei
Stellen** heraus, an denen die Dokumentation etwas anderes sagt als der Code. Alle drei
stammen aus Angaben, die niemand gegen die Quelle geprüft hatte.

**a) Falsche Endpunkt-Adressen.** Die Anleitung nannte
`https://lindas.admin.ch/query` und `https://lindas.admin.ch/elcom/electricityprice`.
Im Skript stehen `https://ld.admin.ch/query` und
`https://energy.ld.admin.ch/elcom/electricityprice`. Wer die Adressen aus unserer
Dokumentation ausprobiert hätte, wäre ins Leere gelaufen.

**b) Eine Behauptung über Geodaten, die die AI selbst erfunden hatte.** Am 27.10. hatte
die AI in die Anleitung geschrieben, im Kurs-Repo von Dr. Gellrich lägen brauchbare
Gemeindegrenzen. Grundlage war ein Hinweis auf Moodle, **nicht** ein Blick in die
Dateien. Am 30.10. wurde nachgesehen: Die KML-Datei enthält 166 Gemeinden mit
BFS-Nummern zwischen 0 und 298, also nur den Kanton Zürich. Die Behauptung stand vier
Tage lang unwidersprochen in der Projektanleitung.

**c) Eine Einschränkung, die falsch war.** Anleitung und geplanter Bericht sagten, die
Fixkosten blieben aussen vor und für Gemeinden mit hoher Grundgebühr unterschätze die
Analyse die Kosten. Der Kommentar im Skript sagte das Gegenteil: Die Fixkosten stecken
bereits in der Netznutzung. Noch am selben Tag an der ElCom-Wegleitung zur
Tarifdeklaration 2026 geklärt: Grund- und Leistungspreise werden in Rappen pro kWh
umgerechnet, die Rappenwerte enthalten die Grundgebühren also bereits. Der
Skriptkommentar stimmt, die Einschränkung war falsch und wurde gestrichen.

**Ein vierter Widerspruch, beim selben Abgleich gefunden:** Abschnitt 4 der Anleitung
ging davon aus, dass es den Messtarif vor 2026 nicht gab. Das Skript sagte, er sei
vorher in der Netznutzung enthalten gewesen. Davon hing die Richtung einer Korrektur
von 1.67 Rappen ab. Dieser Punkt wurde ebenfalls noch am selben Tag geklärt und
erwies sich als der folgenreichste von allen – siehe Fall 7.

**Lehre:** Eine Projektanleitung altert gegenüber dem Code, und zwar unbemerkt. Beide
wurden von Menschen und AI gemeinsam geschrieben, aber nie gegeneinander gelesen. Dass
die Fehler auffielen, lag allein an einem ausdrücklichen Abgleich Zeile für Zeile. Wer
Dokumentation schreibt, muss sie gegen die Quelle prüfen, nicht gegen die Erinnerung.

Bemerkenswert ist Fall b: Hier hat die AI nicht eine fremde Angabe übernommen, sondern
selbst eine plausible Behauptung aufgestellt, ohne sie zu prüfen – und sie dann vier
Tage später selbst widerlegt.

### 7. Eine falsche Annahme war bereits in die Daten eingebaut (27.10. bis 01.11.2026)

Das ist der lehrreichste Fall bisher, weil der Fehler nicht in einem Text stand,
sondern **in einer Datei, die an zwei Teammitglieder gehen sollte**.

**Die Annahme.** Am 27.10. hielt die AI fest: Der Messtarif sei ab 2026 ein neuer
Preisbestandteil, den es 2021 und 2024 nicht gab, und darum beim Vergleich über die
Zeit wegzulassen. Die Beobachtung dahinter stimmte: Das Feld `messtarif` ist 2021 und
2024 leer und 2027 in jeder Zeile gefüllt. Der Schluss daraus war plausibel – und
falsch.

**Wie weit sie sich ausgebreitet hatte.** Bis zum 01.11. stand die Regel
- in Abschnitt 4 der Projektanleitung,
- hinter den Zahlen in Abschnitt 5 (Mittelwert 2027, Nettoanstieg, Anteil der
  Gemeinden unter dem Niveau von 2021),
- als drei eigene Spalten `vergleichbar_*` in
  `daten/verbunden/strompreise_gemeinden.csv`,
- und in einer ausdrücklichen Empfehlung an Subraj, für Zeitvergleiche genau diese
  Spalten zu verwenden.

**Wie sie aufflog.** Nicht durch Nachdenken, sondern durch einen Abgleich: Beim
Durchlesen von Metehans Beschaffungsskript fand sich der Kommentar «Erst ab 2026
separat ausgewiesen, vorher in der Netznutzung enthalten». Das widersprach der
Projektanleitung direkt. Die AI hat den Widerspruch gemeldet, statt eine Seite zu
wählen, und beide Fassungen als ungeklärt markiert.

**Wie sie geklärt wurde.** An der Primärquelle. Die ElCom schreibt zu den Tarifen 2026
wörtlich: «Der Messtarif wird neu separat ausgewiesen. Er war bislang im
Netznutzungstarif integriert.» Damit war die Richtung eindeutig: Die Messkosten gab es
vorher auch, sie standen nur in der Netznutzung.

**Was falsch gewesen wäre.** 2027 ohne Messkosten gegen 2021 mit Messkosten zu
vergleichen. Das hätte 2027 um rund 1.67 Rappen zu billig gemacht und den
Preisanstieg unterschätzt:

| | vorher | richtig |
|---|---|---|
| Mittelwert 2027 | 25.58 Rp | 27.25 Rp |
| Netto 2021 bis 2027 | +4.72 Rp | +6.39 Rp |
| Gemeinden unter dem Niveau 2021 | 14.5 % | 10.9 % |

**Lehre:** Eine Annahme, die einmal in die Daten eingebaut ist, verbreitet sich. Sie
stand nicht nur in einem Dokument, das man korrigieren kann, sondern bereits in einer
CSV-Datei, die an zwei Teammitglieder gehen sollte, zusammen mit der Empfehlung, sie zu
verwenden. Wer die Datei benutzt hätte, hätte den Fehler übernommen, ohne ihn sehen zu
können.

Zwei Dinge haben hier funktioniert: dass der Widerspruch **gemeldet** statt aufgelöst
wurde, und dass die Klärung an der **Primärquelle** erfolgte und nicht an der
plausibelsten Erklärung. Die drei betroffenen Spalten wurden entfernt und nicht nur
umbenannt – eine Spalte, die niemand verwenden soll, wird früher oder später verwendet.

---

## Was gut funktioniert hat

- **Widersprüche in eigenen Texten finden.** Die fünf Fehler in der Projektanleitung
  und die acht Abweichungen zur Aufgabenstellung hätte ich beim Durchlesen nicht
  gefunden. Ein systematischer Abgleich Zeile für Zeile ist genau das, was eine AI
  besser aushält als ein Mensch.
- **Nachrechnen statt glauben.** Jede Zahl, die ins Dokument kam, wurde vorher an
  den CSV-Dateien geprüft. Dabei fiel unter anderem die fehlende Netzzuschlag-Zeile
  auf, ohne die eine Tabellenspalte nur 99.2 Prozent ergab.
- **Einrichtung der Umgebung.** Virtuelle Umgebung, `requirements.txt` und
  `.gitignore` waren in wenigen Minuten erledigt und kommentiert.
- **Unlesbare Quellen erschliessen.** Ein 21 546 Pixel hoher Screenshot und ein
  1795-seitiges PDF wurden maschinell zerlegt und durchsucht.

## Was mühsam war

- **Kontextverlust zwischen Sitzungen.** Jede neue Sitzung beginnt ohne Erinnerung.
  Ohne die Projektanleitung im Repo müsste jedes Mal alles neu erklärt werden. Das
  spricht dafür, Entscheide schriftlich im Repo festzuhalten statt im Chat.
- **Dateigrenzen.** Grosse PDFs und Bilder mussten erst zerlegt werden, bevor sie
  lesbar waren.
- **Versionsunterschiede.** Installiert wurde pandas 3.1.0, während die Kursfolien
  von pandas 2.x ausgehen. Bisher ohne Folgen, aber ein möglicher Stolperstein bei
  Codebeispielen aus dem Unterricht.

---

## Offene Punkte

- Metehan und Subraj führen eigene AI-Notizen. Diese werden vor der Abgabe von mir
  gebündelt (Pflicht 8).
- Die Beispiele 1 und 2 oben gehören in die Folien und ins Video (Kriterium 6).

---

*Letzte Nachführung: 1. November 2026*
