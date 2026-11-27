# AI documentation – Group 15

Data Analytics, ZHAW, HS2026 · Subraj Singh, Lenny Frei, Metehan Altay · Mandatory requirement 8

As of 27 November 2026. Bundled from the individual documents in the folder `ai-doku/`.
The full logs with all details are there.

> Moodle asks for the AI reflection in three places: as documentation (mandatory
> requirement 8), as the section «Reflection on AI usage» in the presentation PDF, and in
> the slides and the video (criterion 6 of the video assessment). This document is the basis
> for all three. The use of AI for the final presentation is still missing (section 6).

---

## Summary

All three of us used Claude by Anthropic: for data collection, databases, the join, maps,
analysis, the model and the documentation. The AI made work possible that was not covered in
class (SPARQL, PostgreSQL, clustered standard errors), and it reliably found contradictions in
long documents.

Its biggest disadvantage: errors looked plausible. Code ran without an error message and
produced wrong figures, and statements about data were phrased concretely without having been
checked. These errors were almost always found only by recalculating from the raw data or by a
second, independent calculation, never by the AI alone.

---

## 1. Tools used

| Tool | Who | For what |
|---|---|---|
| Claude (Anthropic), model Claude Opus 5.5, in the Claude app with web search and access to the user's own browser | Metehan | SPARQL query and collection script, SQLite database, PostgreSQL |
| Claude Code (Claude Opus 5) in VS Code | Lenny | setting up the environment, checking data, join, municipal mergers, maps, project guide and requirements checklist |
| Claude Code in a cloud session | Lenny | one intermediate step on 27/28 October 2026; the result was lost (case L1) |
| a further, external AI review | Lenny | review of the project; delivered the finding on the grid operator level |
| Claude (Anthropic), in the Claude app with a cloud workspace | Subraj | assignment and choice of topic, research question, EDA and tests, regression and k-means, review of the whole repository, translation of his files into English |
| Claude Code (Claude Opus 5.5) in VS Code, with the «Slides» template on claude.ai | Metehan | concept presentation: outline, slide design, diagrams, speaker script (24/25 November 2026, see section 6) |

---

## 2. What the AI was used for

| Task | Who | What the AI did | How the result was checked |
|---|---|---|---|
| Assignment, choice of topic, research question | Subraj | summarised the assignment, checked topics against all bonus points, formulated a main question with five sub-questions and methods | compared with the wording on Moodle |
| Project guide and requirements checklist | Lenny | checked the guide for contradictions (five found), compared the checklist with the Moodle page (eight deviations found) | line-by-line comparison with the original |
| Data collection (mandatory requirement 1) | Metehan | found the endpoint, read the data model of the ElCom cube, wrote the SPARQL query and the Python script | sum check over all 143,837 rows, manual sample |
| Join (mandatory requirement 2) | Lenny | checked the Federal Statistical Office (FSO) source before downloading, pivoted the regional portraits to wide format, joined via the municipality number, resolved mergers via the mutation table | match rate, permutation test for selection bias, comparison with Switzerland as a whole |
| SQLite (mandatory requirement 3) | Metehan | designed a data model with 5 tables and 2 views, wrote the notebook | 0 deviations from Lenny's join in all 8 columns |
| Maps (bonus point 3) | Lenny | clarified the licence, checked coverage, built two maps as images and interactively | looked at the finished images (case L11) |
| PostgreSQL (bonus point 2) | Metehan | transferred the schema, rebuilt the views, six analyses with joins, aggregations and window functions | same row counts and values as SQLite, deviation at most 7 × 10⁻¹⁵ |
| EDA and tests (mandatory requirement 4, bonus point 4) | Subraj | built notebook 03 on the real data, every test at municipality and at operator level | every number in the text checked against the output in the notebook |
| Regression, model quality, k-means (mandatory requirements 5 to 7, bonus point 5) | Subraj | notebook 04, with self-programmed clustered standard errors and grouped cross-validation | coefficients checked against scikit-learn (identical), cross-check against statsmodels prepared |
| Review of the whole repository | Subraj | independently recalculated raw data, join and database, checked the creativity evidence against the course repositories | rebuilt the join exactly, rebuilt the database and compared it table by table |

---

## 3. Advantages

