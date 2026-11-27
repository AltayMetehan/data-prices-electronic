# Integration of the two data sources

**Mandatory requirement 2** · Lenny Frei · Data Analytics, ZHAW, autumn semester 2026 · 1 November 2026

The complete path with code and outputs is in
`scripts/01_daten_bfs_lenny.ipynb`.
This document summarises what was brought together, how, and what was lost on the
way.

---

## 1. The sources

| | Source 1 | Source 2 | Source 3 |
|---|---|---|---|
| Content | electricity prices per municipality | municipality characteristics | canton, language region, typology |
| Publisher | ElCom | Federal Statistical Office (FSO) | Federal Statistical Office (FSO) |
| Obtained by | SPARQL endpoint, our own Python script | download, `regionalportraets_2021.csv` | download, `raumgliederungen_2019.xlsx` |
| Responsible | Metehan | Lenny | Lenny |
| Data as at | 2021, 2024, 2027 | 1 January 2021 | 1 January 2019 |

The requirement asks for two sources; the third was added because neither source 1
nor source 2 contains the canton or the language region. Details in section 9b.

The assignment requires us to collect the data ourselves only for the primary source,
and for the second source it explicitly gives the example «scraped data enriched with
data from opendataswiss». Downloading the FSO data is therefore permissible.

---

## 2. The matching key

The join is made on the **FSO municipality number**. It is the official, unique
number of every Swiss municipality and appears in both sources: as `gemeinde_nr` in
the ElCom data, as `CODE_REGION` in the FSO data.

**Why it works.** Before the join, the format of both sides was checked:

- The FSO codes are 1 to 4 digits long
- **Not a single code has a leading zero**
- Both sides are read in as integers

This is the point at which a join most often fails: if one side came as text with
leading zeros, `04811` would never find its partner `4811`. That was not the case
here, the formats match without any conversion.

Additionally checked: in the FSO data, **no** combination of municipality and
indicator occurs twice. Without this check the pivot would have overwritten values
silently.

---

## 3. Preparation: from long to wide format

The FSO file comes in **long format**: one row per municipality *and* indicator.
Aeugst am Albis occupies 41 rows. The file has 89,093 rows in total, 41 of them
for Switzerland as a whole, leaving 89,052 rows for the 2,172 municipalities.

A join needs one row per municipality. With `pivot` the table was turned around: 41
rows become one row with 39 columns. Without this step every municipality would have
appeared 41 times when joining, and the price data would have been multiplied
accordingly.

The row for Switzerland as a whole (`CODE_REGION = "CH"`) was removed beforehand,
since it is not a municipality.

---

## 4. Different reference years per indicator

Although the file is called «Regionalporträts 2021», the indicators come from
different years:

| Indicator | Reference year | Used |
|---|---|---|
| Population, population density, share aged 65+ | 2019 | yes |
| Jobs | 2018 | yes |
| Total area | 2016 | yes |
| **Settlement areas and their change** | **2004/2009** | **no** |

**Excluded** were `Ind_04_02` and `Ind_04_03`, the settlement areas. Setting data
from the period 2004/2009 against electricity prices of 2027 would not be defensible.

**Kept** was the total area of 2016: municipal areas change almost only through
mergers, and merged municipalities are excluded anyway.

The population figures of 2019 are eight years older than the prices of 2027. Since
population figures change slowly this is acceptable, but it has to be stated in the
report.

---

## 5. Result of the join

| | |
|---|---|
| Municipalities in the analysis | **2,087** |
| Partner found in the FSO data | **2,087** |
| Match rate | **100.00 per cent** |
| Records lost in the join | **0** |
| Records gained | 0 |

**Why the match rate is complete.** Our 2,087 municipalities are the intersection of
all three price years. Whatever appears in it therefore already existed in 2021. The
FSO data has the reference date 1 January 2021 and thus contains every municipality
that existed in 2021.

This is not a coincidence but the consequence of a decision originally taken for a
different reason: restricting to the 2,087 municipalities was meant to secure
**comparability over time**. It additionally resolves the **difference in age between
the two sources**. One decision, two problems solved.

