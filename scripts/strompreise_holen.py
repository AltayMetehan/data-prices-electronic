"""
Strompreise der Schweizer Gemeinden von der ElCom holen (via LINDAS SPARQL).

Holt ALLE Tarife (alle Gemeinden, alle Netzbetreiber, alle Verbrauchskategorien
H1-H8 und C1-C7, Produkt "standard" und "cheapest") und speichert JEDES JAHR
in einer eigenen CSV-Datei unter daten/strompreise/:
Daten_Strompreise_2021.csv, Daten_Strompreise_2024.csv, Daten_Strompreise_2027.csv

Ausfuehren:   pip install requests pandas
              python scripts/strompreise_holen.py            -> alle drei Jahre
              python scripts/strompreise_holen.py 2024       -> nur ein Jahr
              python scripts/strompreise_holen.py 2021 2027  -> mehrere bestimmte Jahre
Die Ablage ist unabhaengig vom Arbeitsverzeichnis: Das Skript legt die Dateien immer
unter daten/strompreise/ im Repo ab, nicht im aktuellen Ordner.

Einheiten: alle Preise in Rappen pro kWh (Rp./kWh), ausser messtarif_chf_jahr.
Spalten:
  total         Gesamtpreis exkl. MWST
                = energie + netznutzung + abgaben + netzzuschlag + messtarif
  energie       Energielieferung
  netznutzung   Netznutzung (die Grundgebuehr ist hier schon auf Rp./kWh umgerechnet
                eingerechnet, darum gibt es keine eigene Spalte fuer Fixkosten)
  abgaben       Abgaben an das Gemeinwesen
  netzzuschlag  Netzzuschlag nach Art. 35 EnG (national einheitlich)
  messtarif     Tarif fuer das Messwesen. Erst ab 2026 separat ausgewiesen,
                vorher in der Netznutzung enthalten. Fuer 2021/2024 daher leer.
  messtarif_chf_jahr  Messtarif in CHF pro Jahr (nur Info, steckt schon in messtarif)
"""

import io
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ENDPOINT = "https://ld.admin.ch/query"  # Alternative: https://lindas-cached.cluster.ldbar.ch/query
JAHRE = [2021, 2024, 2027]
# Das Skript liegt in scripts/, die Daten gehoeren in daten/strompreise/ daneben.
WURZEL = Path(__file__).resolve().parent.parent
AUSGABE_ORDNER = WURZEL / "daten" / "strompreise"
OUTPUT_MUSTER = "Daten_Strompreise_{jahr}.csv"

QUERY_TEMPLATE = """
PREFIX strom: <https://energy.ld.admin.ch/elcom/electricityprice/dimension/>
PREFIX schema: <http://schema.org/>

SELECT ?jahr ?gemeinde_nr ?gemeinde ?netzbetreiber_id ?netzbetreiber ?produkt ?kategorie
       ?total ?energie ?netznutzung ?abgaben ?netzzuschlag ?messtarif ?messtarif_chf_jahr
WHERE {
  <https://energy.ld.admin.ch/elcom/electricityprice>
      <https://cube.link/observationSet>/<https://cube.link/observation> ?obs .

  ?obs strom:period       ?period ;
       strom:municipality ?m ;
       strom:operator     ?op ;
       strom:product      ?p ;
       strom:category     ?c ;
       strom:total        ?total .

  FILTER(STR(?period) = "%(jahr)s")

  OPTIONAL { ?obs strom:energy             ?energie }
  OPTIONAL { ?obs strom:gridusage          ?netznutzung }
  OPTIONAL { ?obs strom:charge             ?abgaben }
  OPTIONAL { ?obs strom:aidfee             ?netzzuschlag }
  OPTIONAL { ?obs strom:meteringrate       ?messtarif }
  OPTIONAL { ?obs strom:annualmeteringcost ?messtarif_chf_jahr }

  OPTIONAL { ?m  schema:name ?gemeinde }
  OPTIONAL { ?op schema:name ?netzbetreiber }

  BIND(STR(?period)                        AS ?jahr)
  BIND(STRAFTER(STR(?m),  "municipality/") AS ?gemeinde_nr)
  BIND(STRAFTER(STR(?op), "operator/")     AS ?netzbetreiber_id)
  BIND(STRAFTER(STR(?p),  "product/")      AS ?produkt)
  BIND(STRAFTER(STR(?c),  "category/")     AS ?kategorie)
}
"""