1. SPARQL, PostgreSQL and clustered standard errors were not covered in class. The AI read
   the data model of the ElCom cube directly at the endpoint and implemented the formula for
   the standard errors together with a check (Metehan, Subraj).
2. Nobody would have found five errors in the project guide, eight deviations of the checklist
   from the assignment and four errors in the project plan just by reading. An AI keeps up a
   line-by-line comparison better than a person (Lenny, Subraj).
3. The AI did not only write queries and code, it also ran them and printed row counts,
   medians and sums. Whether ElCom had already published the 2027 tariffs was open; the AI
   checked it (Metehan).
4. The AI built in checks: sum check, foreign keys, comparison of two databases, `assert`
   checks when joining the data. They run every time (all).
5. The AI marked 36 unchecked FSO labels as «derived», named figures from another AI that
   could not be reproduced as such, and said what had been tested with a substitute module
   instead of the real driver (Metehan, Lenny).
6. Prices are set per grid operator, not per municipality. From this followed the clustered
   standard errors, the calculations at operator level and the grouped cross-validation.
   Without them we would have clearly overestimated the model quality (Lenny, Subraj).
7. A screenshot of the Moodle page 21,546 pixels high and a PDF with 1,795 pages were split up
   and searched (Lenny).

---

## 4. Disadvantages

1. The first SPARQL query ran without errors and returned sensible figures, but without the
   metering tariff (German: «Messtarif»). Wrong guesses were also phrased convincingly (all).
2. The AI described data sources without opening them and cited evidence without calling it
   up. A note «Clarified on …» created trust although the link was dead (Lenny).
3. Given a short request, the AI picked a municipality itself instead of asking about years
   and scope. In another case it wanted to start with invented test data before the real data
   were available (Metehan, Subraj).
4. The AI ran analyses nobody had asked for, for example correlations in the PostgreSQL
   database. Untested, such figures invite hasty conclusions (Metehan).
5. The AI's cloud environments could not install packages (Jupyter, statsmodels, psycopg2) or
   could not reach interfaces (LINDAS). What did not run there was not tested (all).
6. Every new session starts without prior knowledge. Decisions therefore have to be written
   down in the repository (Lenny).
7. The AI's own checks were not complete. A second AI reviewing the same files found gaps the
   first had missed (Subraj).

---

## 5. Where something did not work with AI

The most important cases from all three parts. The L numbers correspond to the cases in
Lenny's document. The M and S numbers are assigned for this overview; the details are in the
documents of Metehan and Subraj.