---

## 6. Contradictions between the sources, and how they were resolved

| Contradiction | Resolution |
|---|---|
| long format against wide format | pivot of the FSO data before the join |
| municipality number as text against integer | read in as an integer on both sides, format checked beforehand |
| municipal mergers between 2021 and 2027 | only municipalities that appear in all three years |
| several grid operators per municipality | mean of the price; for the operator attribution, the operator with the smallest `netzbetreiber_id` |
| metering tariff reported separately from 2026 instead of inside the grid usage charge | use `total` for the comparison over time, see section 4 of the project instructions |
| indicators from different years | two indicators excluded, reference years documented |

On the operator attribution: the rule «smallest `netzbetreiber_id`» is arbitrary but
**reproducible**. An earlier analysis had taken the operator that happens to come
first in the CSV file. That result depends on the row order and changes as soon as
the SPARQL query runs again.

---

## 6b. Placeholder rows in the 2021 data

This is the inconsistency that took longest to find, because nothing about it looks
broken: no error, no missing value, no implausible total. It was found by
recomputing, not by reading.

**What the rows are.** For the 2021 tariff year, some grid operators declared a row
with a **grid usage charge of zero**, in most cases with zero energy as well. An H4
household tariff without a grid usage charge cannot exist - every household pays for
the grid. Eleven such rows are in `daten/strompreise/Daten_Strompreise_2021.csv`,
from four operators:

| Operator | Municipalities | `total` of the placeholder row |
|---|---|---|
| Albula Netz AG | Schmitten (GR), Albula/Alvra, Bergün Filisur | 0.000 |
| DransGrid SA | Bourg-Saint-Pierre, Liddes, Orsières | 0.500 / 0.000 / 0.000 |
| Elektra Genossenschaft Waldhäusern | Bünzen | 0.000 |
| Media Mesolcina Energia | Lostallo, Soazza, Grono | 7.200, energy only |
| Gemeinde Sufers, Stromverkauf | Sufers | 12.433, energy only |

**Why these are placeholders and not a cheap tariff.** The same operators report real
grid usage in 2024 and 2027. Media Mesolcina Energia, for example, reports 0.000 in
2021 and between 12.139 and 15.784 in 2024. A tariff that is genuinely cheap stays
cheap; a field that is empty in one year and filled in the next was not a tariff.

**Why it mattered.** The analysis set takes the **mean** across the rows of a
municipality. Where a placeholder row sits next to a real tariff, that municipality's
2021 price is roughly halved - Bergün Filisur appeared at 12.280 instead of 24.560.
On the change map all affected municipalities were clipped at the top of the colour
scale and appeared as maximally red, in two conspicuous clusters in Valais and the
Albula valley. Bourg-Saint-Pierre sat in the 99th percentile of the price rise; after
cleaning it sits in the 44th.

**Two cases, treated differently.** The eleven rows are not one problem but two:

| | Case | Treatment | Count |
|---|---|---|---|
| a) | Placeholder **next to** a real tariff | an artefact of the mean. **Removed**, the municipality keeps its real tariff | **10** |
| b) | Placeholder as the municipality's **only** row | not an artefact but a **missing value**. **Kept** - removing it would drop the municipality out of the intersection of all three years | **1** |

Case b) is **Sufers (3695)**. Its only 2021 row reports energy of 6.433 and grid
usage of 0.000. Filtering it would shrink the analysis set from 2,087 to 2,086 and
the number of municipalities cheaper in 2027 from 227 to 226. The row is therefore
kept, and Sufers is recorded here as a **residual case**: its 2021 price of 12.433
is probably too low, and it is the only municipality in the set for which that is
true.

**Records lost.** 10 of 2,374 rows in the 2021 file, so **2,374 → 2,364**. No
municipality was lost: the analysis set remains at 2,087, and the number of
municipalities present in all three years is unchanged. The filter sits in
`scripts/01_daten_bfs_lenny.ipynb`, cell 17, and prints how many rows it removed and
which one it kept.

