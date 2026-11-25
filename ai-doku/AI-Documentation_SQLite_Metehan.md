# AI Documentation: SQLite Database

ZHAW Data Analytics HS2026 · Altay Metehan · As of 2 November 2026

## Overview

For the SQLite database (Requirement 3), Claude designed the data model, built the database and wrote the notebook `scripts/02_sqlite_metehan.ipynb`. The result matches Lenny's join for all 2,087 municipalities.

| Item | Details |
| --- | --- |
| Tool | Claude (Anthropic), model Claude Opus 5.5, in the Claude app |
| Date | 2 November 2026 |
| Project part | Store electricity prices and FSO municipality data in an SQLite database and query them with SQL from Python |
| Inputs | My three yearly files of electricity prices, the FSO Regional Portraits 2021, Lenny's joined table, our project plan |
| Result | Notebook, database `strompreise.db` with 5 tables and 2 views, 24 MB |

## Usage log

A single request (“How do I make the tables in SQLite? Describe and do it”) triggered six work steps.

| No | What the AI did | Result |
| --- | --- | --- |
| 1 | Examined all files: rows, duplicates, missing values, sum of the price components | 143,837 price rows, no duplicates, the sum adds up everywhere |
| 2 | Recalculated how Lenny formed the price when a municipality has several grid operators | Mean over the grid operators, confirmed for all 2,087 municipalities |
| 3 | Assigned labels to the FSO codes (`Ind_01_01` etc.), web search for the official list | 5 codes clearly checked via Lenny's columns, 36 only derived |
| 4 | Designed the data model: 5 tables with primary and foreign keys, 2 views for the analysis | `gemeinde`, `netzbetreiber`, `tarif`, `indikator`, `kennzahl`, `v_preis_h4`, `v_analyse` |
| 5 | Wrote the notebook: create tables, load, check, five example queries with GROUP BY, JOIN, CASE and a subquery | Runs without errors |
| 6 | Compared the result against Lenny's file | 0 deviations in all 8 columns |

## Where it did not work or is uncertain

The biggest open point are the labels of the FSO indicators: 36 of 41 have not been checked against an official list.

1. **FSO labels only derived.** The FSO file only contains codes. The AI searched online for the official list but found no mapping on opendata.swiss. It then inferred the labels from plausibility, for example Zurich with 0.15 % vacant dwellings. Only 5 codes are certain, whose values match Lenny's columns exactly. In the database the others are marked as `abgeleitet` (derived). Before using them in the model, we have to compare them with the header row of the original FSO file.
2. **Notebook not run in Jupyter.** Jupyter could not be installed in the AI's environment. The AI therefore wrote its own helper program that runs the cells one after another and writes the outputs into the notebook. So the code did run, but not in a real Jupyter kernel. I still have to do this once on my computer.
3. **Wrong explanatory text.** The first version said that merged municipalities from 2021 have no name. The output, however, showed 0 municipalities without a name, because the names come from the FSO. The AI noticed the contradiction itself and corrected the text.
4. **No median in SQLite.** SQLite has no median function. The median is therefore calculated in pandas, not in SQL.

## Advantages and disadvantages

The AI did not only deliver code but also justified its decisions. Where knowledge was missing, however, it guessed.

**Advantages**

- **Data model with reasons.** The AI explained why the data is split across several tables and what primary and foreign keys are for. This way I can explain the notebook in the video.
- **Lenny's logic rebuilt.** Instead of assuming a method, the AI recalculated how Lenny formed the price per municipality. Database and join therefore work with the same numbers.
- **Checks built in.** Foreign keys, the sum of the price components and the comparison with Lenny's file run on every pass.
- **Reusable.** The views are meant for Subraj and Lenny; the schema fits PostgreSQL almost unchanged (Bonus 2).

**Disadvantages**

- **Guessing without a source.** For the FSO codes, the AI inferred labels. It marked this openly, but an error would be hard to spot in the model.
- **More than asked.** The AI also did first analyses, for example prices by municipality size. These are only means without a test and not yet results for the project.
- **Size of the database.** At 24 MB the file is large for the repo. Since the notebook recreates it, it would be better placed in `.gitignore`.

## How the results were checked

For all 2,087 municipalities, the database returns exactly the same values as Lenny's independently built join.

| Check | Result |
| --- | --- |
| Rows loaded: tarif / kennzahl | 143,837 / 89,052, as many as in the CSV files |
| Violated foreign keys | 0 |
| Price rows where the components do not add up to the total | 0 in all three years |
| Municipalities only in the database or only at Lenny's | 0 / 0 |
| Deviating values in `v_analyse` compared with Lenny's file (prices 2021/2024/2027, population, density, area, employees, share 65+) | 0 in all 8 columns |

Still open: run the notebook in Jupyter on my computer and compare the 36 derived FSO labels with the original file.

## Conclusion and lessons

The database is reliable because it was checked against a second, independent calculation. The labels of the FSO codes are not yet.

- **Check against something independent.** Lenny's join was the best test: two paths lead to the same numbers.
- **Have uncertain things marked.** The column `label_quelle` shows which details are checked and which are only guessed. The AI should always do this.
- **Read the outputs, not just the code.** The wrong explanatory text was only noticed because the output showed something else.
- **Provide everything at once.** This time all files and the project plan were included from the start. The AI therefore did not have to assume anything, unlike during the data collection.

## Sources

- [FSO Regional Portraits 2021: key figures of all municipalities (opendata.swiss)](https://ckan.opendata.swiss/dataset/regionalportrats-2021-kennzahlen-aller-gemeinden)
- [ElCom: tariff data and visualisations](https://www.elcom.admin.ch/en/tariff-data-and-visualisations)