| No | Date | What did not work | How it was noticed | Consequence |
|---|---|---|---|---|
| M1 | 26/27 Oct | The first SPARQL query left out the metering tariff. In 2027 a median of 1.74 cts./kWh was missing. The AI did not notice it and, after Metehan's hint, first suspected the fixed costs | Metehan, when recalculating | query corrected, sum check built into the script |
| L7 | 27 Oct to 1 Nov | The AI decided to leave out the metering tariff in the time comparison. The rule was in the guide and in three columns of the joined table that was to go to two team members. 2027 would have been 1.67 cts. too cheap | contradiction between the guide and a comment in the script, clarified with ElCom's primary source | columns removed, figures corrected |
| L1 | 27/28 Oct | A cloud session could not push; four commits and eight files were lost | search on the own computer | about two hours of work redone |
| L2 | 30 Oct | An external AI delivered figures on the grid operators that could not be recalculated; they depended on the random row order | a second AI could not reproduce them | documented rule: operator with the smallest ID |
| L6 | 27 Oct to 30 Oct | The AI claimed the course repository contained usable municipal boundaries. The file covers only the canton of Zurich | looking into the file | boundaries taken from swisstopo |
| L9 | 27 Oct to 7 Nov | The guide described the FSO data as containing canton and language region, which they do not. Sub-question 1 and the ANOVA could not have been computed | preparing the map, one week later | third data source added |
| L8 | 7 Nov | Metehan's AI sorted the files into subfolders without updating the paths. Both notebooks broke, but the committed outputs looked correct | run on a fresh clone | paths derived from the repository root, rule in the README |
| L11 | 7 Nov | The colour scale of the change map was chosen by the textbook and hid exactly the municipalities that mattered | looking at the finished image | scale with branches of unequal length |
| L12 | 8 Nov | A reference in the guide led to a dead address, and one statement («somewhat more expensive») did not survive a test | audit against primary sources and raw data | references replaced, statement weakened |
| L15 | 25 Nov | The tile source of the interactive maps (CartoDB) now requires an API key and delivered a full-coverage grid of «API KEY REQUIRED» instead of the background map. The notebook reported zero errors. The AI had printed the warning itself and overlooked it in the audit of 24 Nov | screenshot of the finished map in the browser, not the notebook's output | switched to Esri World Light Gray Base; the obvious substitute OpenStreetMap was rejected after looking at it, because blue lakes and blue (i.e. cheaper) municipalities can be confused |
| M2 | 2 Nov | The AI inferred 36 of 41 FSO labels only by plausibility | marked by the AI itself | only the 5 checked indicators used |
| M3 | 2, 17 and 22 Nov | Jupyter and psycopg2 could not be installed in the original cloud environment. The PostgreSQL notebook first ran with a substitute module on a test server | named by the AI itself; on 22 Nov a local PostgreSQL 17.12 / psycopg2 connection was checked | real psycopg2 included, interactive password prompt removed, repository path added |
| S1 | 10 Oct | The first list of topics did not check whether the data would be collected by scraping or an API; for several topics a ready-made dataset would have been the main source | Subraj asked | new topics with own data collection |
| S2 | 8 and 17 Nov | statsmodels could not be installed; the clustered standard errors were programmed by hand | environment | cross-check against statsmodels prepared in the notebook; still to be run locally |
| S3 | 17 Nov | The AI's own interpretation contained three statements that were stronger than the figures | checking every number against the output | corrected |
| S4 | 21 Nov | Notebook 03 lacked the correlation with the size of the grid operator, although sub-question 2 names it explicitly | comparison with the project plan | added as section 8.6; at municipality level the strongest relationship in the project |
| S5 | 21 Nov | In 2021, ten municipalities have a placeholder tariff with grid usage (German: «Netznutzung») of 0 next to a real tariff of another operator. Database and join take the mean, so their 2021 price was roughly halved. All previous checks passed, because a placeholder row also passes the sum check (0 = 0 + 0 + …) | independent recalculation from the raw data (first seven municipalities found; the clean-up found ten) | cleaned up on 27 Nov in notebooks 01 and 02 and in PostgreSQL; notebooks 03 and 04 re-run, no conclusion changes, one finding becomes stronger |
| S6 | 21 Nov | The requirements checklist claimed the map in Python as creative. The exercises in week 5 do exactly that | comparison with the course repositories | claim removed |
| S7 | 23 Nov | Two cells in notebook 03 reported correlations without a p-value, although bonus point 4 requires one for every test. Subraj's AI had not noticed it in its own checks | review by Lenny's AI | p-values added, the heatmap with a Bonferroni threshold |

---

## 6. AI use for the presentation

Mandatory requirement 8 asks for the AI use «for creating the code and the presentation». The
final slides are made after the concept presentation. It will then be recorded what AI was used
for in the outline, texts, graphics and video, what was adopted and what had to be rejected or
corrected. This section will be completed then.

### 6.1 Concept presentation (Metehan, 24/25 November 2026)

**Tool.** Claude Code with the model Claude Opus 5.5 in VS Code, in the project folder. The
slides were made with the «Slides» template on claude.ai, as a private deck that is shown in the
browser and exported as PDF.

**Inputs.** A screenshot of the assessment criteria from Moodle (eight criteria, 10 minutes),
plus the files from the repository: `README.md`, `folien_entwurf_lenny.md`, `punkteliste.md`,
`dokumentation_integration_lenny.md` and the notebook `scripts/03_analyse_subraj.ipynb`. The
figures on the slides come from these files; the graphics on ranking, heatmap, cantons, box
plots and the map are the images from Subraj's notebook and Lenny's map.

**Process in six rounds.**

| Round | Request | Result |
|---|---|---|
| 1 | slides following the criteria, «in keywords and a nice style» | outline along the eight criteria, own colour scheme |
| 2 | «looks very thin», «hardly any sentences» | bullet lists replaced by diagrams, key figures and keywords; sentences moved to the speaker notes |
| 3 | clearer, backup slides, graphics from Subraj's EDA | navigation bar, one graphic with three key messages per slide, two new EDA slides, eight backup slides |
| 4 | backup slides out again, the most important into the main slides | 14 slides; key points (H4, drop-outs, data years, metering tariff) condensed on «Structure» and «Background» |
| 5 | speaker script in the notes | full text per slide with speaker, time and notes for questions |
| 6 | feedback from the team on the framing | navigation bar «Expected results», one sentence in the script that the calculations are first confirmations |