**What changed in the figures.** All values below come from the notebook run of
27 November 2026:

| | before | after |
|---|---|---|
| Rows in the 2021 file (H4/standard) | 2,374 | **2,364** |
| Mean `total_2021` | 20.86 | **20.90** |
| Median `total_2021` | 20.53 | **20.55** |
| Minimum `total_2021` | 7.96 | **8.59** |
| Share of dispersion 2021, canton | 60.3 % | **62.3 %** |
| Share of dispersion 2021, grid operator | 95.0 % | **94.9 %** |
| Share of dispersion 2021, language region | 3.0 % | **3.4 %** |
| Municipalities in the analysis | 2,087 | 2,087 |
| Cheaper in 2027 than in 2021 | 227 = 10.9 % | 227 = 10.9 % |
| Mean 2024 / 2027 | 31.99 / 27.25 | 31.99 / 27.25 |
| Range of the change | −2.1 to +27.7 | −2.1 to +27.7 |

**No conclusion of the project changes.** The grid operator still explains around
95 per cent of the dispersion, the share of municipalities that became cheaper is
identical, no sign flips and no p-value crosses a threshold. What was wrong was the
map and three figures on the slides.

**Found by Sub Raj Singh on 21 November 2026** while recomputing the raw data
independently, and fixed on 27 November 2026. It survived every check until then
because a placeholder row passes the sum check as well: 0 = 0 + 0 + 0 + 0.

---

## 7. Which municipalities drop out of the analysis, and are they randomly distributed?

Nothing is lost in the join itself. What is lost, is lost before and after it - for
two mutually independent reasons.

**Reason 1: municipal mergers.** In 2021 the ElCom data contains 2,201 municipalities
for H4/standard, in 2027 only 2,109. Whoever does not appear in all three years drops
out: 114 municipalities.

**Reason 2: statistical confidentiality.** The FSO suppresses values when they would
allow conclusions about individual businesses or people (status `Q`). For the jobs
figure this affects 88 of our 2,087 municipalities.

Both reasons sound harmless. Taken together they are not:

| Group | Count | Median population | Median price 2021 |
|---|---|---|---|
| Kept, all five characteristics present | 1,999 | **1,717** | 20.53 cts. |
| Dropped: jobs figure suppressed | 88 | **312** | 21.03 cts. |
| Dropped: municipal merger | 114 | **669** | 21.14 cts. |

A note on the median of 312, so that nobody «corrects» it back later: the exact
median of the 88 municipalities is **312.5** - the two middle values are 310 and 315.
Python's formatting rounds that to 312, and the notebook prints 312. This
documentation records what the notebook outputs, so 312 it is. Commercial rounding
would give 313; that is not the figure the code produces.

Medians alone carry no conclusion. Hence a **permutation test** with 20,000 draws:
the values of both groups are redistributed at random, and the p-value says how often
chance produces a difference at least as large. The procedure needs no distributional
assumption, which fits here because population figures are strongly right-skewed.

Each group against the right comparison group: the merged municipalities dropped out
**before** the join, so they are compared with all 2,087. The municipalities without
a jobs figure are part of the 2,087 and are compared with the remaining 1,999.

| Group | Population, diff. median | p | Price, diff. median | p | Price, diff. mean | p |
|---|---|---|---|---|---|---|
| Merger (114), against all 2,087 | **−958** | **0.0066** | +0.59 cts. | **0.0095** | −0.07 cts. | 0.7974 |
| Jobs figure suppressed (88), against 1,999 | **−1,404** | **0.0003** | +0.50 cts. | 0.2452 | +0.42 cts. | 0.1892 |

**Finding, as far as the numbers carry:**

**By municipality size the selection is biased.** Both excluded groups are clearly
smaller, and both times the difference is clearly established (p = 0.007 and
p = 0.0003). Of the 2,201 municipalities present in 2021, 202 drop out, a good
9 per cent, and the small and rural ones are over-represented among them. For any
statement about urban and rural areas this matters.

