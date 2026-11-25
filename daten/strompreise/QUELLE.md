# Source of the electricity price data — PRIMARY SOURCE

This is the source that satisfies mandatory requirement 1, «Data collection using
Web Scraping and/or a Web API». The data was collected by the group itself, with
`scripts/strompreise_holen.py`, not downloaded as a ready-made dataset.

## Daten_Strompreise_2021.csv, Daten_Strompreise_2024.csv, Daten_Strompreise_2027.csv

- **Dataset:** «Electricity tariff per provider» (German: «Strompreis per
  Stromnetzbetreiber»), the ElCom electricity price cube on LINDAS
- **Description, as published:** «Electricity tariff per provider and municipality
  in Switzerland»
- **Publisher:** Federal Electricity Commission ElCom, as
  `https://register.ld.admin.ch/opendataswiss/org/elcom`
- **Collected by:** Altay Metehan, via `scripts/strompreise_holen.py`
- **Collected on:** ⚠️ **retrieval date to be confirmed by Altay Metehan.** The Git
  history proves the three files were committed on 2 November 2026 (`0d56262`) at
  the latest, and they have not been modified since.
- **Endpoint:** https://ld.admin.ch/query (LINDAS SPARQL)
- **Cube:** https://energy.ld.admin.ch/elcom/electricityprice
- **Landing page:** https://www.strompreis.elcom.admin.ch/
- **Query:** `query.txt` in the repository root, and `QUERY_TEMPLATE` inside
  `scripts/strompreise_holen.py`. The two differ in one respect: `query.txt` has
  the year hard-coded as `"2021"`, the script uses a placeholder.
- **Update frequency, as published:** annual
- **Format:** CSV, 14 columns, UTF-8
- **Units:** centimes per kWh (cts./kWh), excluding VAT, except
  `messtarif_chf_jahr`, which is in CHF per year

### Scope

| File | Data rows | Municipalities | Grid operators | H4 / standard |
|---|---|---|---|---|
| `Daten_Strompreise_2021.csv` | 54,210 | 2,203 | 601 | 2,374 |
| `Daten_Strompreise_2024.csv` | 48,187 | 2,140 | 577 | 2,300 |
| `Daten_Strompreise_2027.csv` | 41,440 | 2,109 | 537 | 2,242 |

Each file holds **all** tariffs of its year: every municipality, every grid
operator, consumption categories H1–H8 and C1–C7, products `standard` and
`cheapest`. The analysis set of 2,087 municipalities is derived from these files
later, in `scripts/01_daten_bfs_lenny.ipynb`.

## Licence

The cube states its licence itself. Queried from the same endpoint the data comes
from, not read off a website:

```
dcterms:license  ->  https://ld.admin.ch/vocabulary/TermsOfUse/Open-Use
dcterms:rights   ->  https://ld.admin.ch/vocabulary/TermsOfUse/Open-Use
```

That term resolves to:

| | |
|---|---|
| Name | **Open use** (German: «Freie Nutzung») |
| Identifier | `NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired` |
| On opendata.swiss | **OPEN** |

**Attribution is therefore not required** for this source. Commercial use is
permitted as well.

⚠️ **This is a different licence from the FSO data.** The FSO datasets in
`daten/bfs/` and `daten/raumgliederungen/` are **OPEN-BY**, where attribution **is**
mandatory, and swissBOUNDARIES3D in `daten/geo/` requires `©swisstopo`.

We name ElCom as the source everywhere anyway — in both maps, in the
documentation and on the slides. That is **good practice, not an obligation**. The
distinction matters: what the licence demands and what we do voluntarily should
stay distinguishable.

## Frozen snapshot — do not re-run the script

These three files are a **frozen snapshot**. Every figure in this project rests on
exactly this state.

Running `scripts/strompreise_holen.py` again overwrites all three files in place.
If ElCom has corrected anything upstream, the data changes silently, the notebooks
then compute different numbers, and every verified figure in the documentation
becomes invalid without any error being raised. Re-fetch only deliberately — and
then re-run the whole chain and re-check every figure.

### Checked on 25 November 2026: the upstream data is unchanged

The cube reports `dcterms:modified = 2026-11-25`, that is, it was touched on the
day of this check. That alone does not say whether any numbers changed, so it was
tested rather than assumed.

The 2027 query was issued again, with the identical `QUERY_TEMPLATE` and the same
deduplication the script applies, and the result was written to a scratch
directory outside the repository, never into `daten/`. Compared against
`Daten_Strompreise_2027.csv`:

| | Repository, 2 November | LINDAS, 25 November |
|---|---|---|
| Data rows | 41,440 | 41,440 |
| Municipalities | 2,109 | 2,109 |
| Grid operators | 537 | 537 |
| H4 / standard rows | 2,242 | 2,242 |
| H4 / standard, mean `total` | 27.3132 | 27.3132 |
| H4 / standard, median `total` | 26.909 | 26.909 |

A full cell-by-cell comparison of all 41,440 × 14 values found **no difference at
all**. The `modified` date of 25 November 2026 therefore reflects a
republication, not a change of content — at least for the 2027 tariff year.

The analysis stays on the snapshot of 2 November 2026 regardless. That is normal
and correct for a data analysis: the figures must remain reproducible. The point
of this check is that the state is **known** rather than assumed.