SCHLUESSEL = ["gemeinde_nr", "netzbetreiber_id", "produkt", "kategorie"]
BESTANDTEILE = ["energie", "netznutzung", "abgaben", "netzzuschlag", "messtarif"]


def hole_jahr(jahr: int) -> pd.DataFrame:
    """Fuehrt die SPARQL-Abfrage fuer ein Jahr aus und gibt ein DataFrame zurueck."""
    query = QUERY_TEMPLATE % {"jahr": jahr}
    for versuch in range(3):
        try:
            r = requests.post(
                ENDPOINT,
                data={"query": query},
                headers={"Accept": "text/csv"},
                timeout=180,
            )
            r.raise_for_status()
            return pd.read_csv(io.StringIO(r.text), dtype={"gemeinde_nr": "Int64"})
        except requests.RequestException as e:
            print(f"  Versuch {versuch + 1} fuer {jahr} fehlgeschlagen: {e}")
            time.sleep(5)
    raise RuntimeError(f"Abfrage fuer {jahr} ist dreimal fehlgeschlagen")


def bereinige(df: pd.DataFrame) -> pd.DataFrame:
    """Doppelte Zeilen entfernen und die Summe der Bestandteile kontrollieren."""
    # Falls ein Netzbetreiber/Gemeinde mehrere Namen hat, entstehen doppelte Zeilen
    vorher = len(df)
    df = df.drop_duplicates(subset=SCHLUESSEL)
    if vorher != len(df):
        print(f"  {vorher - len(df)} doppelte Zeilen entfernt")

    # Der messtarif bleibt leer, wo ihn die ElCom nicht liefert. Beim Beschaffen wird
    # nichts veraendert, das passiert spaeter im Code (Abschnitt 3 der Anleitung).
    # Sachlich war der Messtarif 2021/2024 auch nicht null, sondern in der Netznutzung
    # enthalten; eine 0 in der Datei wuerde das verdecken.
    # Nur fuer die folgende Kontrolle wird die Luecke als 0 gerechnet.
    kontrolle = df[BESTANDTEILE].fillna(0.0).sum(axis=1)
    differenz = (df["total"] - kontrolle).abs()
    print(f"  Zeilen, bei denen die Summe nicht aufs Total aufgeht: {(differenz > 0.01).sum()}")

    return df.sort_values(SCHLUESSEL).reset_index(drop=True)


def main():
    jahre = [int(j) for j in sys.argv[1:]] or JAHRE

    for jahr in jahre:
        print(f"\n{jahr}:")
        t0 = time.time()
        df = hole_jahr(jahr)
        if df.empty:
            print(f"  Keine Daten fuer {jahr} gefunden, nichts gespeichert")
            continue

        df = bereinige(df)
        AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
        datei = AUSGABE_ORDNER / OUTPUT_MUSTER.format(jahr=jahr)
        df.to_csv(datei, index=False, encoding="utf-8")

        h4 = df[(df["kategorie"] == "H4") & (df["produkt"] == "standard")]
        print(f"  {len(df)} Zeilen, {df['gemeinde_nr'].nunique()} Gemeinden "
              f"({time.time() - t0:.1f} s)")
        print(f"  Median H4 (Standardprodukt): {h4['total'].median():.2f} Rp./kWh")
        print(f"  Gespeichert: {datei.relative_to(WURZEL)}")


if __name__ == "__main__":
    main()