# AI documentation – Subraj

Data Analytics, ZHAW, HS2026. Part of mandatory requirement 8.

> Draft compiled by Claude from the course of the working sessions. Subraj checks it and
> adds his own impressions before it goes into the bundled documentation. The AI reflection
> is also required in the slides and in the video (criterion 6 of the video assessment).

---

## Tools used

| Tool | Used for |
|---|---|
| Claude (Anthropic), in the Claude app with a cloud workspace | Understanding the assignment, choice of topic, research question, checking the project plan, code and interpretation of notebooks 03 and 04, translation into English |

---

## Session log

### 10 October 2026 – Assignment and choice of topic

- The AI summarised the assignment on Moodle and pointed out three open issues: the
  missing submission date for the final project, the unclear deadline for the concept PDF
  and the relationship between SQLite (mandatory) and PostgreSQL (bonus).
- It proposed several topics and checked which ones allow all six bonus points. Among them
  was the later topic «Electricity prices of Swiss municipalities».
- In the first list of topics, the AI did not check whether the data would be collected by
  web scraping or a web API. Several proposals would have meant downloading a ready-made
  dataset, which is not allowed as the main source. Only when asked did it name this as a
  risk and propose new topics.

### 25 October 2026 – Research question and project plan

- The AI formulated a main question with five sub-questions and assigned a method to each
  sub-question. The comparison over time (2021, 2024, 2027) makes the question more than a
  pure prediction, as mandatory requirement 5 demands.
- When proofreading the project plan it found four errors, among them:
  - a wrong statement about the number of grid operators
  - a t-test that does not count for bonus point 4
  - the municipal mergers, which distort a join over several years
- The AI wanted to start the EDA notebook immediately with invented test data. I stopped
  this, because the real data from Metehan and Lenny were still missing.

### 8 November 2026 – Notebook 03: EDA and tests

- The AI read the repository, including the project guide and the integration
  documentation, and built and ran the notebook on the real data.
- **Did not work:** `pip install` did not work in the AI's cloud workspace. Jupyter and
  statsmodels were not available. The AI therefore ran the notebook with a script of its
  own and wrote the outputs into the `.ipynb`.
- **Did not work:** The Alexander-Govern test (ANOVA without the assumption of equal
  variances) returned `NaN` for the cantons. Cause: in Basel-Stadt and Obwalden all
  municipalities have the same price. The first attempt at a fix (groups with a standard
  deviation above zero) failed because of rounding errors. Only a test on the range of the
  values solved it.
- **Did not work:** In two charts, the legend and labels covered the title or data points.
  This was only noticed when the AI looked at the generated images, not while writing the
  code.
- **Helpful:** The AI computed every test at municipality level and at grid operator level.
  This revealed findings that arise only from the large grid operators, for example the
  lower price of dense municipalities in 2021.

### 17 November 2026 – Cross-check with the repository and notebook 04

- The AI compared the new state of the repository with that of 8 November. It checked
  that Lenny's changes to the joined table do not change any values but only add columns.
  It took over his note on the data years of the municipal characteristics (2016 to 2019)
  into notebook 03.
- **Did not work:** statsmodels still could not be installed. The AI therefore programmed
  the standard errors clustered by grid operator itself, with the formula in the notebook.
  It checked the coefficients against scikit-learn (identical). The cross-check of the
  standard errors against statsmodels is in the notebook, but only runs on a computer where
  statsmodels is installed. **Still open: run locally and check that the cross-check
  passes.**
- **Did not work:** The AI could not push to the GitHub repository because no GitHub
  account was connected to it. The files were uploaded by hand.
- **Helpful, but only through checking:** When proofreading its own interpretation, the AI
  found three statements that were stronger than the numbers. The most important: it had
  written that the change in the relationship between density and price also holds at
  operator level. There, however, the p-value was 0.059.
- **Helpful:** The AI suggested grouping the cross-validation by grid operator instead of
  splitting at random. With random folds the model looked good (R² up to 0.29), with
  grouped folds it was worse than the mean. Without this comparison we would have clearly
  overestimated the model quality.

### 21 November 2026 – Cross-check with the project plan and the raw data

- **Did not work:** The cross-check with the project plan showed that the AI had missed
  part of sub-question 2 in notebook 03: the correlation with the size of the grid
  operator. It was included in the model (notebook 04), but was missing as a correlation
  with a p-value. Added as section 8.6. At municipality level it is the strongest
  relationship in the project (rho up to 0.44). Two sentences that previously said «at
  most 0.28» had to be made more precise.
- **Did not work:** The new text first said that the relationship with the 2024 price
  misses the Bonferroni threshold. The AI had used the threshold from section 8.5
  (25 tests) instead of the one from 8.6 (5 tests). Corrected during proofreading.
- **Helpful:** While checking the repository, the AI found seven municipalities whose
  2021 tariffs at two grid operators contain placeholder rows with an energy and grid usage
  (German: «Netznutzung») price of zero. Averaging over the tariff rows roughly halves their 2021 price, which is
  also visible on the map. Re-running notebooks 03 and 04 without these rows changed no
  conclusion. The clean-up belongs in notebooks 01 and 02 and is still open.
- **Did not work:** The push to the group repository failed twice, first because of
  missing write permissions, then because the Claude app for GitHub was not installed on
  the repository.

### 23 to 26 November 2026 – Review by Lenny's AI, chi-squared test, translation

- **Did not work:** Lenny's AI found two cells in notebook 03 (correlation of the prices
  between the years and the heatmap of characteristics against prices) that reported only
  the correlation coefficient without a p-value. Bonus point 4 requires a p-value for each
  test. My AI had not noticed this in its own checks. Both cells now show the p-values,
  the heatmap with a Bonferroni threshold over 25 tests.
- **Helpful:** At the group's request, the AI added a chi-squared test of independence
  between the k-means clusters and the municipality typology (German:
  «Gemeindetypologie») of the Federal Statistical Office (FSO) to notebook 04
  (Cramér's V 0.45). It first pointed out that bonus point 4 is already met through ANOVA
  and correlation, because the requirement says «or». It then re-ran the whole notebook
  and checked that all earlier outputs stayed the same.
- **Did not work:** Before the translation into English, the AI's workspace was reset and
  its own build scripts for the notebooks were lost. The translation therefore had to be
  done directly in the notebooks, followed by a full re-run.
- **Helpful:** For the translation, the AI followed the team glossary (`glossar.md`):
  column names, variable names and file names stay unchanged, only text is translated.
  After the re-run it compared every number in the outputs with the German version
  (identical) and looked at all charts.

---

## What worked well

- Turning the assignment into concrete work steps and checking which points a topic
  allows at all.
- Recognising methodological pitfalls that did not come up in class: dependent
  observations within a grid operator, weighting of municipalities versus operators,
  cross-validation with groups.
- Writing code that runs straight away, including checks with `assert` that immediately
  show errors when joining the data.

## What was tedious or did not work

- The AI works in its own environment without internet access for packages. It cannot
  test anything that is not installed there.
- It tends to start straight away, even when the basis is still missing (test data
  instead of real data).
- Its interpretations sound certain, even where the numbers do not support that. Every
  statement with a number has to be checked against the output in the notebook.
- It only checks charts when it actually looks at the images.
- Its own checks are not complete: a second AI reviewing the same files found gaps that it
  had missed.

## What I take away from this

AI is a tool and does not replace understanding. For the presentation I have to be able
to explain every method in notebooks 03 and 04 myself: why clustered standard errors, why
the increase model tests the change, and why R² is negative with grouped cross-validation.
