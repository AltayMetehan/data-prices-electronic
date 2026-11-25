# AI Documentation: Collecting the Electricity Prices

ZHAW Data Analytics HS2026 · Altay Metehan · As of 1 November 2026

## Overview

For the data collection (Requirement 1) I used Claude by Anthropic, the Claude app with web search and access to the browser on my computer. The AI found the endpoint, wrote and tested the SPARQL query and turned it into the Python script `strompreise_holen.py`.

| Item | Details |
| --- | --- |
| Tool | Claude (Anthropic), model Claude Opus 5.5, in the Claude app |
| Period | 26 and 27 October 2026 |
| Project part | Fetch the electricity prices of the municipalities from ElCom, years 2021, 2024, 2027 |
| Data source | ElCom tariff data on LINDAS, endpoint `https://ld.admin.ch/query` |
| Result | SPARQL query, Python script, CSV with 143,837 rows |

## Usage log

The AI was used in five steps; most problems only showed up when recalculating.

| No | Date | My request | What the AI did | Result |
| --- | --- | --- | --- | --- |
| 1 | 26 Oct | Where to query the ElCom data via SPARQL | Web search, compiled the LINDAS endpoints and graph URIs, wrote an example query | Useful. The example query was untested |
| 2 | 26 Oct | “I need the electricity prices” | Wrote a query for a single municipality without asking. Running it in the cloud failed because of a network block | Did not work |
| 3 | 26 Oct | Years 2021, 2024, 2027, all prices, plus our project plan as a PDF | Read the plan, tested the query directly on LINDAS through my browser, examined the data structure, checked whether 2027 is already available, wrote the Python script | Works. 2027 is fully available |
| 4 | 27 Oct | About 1.8 centimes are missing from the total | Recalculated all rows and found the cause: the metering tariff was missing from the query. Corrected the script and added a sum check | Fixed, the sum adds up in every row |
| 5 | 27 Oct | Finished query for the LINDAS editor | Complete query including the metering tariff, plus instructions for the web editor | Works |

## Where it did not work

The biggest mistake was about content: the first query returned a wrong total for 2027, and the AI did not notice this itself.

1. **Missing price component.** The first query only contained energy, grid usage, levies and grid surcharge. Since 2026, ElCom reports the metering tariff (`strom:meteringrate`) separately. For 2027 the median was therefore 1.74 Rp./kWh too low. The script even contained the wrong formula as a comment. I found the error myself when recalculating, not the AI.
2. **Wrong first guess.** After my hint, the AI first suspected the fixed costs. Only checking all rows showed: 2021 and 2024 are exactly right, only from 2026 onwards is the metering tariff missing. My own assumption that 2021 was affected was wrong as well.
3. **Guessed instead of asked.** In response to “I need the electricity prices”, the AI wrote a query for a single municipality that I had never mentioned. It should have asked about the years and scope first.
4. **Network block.** The AI runs in a cloud environment that was not allowed to reach LINDAS. The queries were therefore run through the browser on my computer.
5. **Script not run in Python.** Because of the block, the AI only checked the Python script for syntax errors. The query itself was tested, but I had to run the script as a whole myself.

## Advantages and disadvantages

The AI quickly made SPARQL accessible to me, but the data only became reliable through my own recalculation.

**Advantages**

- **Quick start with SPARQL.** SPARQL was not covered in class. The AI read the data model of the ElCom cube directly from the endpoint, so I did not have to work through the documentation.
- **Checks against real data.** The AI did not just write code; it ran the query and reported rows, municipalities and medians per year.
- **Open question answered.** Whether 2027 was already available was open in the project plan. The AI checked it: yes, with 41,440 rows.
- **Hints for the group.** The AI pointed out 120 rows without a municipality name in 2021 (merged municipalities). This matters for Lenny's join.

**Disadvantages**

- **Errors look plausible.** The incomplete query ran without errors and returned sensible numbers. Without recalculating, the error would have gone into the analysis.
- **Assumptions without asking.** With a short request, the AI chose a municipality itself instead of asking.
- **Technical hurdles.** The network block cost time and required the detour through my browser.
- **Confident explanations.** Even the wrong guess (fixed costs) was phrased convincingly.

## How the results were checked

Every row was recalculated: in all 143,837 rows the sum of the components equals the total.

- **Sum check.** total = energie + netznutzung + abgaben + netzzuschlag + messtarif, deviation below 0.01 Rp./kWh. After each download the script prints the number of rows that do not add up. Expected: 0.
- **Spot check.** Windisch 2027, H4: 12.2 + 7.617 + 1.13 + 2.3 + 1.333 = 24.58 Rp./kWh, as in the total.
- **Plausibility.** Median H4 (standard product): 20.56 Rp./kWh (2021), 32.14 (2024), 26.91 (2027). This fits the known development: low before the crisis, peak in 2024, lower afterwards, but not back to the old level.
- **Completeness.** Number of rows per year: 54,210 (2021), 48,187 (2024), 41,440 (2027).

Still open: run the Python script once completely on my computer and compare the output with these numbers.

## Conclusion and lessons

Without AI I would have had to learn SPARQL from scratch; without recalculating we would have analysed wrong prices for 2027.

- **Always recalculate.** Code that runs without errors does not automatically deliver correct data. A built-in check (here the sum check) finds such errors immediately.
- **Ask precisely.** State the years, scope and goal in the first request. With the project plan as a PDF, the answers became much better.
- **Check the data model, don't assume it.** The metering tariff shows that the data structure can change between years. This also matters for the analysis: for a fair comparison of grid usage from 2026 onwards, netznutzung + messtarif have to be added together.
- **For the group.** These points also apply to Lenny's join and Subraj's model when they work with AI.

## Sources

- [ElCom: tariff data and visualisations](https://www.elcom.admin.ch/en/tariff-data-and-visualisations)
- [opendata.swiss: electricity price per grid operator](https://ckan.opendata.swiss/en/perma/electricityprice@elcom)
- [LINDAS SPARQL editor](https://lindas.admin.ch/sparql/)
