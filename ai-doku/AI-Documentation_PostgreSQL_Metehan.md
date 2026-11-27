# AI Documentation: PostgreSQL

ZHAW Data Analytics HS2026 · Metehan Altay · As of 22 November 2026

## Overview

For Bonus 2, Claude wrote the notebook `03_postgresql.ipynb`. It transfers our SQLite database to PostgreSQL and analyses it with joins and aggregations. The SQL commands were first tested with a substitute module. On 22 November 2026, PostgreSQL 17.12 was additionally connected locally with the real Python driver `psycopg2` 2.9.13.

| Item | Details |
| --- | --- |
| Tool | Claude (Anthropic), model Claude Opus 5.5, in the Claude app |
| Date | 17 November 2026 |
| Project part | PostgreSQL with joins and aggregations (Bonus 2) |
| Inputs | `strompreise.db` from notebook 02, project plan |
| Result | Notebook with schema, data transfer, views, six analyses and a check against SQLite |

## Usage log

The request “Do the PostgreSQL task for me and the AI documentation for it” was followed by five work steps.

| No | What the AI did | Result |
| --- | --- | --- |
| 1 | Checked what is available in its environment | PostgreSQL 16 available, Python driver `psycopg2` could not be installed |
| 2 | Started a local PostgreSQL server for testing, wrote a substitute module for `psycopg2` | SQL runs on a real server |
| 3 | Took over the schema from SQLite and adapted it: prices as `NUMERIC(7,3)` instead of `REAL` | 5 tables, same keys |
| 4 | Transferred the data from `strompreise.db`, rebuilt the views, wrote six analyses (median, shares, ranking with `HAVING` and `RANK`, development with `LAG`, correlation with `CORR`, quartiles with `NTILE`) | All cells without errors |
| 5 | Compared the result against SQLite | Same row counts, same 2,087 municipalities, deviations only in the 15th decimal place |

## Where it did not work or is uncertain

1. **Original test without the real driver.** In the AI's cloud environment, `psycopg2` could not be installed. The AI therefore wrote a substitute module that sends every command through the command-line program `psql`. These early notebook outputs do not come from `psycopg2`.
2. **Local driver test on 22 November 2026.** PostgreSQL 17.12 was installed locally, the database `strompreise` was created and the connection with `psycopg2` 2.9.13 was tested successfully. The notebook now uses environment variables instead of a `getpass` prompt and a path to the repository root.
3. **The AI analysed more than requested.** The correlations and the “back to 2021” comparison are first overviews without p-values. They belong in Subraj's analysis and must not be quoted as results before he has tested them.
4. **Derived FSO labels taken over.** The table `indikator` comes unchanged from SQLite. The 36 unchecked labels are therefore still open here as well. The analyses only use the 5 checked indicators.

## Advantages and disadvantages

The AI worked around a technical block by itself and openly said what remained untested as a result.

**Advantages**

- **Real server instead of assumptions.** Instead of only writing the SQL, the AI started a PostgreSQL server and ran every command. Errors in the SQL would have shown up.
- **Differences to SQLite explained.** The notebook shows in a table what PostgreSQL can do in addition: exact decimal numbers, median, correlation, window functions. This helps for the video.
- **Same data as SQLite.** Because the data comes from `strompreise.db`, both databases demonstrably work with the same numbers.
- **Password not in the code.** It is read from an environment variable or prompted for. This way it does not end up on GitHub.

**Disadvantages**

- **Early substitute.** The substitute module behaves similarly to `psycopg2`, but not identically. The local connection with the real driver removes this uncertainty for the database connection.
- **Local setup required.** PostgreSQL, the database `strompreise`, the user and `PGPASSWORD` have to be set up on every computer. The instructions are in `README.md`.
- **Unrequested results.** The analyses show interesting numbers, for example that only 227 of 2,087 municipalities are back at the 2021 level in 2027. Untested, however, such numbers tempt one to draw hasty conclusions.

## How the results were checked

PostgreSQL and SQLite demonstrably contain the same data and return the same analysis table.

| Check | Result |
| --- | --- |
| Rows per table, PostgreSQL vs SQLite | Equal in all 5 tables (e.g. tarif 143,837) |
| Price rows where the components do not add up to the total | 0 in all three years |
| Municipalities in `v_analyse`, PostgreSQL vs SQLite | 2,087 / 2,087, same numbers |
| Largest price deviation in `v_analyse` | 7.1 × 10⁻¹⁵ Rp./kWh, only floating-point rounding in SQLite |
| Median H4 per year in PostgreSQL vs pandas in notebook 02 | 20.63 / 32.15 / 26.91, identical |

Done: the real `psycopg2` connection was tested locally on PostgreSQL 17.12. The only thing still open is a complete rerun of all notebook cells on every new development computer.

Re-run on 27 November 2026 on my own computer after the placeholder filter in `v_preis_h4`: all cells without errors, same row counts and the same 2,087 municipalities as SQLite, largest deviation 7.1 × 10⁻¹⁵.

## Conclusion and lessons

The SQL and the real local Python connection are tested. For the initial task, the AI openly named the difference between the substitute module and the real driver.

- **Ask how it was tested.** “Runs without errors” at first meant: substitute module on a test server. The local run with the real `psycopg2` was checked separately afterwards.
- **A second source as a check.** As with SQLite, comparing with an independent calculation was the strongest test.
- **Never put passwords in the code.** The AI solved this on its own. This should apply to the whole repo.
- **Pass results on to their owner.** I pass the unrequested analyses on to Subraj instead of interpreting them myself.

## Sources

- [PostgreSQL 16: aggregate functions (percentile\_cont, corr, FILTER)](https://www.postgresql.org/docs/16/functions-aggregate.html)
- [PostgreSQL 16: window functions (LAG, RANK, NTILE)](https://www.postgresql.org/docs/16/functions-window.html)
- [psycopg2: execute\_values](https://www.psycopg.org/docs/extras.html#fast-execution-helpers)