**By price level no bias is established.** Among the merged municipalities the median
is indeed 0.59 centimes higher (p = 0.0095), but the **mean is practically identical**:
20.83 against 20.90 centimes, p = 0.7974. The higher median therefore comes from the
shape of the distribution, not from a generally more expensive price level. In the
second group neither the median (p = 0.2452) nor the mean (p = 0.1892) survives a
test.

An earlier version of this section said both groups were «clearly smaller and somewhat
more expensive». The first part holds, the second was written without a test and does
not stand up that way. Corrected on 8 November 2026.

**How this is dealt with.** The model is computed twice:

1. with the **four complete characteristics** on all **2,087** municipalities
2. with **all five characteristics** on the **1,999** municipalities with complete data

If both show the same picture, the bias is irrelevant. If they do not, that is itself
a result. This is a requirement for the modelling, not for the data preparation.

### On choosing jobs instead of workplaces

Originally `Ind_06_07` workplaces was intended as the characteristic for commercial
load. There, however, **269** values are missing instead of 88, and the gaps likewise
hit the small municipalities. `Ind_06_03` jobs, total was chosen instead:

- 181 more municipalities in the model, 1,999 instead of 1,818
- The correlation between the two indicators is **0.986**, in substance they measure
  the same thing
- Jobs are even the better measure: what counts for the electricity load is how many
  people work, not how many businesses are registered. A joinery with 20 employees and
  a one-man trust office are both «one workplace»

---

## 7b. How many time levels are there in a single row?

The joined table looks like one snapshot. It is in fact assembled from five sources
with five territorial statuses and six data years. Anyone who does not know that will
read it wrongly.

| Column | Source | Territorial status | Reference year of the value |
|---|---|---|---|
| `gemeinde_nr`, `gemeinde` | ElCom | per tariff year | – |
| `netzbetreiber_id`, `netzbetreiber` | ElCom | tariff year 2027 | 2027 |
| `anz_gemeinden_betreiber` | ElCom, derived | tariff year 2027 | 2027 |
| `total_2021` | ElCom | tariff year 2021 | **2021** |
| `total_2024` | ElCom | tariff year 2024 | **2024** |
| `total_2027` | ElCom | tariff year 2027 | **2027** |
| `energie_*`, `netznutzung_*`, `abgaben_*`, `netzzuschlag_*` | ElCom | per tariff year | 2021, 2024, 2027 |
| `messtarif_2027` | ElCom | tariff year 2027 | **2027** |
| `einwohner` | Regional portraits | 1 January 2021 | **2019** |
| `dichte` | Regional portraits | 1 January 2021 | **2019** |
| `anteil_65plus` | Regional portraits | 1 January 2021 | **2019** |
| `beschaeftigte` | Regional portraits | 1 January 2021 | **2018** |
| `flaeche_total` | Regional portraits | 1 January 2021 | **2016** |
| `kanton`, `kanton_nr` | Spatial divisions | 1 January 2019 | 2019 |
| `sprachregion` | Spatial divisions | 1 January 2019 | language areas 2011 |
| `gemeindetyp_9` | Spatial divisions | 1 January 2019 | typology 2012 |
| geometry (`daten/geo/`) | swissBOUNDARIES3D | edition 2026-01 | 2026 |
| four merger cases | historicized commune register | changes 2018–2022 | – |

The reference years of the FSO indicators are read directly from the `PERIOD_REF`
column of the raw file, not taken from a description.

**What this means for the interpretation, without glossing over it: we explain prices
from 2021 to 2027 with municipality characteristics from 2016 to 2019.** For the
municipal area that is a gap of up to eleven years, for the population figures up to
eight. Municipal areas change almost only through mergers, and merged municipalities
have been excluded - there the gap is uncritical. Population figures and jobs, on the
other hand, change continuously. A municipality that grew strongly between 2019 and
2027 is carried in our model with its old size.

This is not negligence but a consequence of what the data offers: the Regional
portraits 2021 are the most recent edition the FSO has published. It does, however,
belong in the report as a limitation, and not only in this documentation.

---

## 8. A deliberate move in the design

