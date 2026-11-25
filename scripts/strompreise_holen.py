"""
Fetch the electricity prices of Swiss municipalities from ElCom (via LINDAS SPARQL).

Fetches ALL tariffs (all municipalities, all grid operators, all consumption
categories H1-H8 and C1-C7, products "standard" and "cheapest") and stores EACH
YEAR in its own CSV file under daten/strompreise/:
Daten_Strompreise_2021.csv, Daten_Strompreise_2024.csv, Daten_Strompreise_2027.csv

Run with:   pip install requests pandas
            python scripts/strompreise_holen.py            -> all three years
            python scripts/strompreise_holen.py 2024       -> a single year
            python scripts/strompreise_holen.py 2021 2027  -> several specific years
Where the files land does not depend on the working directory: the script always
writes to daten/strompreise/ inside the repository, not to the current folder.

Units: all prices in centimes per kWh (cts./kWh), except messtarif_chf_jahr.
Columns (the column names stay German because they are identifiers shared with
the CSV, SQLite, PostgreSQL and the SPARQL query):
  total         total price excluding VAT
                = energie + netznutzung + abgaben + netzzuschlag + messtarif
  energie       energy supply
  netznutzung   grid usage. The fixed basic fee is already converted to cts./kWh
                and included here, which is why there is no separate column for
                fixed costs.
  abgaben       levies to public authorities
  netzzuschlag  grid surcharge under Art. 35 EnG (uniform across Switzerland)
  messtarif     metering tariff. Reported separately only from 2026 onwards,
                before that it was contained in netznutzung. Empty for 2021/2024.
  messtarif_chf_jahr  metering tariff in CHF per year (information only, it is
                      already contained in messtarif)
"""

import io
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ENDPOINT = "https://ld.admin.ch/query"  # Alternative: https://lindas-cached.cluster.ldbar.ch/query
JAHRE = [2021, 2024, 2027]
# This script lives in scripts/, the data belongs in daten/strompreise/ next to it.
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
    """Runs the SPARQL query for one year and returns a DataFrame."""
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
            print(f"  Attempt {versuch + 1} for {jahr} failed: {e}")
            time.sleep(5)
    raise RuntimeError(f"The query for {jahr} failed three times")


def bereinige(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows and checks that the components add up to the total."""
    # If a grid operator or a municipality carries several names, duplicates appear
    vorher = len(df)
    df = df.drop_duplicates(subset=SCHLUESSEL)
    if vorher != len(df):
        print(f"  {vorher - len(df)} duplicate rows removed")

    # messtarif stays empty wherever ElCom does not supply it. Nothing is changed
    # while fetching; that happens later in the code (section 3 of the project
    # instructions). Factually the metering tariff was not zero in 2021/2024 either,
    # it was contained in netznutzung; a 0 in the file would hide that.
    # The gap is treated as 0 for the following check only.
    kontrolle = df[BESTANDTEILE].fillna(0.0).sum(axis=1)
    differenz = (df["total"] - kontrolle).abs()
    print(f"  Rows where the components do not add up to the total: {(differenz > 0.01).sum()}")

    return df.sort_values(SCHLUESSEL).reset_index(drop=True)


def main():
    jahre = [int(j) for j in sys.argv[1:]] or JAHRE

    for jahr in jahre:
        print(f"\n{jahr}:")
        t0 = time.time()
        df = hole_jahr(jahr)
        if df.empty:
            print(f"  No data found for {jahr}, nothing saved")
            continue

        df = bereinige(df)
        AUSGABE_ORDNER.mkdir(parents=True, exist_ok=True)
        datei = AUSGABE_ORDNER / OUTPUT_MUSTER.format(jahr=jahr)
        df.to_csv(datei, index=False, encoding="utf-8")

        h4 = df[(df["kategorie"] == "H4") & (df["produkt"] == "standard")]
        print(f"  {len(df)} rows, {df['gemeinde_nr'].nunique()} municipalities "
              f"({time.time() - t0:.1f} s)")
        print(f"  Median H4 (standard product): {h4['total'].median():.2f} cts./kWh")
        print(f"  Saved: {datei.relative_to(WURZEL)}")


if __name__ == "__main__":
    main()
