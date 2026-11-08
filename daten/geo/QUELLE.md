# Quelle der Gemeindegrenzen

## gemeinden_2087.geojson

Abgeleitet aus **swissBOUNDARIES3D**, nicht selbst erhoben.

- **Datensatz:** swissBOUNDARIES3D, Ausgabe **2026-01**, Ebene `tlm_hoheitsgebiet`
- **Herausgeber:** swisstopo, Bundesamt für Landestopografie
- **Bezogen am:** 07.11.2026, per `scripts/hole_geodaten.py`
- **Download der Rohdatei:** https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.gpkg.zip
- **Produktseite:** https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
- **Lizenz:** kostenlose Geodaten von swisstopo. Nutzung, Verbreitung, Bearbeitung
  und auch kommerzielle Nutzung erlaubt; **Quellenangabe ist Pflicht**. Kein Konto
  und keine Registrierung nötig.
  Nutzungsbedingungen: https://www.swisstopo.admin.ch/de/nutzungsbedingungen-kostenlose-geodaten-und-geodienste
- **Vorgeschriebene Quellenangabe:** eine von sechs gleichwertigen Formen, wir
  verwenden **`©swisstopo`** (so geschrieben, ohne Leerzeichen) bzw. ausgeschrieben
  «Bundesamt für Landestopografie swisstopo». Die Angabe steht in beiden Karten im
  Bild.
- **Join-Schlüssel:** `bfs_nummer`, Ganzzahl, bei uns `gemeinde_nr`

### Was mit den Rohdaten gemacht wurde

Die Rohdatei ist 36 MB gepackt, 74 MB entpackt, und liegt **nicht** im Repo; die
`.gitignore` schliesst `daten/geo/_roh/` aus. `scripts/hole_geodaten.py` erzeugt
daraus die Datei in diesem Ordner:

1. nur die 2087 Gemeinden unserer Analysemenge, geprüft: **alle 2087 sind in der
   Ausgabe 2026-01 vorhanden, keine Lücke**
2. Höhendimension entfernt, sie wird für eine Flächenkarte nicht gebraucht
3. Umrisse vereinfacht mit 100 m Toleranz, in LV95 gerechnet, wo Meter Meter sind
4. umgerechnet nach WGS84 (EPSG:4326), weil Web-Karten das erwarten
5. Koordinaten auf fünf Nachkommastellen gerundet, rund 1 m Genauigkeit

Ergebnis: 1 869 294 Byte statt 74 MB, 0 leere und 0 ungültige Geometrien.

### Einschränkung

Jedes Polygon wird einzeln vereinfacht. Gemeinsame Grenzlinien zweier Nachbarn
werden dadurch nicht identisch behandelt, es können rechnerisch winzige Lücken
entstehen. Bei der Betrachtung der ganzen Schweiz ist das nicht sichtbar; für eine
Karte eines einzelnen Bezirks müsste man feiner vereinfachen.