The FSO characteristics come from **a single survey** and are **identical** for all
three price years. The prices change between 2021, 2024 and 2027, the municipality
characteristics do not.

That is not a shortcoming but a clean design: any change of the regression
coefficients between the three years therefore comes **exclusively from the price
side**. There is no mixing with municipality characteristics changing at the same
time.

---

## 9. The joined table

`daten/verbunden/strompreise_gemeinden.csv` · 2,087 rows · 30 columns

| Column | Content |
|---|---|
| `gemeinde_nr` | FSO municipality number, the matching key |
| `gemeinde` | name of the municipality |
| `netzbetreiber_id`, `netzbetreiber` | grid operator; where there are several, the one with the smallest id |
| `total_2021`, `total_2024`, `total_2027` | total price in centimes per kWh |
| `energie_*`, `netznutzung_*`, `abgaben_*`, `netzzuschlag_*` | the four price components, per year |
| `messtarif_2027` | metering tariff, exists only from 2026 onwards |
| `einwohner`, `dichte`, `flaeche_total`, `anteil_65plus` | four of the five municipality characteristics, **complete** |
| `beschaeftigte` | fifth municipality characteristic, **88 of 2,087 values missing** |
| `kanton`, `kanton_nr` | canton, abbreviation and number, complete |
| `sprachregion` | `Deutsch`, `Französisch`, `Italienisch` or `Rätoromanisch`, complete |
| `gemeindetyp_9` | municipality typology 2012, 9 types, **1 of 2,087 values missing** |
| `anz_gemeinden_betreiber` | number of municipalities this operator supplies in 2027 for H4/standard |

### Two columns with gaps

Only two of the 30 columns have missing values. Both times the gap is not random, and
both times it has consequences for the modelling.

**`beschaeftigte`: 88 missing values.** The FSO suppresses the figure when it would
allow conclusions about individual businesses (status `Q` in the raw file). This
affects almost exclusively small municipalities: median 312 inhabitants among the
missing against 1,717 among the present ones.

**What this means for the regression: anyone computing with this column and setting
`dropna()` loses 88 municipalities** - and not just any of them, but
over-proportionally the small ones. The sample shrinks from 2,087 to 1,999 and
becomes more urban in the process. Hence the requirement in section 7 to compute the
model twice: once without `beschaeftigte` on all 2,087, once with it on the 1,999.

**`gemeindetyp_9`: 1 missing value.** Prez (2237), created in 2020 out of three
municipalities with different typologies. A `dropna()` on this column costs exactly
one municipality; it does not create a bias.

All the other 28 columns are complete.

**Important for Metehan and Subraj:** for comparisons over time, **use the `total_*`
columns**. Only they contain the same components in all three years.

The four price components are included because sub-question 1 asks which component
accounts for the differences. Two rules for them:

1. **Within one year** the components add up to the total price: four in 2021 and
   2024, five in 2027 (with the metering tariff). Recomputed, largest deviation
   0.001 centimes.
2. **Across the years `netznutzung` is not comparable.** Up to 2024 the metering costs
   were contained in it, from 2026 onwards they stand separately. For a comparison of
   grid costs over time, compute `netznutzung_2027 + messtarif_2027`. `energie`,
   `abgaben` and `netzzuschlag` are directly comparable.

A sum of energie, netznutzung, abgaben and netzzuschlag is **not** comparable across
the years: up to 2024 the metering costs were inside the grid usage charge, from 2026
onwards they are reported separately as `messtarif`. Such a sum would be about 1.67
centimes too low for 2027.

**Corrected on 1 November 2026.** This file previously contained three columns
`vergleichbar_2021/2024/2027` with exactly this wrong sum, together with the
recommendation to use them for the comparison over time. The columns were removed
rather than merely renamed: a column nobody is supposed to use will sooner or later
be used. Background in section 4 of the project instructions.

The column `netzbetreiber_id` is included because, according to section 5b of the
project instructions, prices are set per grid operator and the regression is to be
computed on that level as well.

---

## 9b. Third source: canton, language region and municipality typology