**Adopted.** Structure following the assessment criteria, the layout «one graphic, three key
messages», the self-drawn diagrams (price components, R² by validation type, drop-out funnel),
the speaker script as a template that we still put into our own words.

**Rejected.** The first version with many full sentences on the slides (too text-heavy). The
eight backup slides, because they bloated the deck; only their key messages remained.

**Where it did not work.**

| No | What did not work | How it was noticed | Consequence |
|---|---|---|---|
| P1 | The data slide claimed «202 of 2,201 municipalities are missing». But 88 of these 202 are part of the 2,087; they only lack the job figure | comparison with the integration documentation (§7) during revision | shown as a funnel 2,201 → 2,087 → 1,999 |
| P2 | Lenny's slide draft placed the municipalities that became cheaper around ZH/ZG/AG. On the map they lie mainly around Bern/Jura. The AI had first adopted the sentence | comparison of the text with the map | statement on the slide phrased neutrally |
| P3 | The description of the reference household H4 (5-room flat, electric cooker, tumble dryer) came from the AI's general knowledge, not from our sources | marked by the AI itself | only «4,500 kWh per year» adopted; the rest to be checked with ElCom |
| P4 | Several slides were too full and ran over the edge. The AI did not look at the layout as an image but only recalculated the heights | revision, the team clicking through | content shortened; visual check remains with the team |
| P5 | The AI showed the calculations as finished results without checking the module description: the live presentation «does not cover the finished project work or final results» | feedback from the team | «Expected results» in the navigation bar, note in the script, status on the model slide |
| P6 | The assignment of the language region means (27.2 / 27.5 / 26.8) to German-speaking Switzerland, French-speaking Switzerland and Ticino followed only the order in the notebook text | marked by the AI itself | to be confirmed by Subraj; slide removed, figures only in the cheat sheet |

**Learned.** Section 7 also applies to slides: every figure on a slide needs a source in the
repository (P1, P3), a text about a graphic must be checked against the graphic (P2), and a
slide has to be looked at as a finished image (P4). The AI optimises for the request it gets;
the team had to bring in the constraints of the module description itself (P5).

---

## 7. What we learned

1. Code without an error message does not automatically produce correct figures (M1, L7, S5).
   A built-in check finds many errors immediately, but not all: the sum check also passed
   placeholder tariffs.
2. The strongest tests were two routes to the same result: database against join, PostgreSQL
   against SQLite, a second AI against the first (L2, M2, S5, S7).
3. A description of data or a reference that nobody has opened is a guess (L6, L9, L12, S6).
4. A graphic has to be looked at as a finished image, and a notebook has to be run on a fresh
   clone. Committed outputs are a photo from yesterday (L8, L11).
5. With the project plan and the files available from the start, the AI did not have to assume
   anything (M1, M2).
6. What is not pushed does not exist (L1).
7. We have to be able to explain every method in the notebooks ourselves in the video.

---

## 8. Proposal for slides and video

Criterion 6 asks for the reflection in the slides and the video. One example per person that
shows where AI did not work and how the error was found:

| Who | Example | Why it works well in the video |
|---|---|---|
| Metehan | M1, the missing metering tariff | shows plausible but wrong data and the sum check as the remedy |
| Lenny | L7, the wrong assumption in the joined table | shows how an error spreads through documents and data and is clarified at the primary source |
| Subraj | S5, the placeholder tariffs that passed every check | shows that even a good check has blind spots and only an independent calculation helps |

---

## Individual documents

- `ai-doku/AI-Documentation_DataCollection_Metehan.md`
- `ai-doku/AI-Documentation_SQLite_Metehan.md`
- `ai-doku/AI-Documentation_PostgreSQL_Metehan.md`
- `ai-doku/AI-Documentation_Presentation_Metehan.md`
- `ai-doku/ai_dokumentation_lenny.md`
- `ai-doku/ai_dokumentation_subraj.md`
