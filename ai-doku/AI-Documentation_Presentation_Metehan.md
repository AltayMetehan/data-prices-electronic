# AI Documentation: Concept Presentation

ZHAW Data Analytics HS2026 · Altay Metehan · As of 25 November 2026

## Overview

For the concept presentation (Requirement 8: AI use “for creating the code and the presentation”), Claude designed the slides, drew charts and wrote a speaker script. Content and numbers come from our repo; the framing as a concept came from the team.

| Item | Details |
| --- | --- |
| Tool | Claude Code (Anthropic), model Claude Opus 5.5, in VS Code inside the project folder |
| Slides | “Slides” template on claude.ai, private deck, exported as PDF for Moodle |
| Date | 24 and 25 November 2026 |
| Project part | Live presentation of the project concept, 10 minutes, eight grading criteria |
| Inputs | Screenshot of the grading criteria from Moodle, `README.md`, `folien_entwurf_lenny.md`, `punkteliste.md`, `dokumentation_integration_lenny.md`, `scripts/03_analyse_subraj.ipynb` |
| Result | 14 slides with a navigation bar, 3 charts drawn from our numbers, 3 figures from the repo, speaker script in the notes; a German and an English version |

## Usage log

The slides were created in seven rounds. Each round was a short request from me, after which the AI revised the whole deck.

| No | My request | What the AI did |
| --- | --- | --- |
| 1 | Slides based on the criteria, “in bullet points and with a nice style” | Outline following the eight criteria, colour scheme and typefaces, numbers from the README, Lenny's draft and the integration documentation |
| 2 | “looks very thin”, “hardly any sentences” | Replaced bullet lists with charts, key figures and keywords; moved full sentences into the speaker notes |
| 3 | Clearer layout, backup slides, figures from Subraj's EDA | Navigation bar at the top of every slide, one figure with three key points per slide, slides on ranking and heatmap, eight backup slides |
| 4 | Remove the backup slides, move the most important points into the main slides | Backup removed; H4, dropout, data years and metering tariff condensed onto the “Structure” and “Background” slides |
| 5 | Speaker script in the notes | Full text per slide with speaker, time, hand-overs and answers for questions; about 920 words, 7–8½ minutes |
| 6 | Team feedback on the framing | “Expected Results” in the navigation bar, one sentence in the script that the calculations are first confirmations, date on the model slide |
| 7 | English version of the presentation and this documentation | Translated the deck, the speaker script and this documentation into English |

## Where it did not work or is uncertain

The most important mistake was not technical: the AI built the slides the way I asked and did not take the module description into account.

1. **Final results instead of a concept.** The module description says about the live presentation: “This does not cover the finished project work or final results.” The AI still presented our calculations as final results. This was only noticed through feedback from the team. Fixed with “Expected Results” in the navigation bar and a sentence in the script.
2. **Wrong dropout number.** The data slide said “202 of 2201 municipalities are missing”. But 88 of these 202 municipalities are included in the 2087; they only lack the number of employees. The AI found this itself when checking against the integration documentation (§7) and redrew the slide as a funnel 2201 → 2087 → 1999.
3. **Sentence did not match the map.** Lenny's slide draft placed the municipalities that became cheaper around ZH/ZG/AG. On the map they are mainly in the Bern/Jura region. The AI first copied the sentence and only noticed when comparing it with the image. The slide now uses neutral wording.
4. **Knowledge without a source.** The description of the reference household H4 (5-room flat, electric stove, tumble dryer) came from the AI's general knowledge, not from our files. The AI flagged this itself. The slides only say “4500 kWh per year”; the rest still has to be checked with ElCom.
5. **Layout not looked at.** Several slides were too full and ran over the edge. The AI only calculated the heights and did not look at the slides as images. I had to do the visual check myself.
6. **Mapping guessed.** The AI assigned the language-region means (27.2 / 27.5 / 26.8) to German-speaking Switzerland, Romandy and Ticino based on the order in the notebook text. Subraj has to confirm this. The numbers are now only in the cheat sheet for questions.
7. **Date not checked.** Date and time of the presentation (8 December, 11:00) come from our project guide, not from Moodle. The greeting in the script depends on it.
8. **Figures not translated.** In the English deck, the figures from the notebook and the map still have German axis labels and titles. The AI can only translate the slide text, not the images; they would have to be re-exported from the notebooks.

## Advantages and disadvantages

The AI was fast and took numbers cleanly from our files. Anything that looked good still had to be checked against the source and the assignment.

**Advantages**

- **Structure based on the criteria.** The outline follows the eight grading criteria exactly; the navigation bar on every slide shows where we are.
- **Charts instead of text.** Price components, R² by validation type and the dropout funnel were drawn directly from our numbers.
- **Contradictions found.** The wrong dropout number and the sentence about the map were noticed when comparing with the integration documentation and the map image.
- **Script as a template.** The speaker script with times and hand-overs helps with rehearsing. The cheat sheet on the final slide covers the most likely questions.
- **Second language quickly.** The English version was created in one step, with the same layout and numbers.

**Disadvantages**

- **Optimised for my request.** The AI did what I asked, not what the assignment requires. The team had to bring in the framing as a concept.
- **Many rounds.** The first version was too text-heavy, and the backup slides were built and then removed again. A clear brief at the start would have saved rounds.
- **No look at the result.** The AI did not view the slides as images. I had to find overflowing content myself.
- **Someone else's voice.** The script sounds like AI. We have to put it into our own words and be able to explain it ourselves.

## How the results were checked

Every number on the slides can be traced back to a file in the repo.

| Check | Result |
| --- | --- |
| Prices and components 2021 / 2024 / 2027 | same as in notebook 03: 20.86 / 31.99 / 27.25 Rp./kWh |
| Dropout of municipalities | same as in the integration documentation §7: 2201 → 2087 → 1999, p = 0.91 for the price |
| Rank correlation, heatmap, variance shares | same as in notebook 03 |
| Figures | images from notebook 03 and Lenny's map, not regenerated |
| Text about the map | checked against the map image, corrected (point 3) |
| Framing | checked against the module description, corrected (point 1) |

Still open: click through all slides in presentation mode, check the H4 description with ElCom, clarify the language-region mapping with Subraj, confirm the date in Moodle, do a rehearsal with a stopwatch.

## Conclusion and lessons

The AI is good at presenting our numbers clearly. Whether the slides fit the assignment is for the team to decide.

- **Give it the assignment, not only the criteria.** With the module description from the start, point 1 would not have happened.
- **Every number needs a source in the repo.** Whatever the AI adds from general knowledge is an assumption (point 4).
- **Check text against the figure.** A sentence about a map is only correct if someone looks at the map (point 3).
- **Look at slides as images.** Calculated heights do not replace looking at the finished slide (point 5).
- **Ask the team for feedback.** The most important mistake was found by another person, not by the AI and not by me.

## Sources

- Moodle: grading criteria for the concept presentation and module description Data Analytics HS2026
- `ai-doku/ai_dokumentation_gruppe_15.md`, section 6.1 (summary of the same work, German)