Neither the ElCom price data nor the Regional portraits contain these three
characteristics. Without them, sub-question 1 of the research question - the
differences between cantons and language regions - cannot be answered.

| | |
|---|---|
| Dataset | «Die Raumgliederungen der Schweiz 2019», the FSO's Spatial divisions |
| Publisher | Federal Statistical Office (FSO) |
| Retrieved on | 7 November 2026, via `scripts/hole_zusatzdaten.py` |
| Licence | OPEN-BY, free use with attribution |
| Territorial status (German: «Gebietsstand») | **1 January 2019** |
| Join key | `BFS Gde-nummer`, integer without leading zeros |

Four columns are taken over: `kanton`, `kanton_nr`, `sprachregion` and
`gemeindetyp_9` (municipality typology 2012, 9 types). The language region is stored
as a number in the file; the code list in the same document reads 1 = `Deutsch`,
2 = `Französisch`, 3 = `Italienisch`, 4 = `Rätoromanisch`. Our table holds the plain
text, not the code.

### Contradiction: a territorial status two years too old

The Spatial divisions have the status 1 January 2019, while our analysis set comes
from the price data of 2021. **Four of our 2,087 municipalities are missing**, because
they were only created through mergers in 2020 and 2021.

This was resolved **not by hand** but through the changes table of the FSO's
historicized commune register. Each row there links a predecessor municipality
(`InitialCode`) to its successor (`TerminalCode`). The characteristics of the
successor are taken from the predecessors - but only if these agree with one another.
A merger across a cantonal or a language border would not have produced an
unambiguous value; this is checked in the code, not assumed.

| No | Municipality | Merger | Predecessors | Canton | Language region | Type 9 |
|---|---|---|---|---|---|---|
| 889 | Thurnen | 1 January 2020 | 873 Kirchenthurnen, 874 Lohnstorf, 876 Mühlethurnen | BE (all) | `Deutsch` (all) | 22 (all) |
| 2117 | Villaz | 1 January 2020 | 2111 Villaz-Saint-Pierre, 2116 La Folliaz | FR (all) | `Französisch` (all) | 32 (all) |
| 2237 | Prez | 1 January 2020 | 2185 Corserey, 2213 Noréaz, 2221 Prez-vers-Noréaz | FR (all) | `Französisch` (all) | **not uniform: 32, 23, 23** |
| 2430 | Welschenrohr-Gänsbrunnen | 1 January 2021 | 2423 Gänsbrunnen, 2429 Welschenrohr | SO (all) | `Deutsch` (all) | 32 (all) |

For three of the four municipalities all predecessors agree in all characteristics;
taking the values over is unambiguous.

**Open for Prez (2237):** canton and language region are unambiguous and were taken
over. The municipality typology of the three predecessors is not - Corserey had type
32, Noréaz and Prez-vers-Noréaz type 23. There is no substantively compelling value,
so for the time being no entry is made there. That is the only missing value in the
four new columns, across 2,087 municipalities.

### Checks after the join

| Check | Result |
|---|---|
| Rows | 2,087, unchanged |
| Missing values in `kanton`, `kanton_nr`, `sprachregion` | 0 |
| Missing values in `gemeindetyp_9` | 1 (Prez, see above) |
| Number of cantons | 26 |
| The twelve previous columns | **0 differing values**, column and row order identical |

### Distribution across the language regions

| | our 2,087 | all 2,212 municipalities of Switzerland |
|---|---|---|
| `Deutsch` | 1,365 (65.4 %) | 1,421 (64.2 %) |
| `Französisch` | 595 (28.5 %) | 641 (29.0 %) |
| `Italienisch` | 111 (5.3 %) | 130 (5.9 %) |
| `Rätoromanisch` | 16 (0.8 %) | 20 (0.9 %) |

The shares match those of Switzerland as a whole almost exactly. Our selection is
therefore **not biased** by language region - unlike by municipality size and price
level, see section 7.

