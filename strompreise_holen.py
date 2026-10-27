"""
Strompreise der Schweizer Gemeinden von der ElCom holen (via LINDAS SPARQL).

Holt ALLE Tarife (alle Gemeinden, alle Netzbetreiber, alle Verbrauchskategorien
H1-H8 und C1-C7, Produkt "standard" und "cheapest") fuer die Jahre 2021, 2024, 2027
und speichert sie als CSV.

Ausfuehren:   pip install requests pandas
              python strompreise_holen.py

Einheiten: alle Preise in Rappen pro kWh (Rp./kWh), ausser den Spalten mit CHF pro Jahr.
Spalten:
  total         Gesamtpreis exkl. MWST
                = energie + netznutzung + abgaben + netzzuschlag + messtarif
  energie       Energielieferung
  netznutzung   Netznutzung (enthaelt die Fixkosten, auf Rp./kWh umgerechnet)
  abgaben       Abgaben an das Gemeinwesen
  netzzuschlag  Netzzuschlag nach Art. 35 EnG (national einheitlich)
  messtarif     Tarif fuer das Messwesen. Erst ab 2026 separat ausgewiesen,
                vorher in der Netznutzung enthalten. Fuer 2021/2024 daher leer (= 0).
  fixkosten           Grundgebuehr in CHF pro Jahr (nur Info, steckt schon in netznutzung)
  messtarif_chf_jahr  Messtarif in CHF pro Jahr (nur Info, steckt schon in messtarif)
"""

import io
import time

import pandas as pd
import requests

ENDPOINT = "https://ld.admin.ch/query"  # Alternative: https://lindas-cached.cluster.ldbar.ch/query
JAHRE = [2021, 2024, 2027]
OUTPUT = "strompreise_2021_2024_2027.csv"

QUERY_TEMPLATE = """
PREFIX strom: <https://energy.ld.admin.ch/elcom/electricityprice/dimension/>
PREFIX schema: <http://schema.org/>

SELECT ?jahr ?gemeinde_nr ?gemeinde ?netzbetreiber_id ?netzbetreiber ?produkt ?kategorie
       ?total ?energie ?netznutzung ?abgaben ?netzzuschlag ?messtarif
       ?fixkosten ?messtarif_chf_jahr
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

  OPTIONAL { ?obs strom:energy    ?energie }
  OPTIONAL { ?obs strom:gridusage ?netznutzung }
  OPTIONAL { ?obs strom:charge    ?abgaben }
  OPTIONAL { ?obs strom:aidfee    ?netzzuschlag }
  OPTIONAL { ?obs strom:fixcosts  ?fixkosten }
  OPTIONAL { ?obs strom:meteringrate       ?messtarif }
  OPTIONAL { ?obs strom:annualmeteringcost ?messtarif_chf_jahr }

  OPTIONAL { ?m  schema:name ?gemeinde }
  OPTIONAL { ?op schema:name ?netzbetreiber }

  BIND(STR(?period)                       AS ?jahr)
  BIND(STRAFTER(STR(?m),  "municipality/") AS ?gemeinde_nr)
  BIND(STRAFTER(STR(?op), "operator/")     AS ?netzbetreiber_id)
  BIND(STRAFTER(STR(?p),  "product/")      AS ?produkt)
  BIND(STRAFTER(STR(?c),  "category/")     AS ?kategorie)
}
"""


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


def main():
    teile = []
    for jahr in JAHRE:
        t0 = time.time()
        df = hole_jahr(jahr)
        print(f"{jahr}: {len(df):>6} Zeilen, {df['gemeinde_nr'].nunique()} Gemeinden "
              f"({time.time() - t0:.1f} s)")
        teile.append(df)

    alle = pd.concat(teile, ignore_index=True)

    # Falls ein Netzbetreiber/Gemeinde mehrere Namen hat, entstehen doppelte Zeilen -> entfernen
    schluessel = ["jahr", "gemeinde_nr", "netzbetreiber_id", "produkt", "kategorie"]
    vorher = len(alle)
    alle = alle.drop_duplicates(subset=schluessel)
    if vorher != len(alle):
        print(f"{vorher - len(alle)} doppelte Zeilen entfernt")

    # Messtarif gibt es erst ab 2026 separat. Vorher steckt er in der Netznutzung -> 0 setzen
    alle["messtarif"] = alle["messtarif"].fillna(0.0)

    # Kontrolle: Summe der Bestandteile muss das Total ergeben
    bestandteile = ["energie", "netznutzung", "abgaben", "netzzuschlag", "messtarif"]
    differenz = (alle["total"] - alle[bestandteile].sum(axis=1)).abs()
    print(f"Zeilen, bei denen die Summe nicht aufs Total aufgeht: {(differenz > 0.01).sum()}")

    alle = alle.sort_values(schluessel).reset_index(drop=True)
    alle.to_csv(OUTPUT, index=False, encoding="utf-8")

    print(f"\nGespeichert: {OUTPUT} ({len(alle)} Zeilen)")
    print("\nKontrolle: Median Gesamtpreis H4 (Standardprodukt) in Rp./kWh")
    h4 = alle[(alle["kategorie"] == "H4") & (alle["produkt"] == "standard")]
    print(h4.groupby("jahr")["total"].median().round(2).to_string())


if __name__ == "__main__":
    main()