A note for the report: measured by **population**, German-speaking Switzerland is
about three quarters of the country; measured by the **number of municipalities**,
only about two thirds. French-speaking Switzerland has many small municipalities.
Anyone confusing the number of municipalities with the share of population will think
our figures are wrong.

---

## 9c. Municipal boundaries for the map (bonus 3)

| | |
|---|---|
| Dataset | swissBOUNDARIES3D, edition 2026-01, layer `tlm_hoheitsgebiet` |
| Publisher | swisstopo |
| Retrieved on | 7 November 2026, via `scripts/hole_geodaten.py` |
| Licence | free geodata, modification permitted, attribution `©swisstopo` mandatory |
| Join key | `bfs_nummer`, integer, called `gemeinde_nr` in our data |
| Coverage | **all 2,087 municipalities present, 0 gaps** |

The raw file is 36 MB compressed and is not kept in the repository. The repository
holds only the derived file `daten/geo/gemeinden_2087.geojson` at 1.9 MB: only our
municipalities, without the Z dimension, simplified with a tolerance of 100 m and
reprojected from LV95 (EPSG:2056) to WGS84 (EPSG:4326). Details in
`daten/geo/QUELLE.md`.

### What the maps show

Two maps, each as a PNG at 300 dpi for the presentation and as an interactive HTML
map: the price level in 2027 and the change from 2021 to 2027.

The change map answers the hypothesis from section 5b of the project instructions -
do the price boundaries follow the supply areas or the cantonal borders? Measured
share of the price dispersion that lies between the groups:

| Year | Canton | Grid operator | Language region |
|---|---|---|---|
| 2021 | 62.3 % | **94.9 %** | 3.4 % |
| 2024 | 23.1 % | **94.0 %** | 1.7 % |
| 2027 | 35.2 % | **96.8 %** | 0.4 % |

Visible on the map as large areas of a single colour spanning dozens of
municipalities and running straight across cantonal borders - most clearly the blue
block around Zurich, Zug and Aargau, where prices in 2027 are back below the level of
2021.

**Limitation:** canton and grid operator are not independent. Many large suppliers are
historically cantonal utilities. The cantonal share of 23 to 62 per cent therefore
arises largely because the cantonal border and the operator boundary often coincide.
The map shows which boundary is the sharper one, not which one is the cause.

**On the scaling of both maps:** the colour scales are clipped at the edges, because
93.8 per cent of municipalities lie between 20 and 32 centimes while the range reaches
up to 45.9. On the change map, zero lies at the centre of the colour scale and the
arms are of different length (−2.1 against +27.7). A symmetric scale would have made
the 227 municipalities that became cheaper invisible; the price for this is that
equally strong blue and red do not mean equally many centimes. All of this is stated
in the notebook as well.

---

## 10. An assumption that turned out to be wrong

From 27 October to 1 November 2026 the rule applied in this project that the metering
tariff had newly been added in 2026 and was to be left out of the comparison over
time. The rule was plausible: the field is empty in 2021 and 2024 and filled in 2027.

It was wrong. ElCom writes about the 2026 tariffs: «Der Messtarif wird neu separat
ausgewiesen. Er war bislang im Netznutzungstarif integriert.» - the metering tariff is
now reported separately, having previously been integrated into the grid usage tariff.
The metering costs existed before as well, they were simply in a different column.

The consequence of the wrong rule would have been that 2027 without metering costs is
compared against 2021 with metering costs - so 2027 appears about 1.67 centimes too
cheap and the price rise is underestimated.

It was noticed only because the comment in Metehan's collection script said something
different from the project instructions. By that time the assumption had already been
built into the delivered table and recommended to Subraj.

Affected figures, corrected:

| | before | correct |
|---|---|---|
| Mean 2027 | 25.58 cts. | **27.25 cts.** |
| Net 2021 to 2027 | +4.72 cts. | **+6.39 cts.** |
| Municipalities below the 2021 level | 14.5 % | **10.9 %** |

---

## 11. Open

- Municipality typology of Prez (2237): the predecessors had different types, see
  section 9b. Either the value stays empty, or the group agrees on a rule that can be
  justified
