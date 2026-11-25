# AI documentation – Lenny Frei

Data Analytics, ZHAW, autumn semester 2026. Part of mandatory requirement 8.

This document is updated **continuously**, at the end of every working session. It
records which AI tools were used for which tasks, which advantages and disadvantages
showed up along the way and – above all – **where something did not work with the
help of AI**.

That last point is the most important one. It cannot be reconstructed at the end,
because you forget the failures as soon as the result is right.

> Note for the submission: the AI reflection is required twice. Once as documentation
> (mandatory requirement 8) and once **in the slides and in the video** (criterion 6
> of the video assessment). This document is the basis for both.

---

## Tools used

| Tool | Used for |
|---|---|
| Claude Code (Claude Opus 5) in VS Code | setting up the environment, checking the data, correcting the project instructions, recomputing figures |
| Claude Code in a cloud session | one intermediate step on 27/28 October 2026, result lost (see below) |
| a further, external AI review | review of the project, produced the finding about the grid operator level |

---

## Session log

### 27 October 2026 – setup and first check of the data

- Environment checked: Python 3.11.4, git 2.50.1, pip present.
- Repository cloned, virtual environment `.venv` created, seven packages installed
  (pandas, matplotlib, jupyter, requests, openpyxl, geopandas, folium),
  `requirements.txt` written by hand instead of with `pip freeze`, so that it holds
  only the seven packages actually needed and not 120 helper packages.
- The AI read the project instructions `CLAUDE Data Analytics.md` and found **five
  contradictions** that I had not noticed myself: a missing section 12, the
  contradiction between "Codespaces only" and a local installation, an outdated
  column list, a mandatory point 9 handed out twice, and a guessed claim about an
  allegedly wrong submission deadline.
- Recomputed whether `energie + netznutzung + abgaben + netzzuschlag + messtarif`
  adds up to the total price. Result: yes, in all three years, largest deviation
  0.001 centimes. That explained the previously unresolved gap of 1.675 centimes in
  the 2027 data: it was the metering tariff, reported separately from 2026 onwards.

### 30 October 2026 – comparison against the original and a methodological reservation

- The Moodle page with the assignment existed only as an image (3,298 × 21,546
  pixels, no text layer). The AI cut the image into strips and read it.
- Comparing our requirements checklist against the original: **eight deviations**, all
  of them caused by me, because I had condensed the Moodle page too aggressively. The
  most important ones: mandatory requirement 2 was missing "resolving
  inconsistencies" – that is my own task. And the video assessment consists of seven
  criteria, not of one line about the length; one of them requires the AI reflection
  in the slides and in the video.
- In the process, **an error on the Moodle page itself** came to light: the
  submission of the final project carries 10 January 2027 in its title, but
  11 January 2026 in the due-date field. To be raised with the lecturers.
- The group's reference values (means, shares of dispersion, 2,087 common
  municipalities) were recomputed against the CSV files and confirmed. The missing
  row for the grid surcharge was added; without it one column only reached 99.2 per
  cent instead of 100 per cent.
- New section 5b on the methodological reservation at the operator level (see below).

### 1 November 2026 – second data source, join, and a comparison of code against documentation

- The FSO source was checked **before** downloading it: the AI first read out the
  metadata attachment and showed the list of indicators. That revealed that the
  municipality typology and the language region are **not** contained, and that the
  indicators come from different years, from 2016 to 2019. Two indicators with
  reference period 2004/2009 were excluded as a result.
- The geodata from the course repository was checked before being used: it covers
  only the canton of Zurich. See case 6 below.
- Join built: Regional portraits 2021 pivoted into wide format, joined with the price
  data on the FSO municipality number. **Match rate 100 per cent**, no record lost.
- While checking the missing values it emerged that the originally planned
  characteristic «workplaces» is missing for 269 municipalities, while «jobs» is
  missing for only 88, at a correlation of 0.986. The swap brought 181 municipalities
  back into the model.
- Notebook `scripts/01_daten_bfs_lenny.ipynb` created and executed, documentation for
  mandatory requirement 2 written.
- One of my own figures corrected: the share of municipalities dropping out had been
  stated verbally as «a good 17 per cent»; that applied to the old choice of
  characteristics. The correct figure is **a good 9 per cent**.
- On the same day it came out that a rule about the metering tariff, in force since
  27 October, had it the wrong way round. It was already built into the delivered
  CSV. See case 7. Sections 4 and 5 of the project instructions, the notebook, the
  integration documentation and the table were all corrected.

### 7 November 2026 – repair after a rearrangement of the folder structure

- Metehan's AI had sorted the files into subfolders (`daten/strompreise/`,
  `daten/bfs/`, `daten/verbunden/`, `scripts/`, `sql/`, `ai-doku/`) without updating
  the paths in the notebooks. Both notebooks were broken as a result. See case 8.
- Both notebooks were given an anchor to the repository root, `finde_wurzel`, and
  derive all paths from it. Tested from three working directories.
- `scripts/strompreise_holen.py`: output path and file names aligned, `fillna(0.0)`
  removed from the saved DataFrame. It now applies only inside the sum check.
- Notebooks renamed according to the order of the work:
  `01_daten_bfs_lenny.ipynb`, `02_sqlite_metehan.ipynb`.
- While preparing the map it came out that the project instructions had described the
  second data source wrongly. See case 9.

**Second session on the same day:** third source built in. «Die Raumgliederungen der
Schweiz 2019» supplies canton, language region and municipality typology in a single
file. Four municipalities were missing there, because its territorial status is 2019;
they were resolved mechanically through the changes table of the historicized commune
register, not by hand. For three of the four, all predecessors agreed; for Prez (2237)
they did not agree on the typology – nothing was entered there, instead of guessing.
See case 10.

**Third session, maps (bonus 3):** the licence of swissBOUNDARIES3D was clarified
before the data was fetched – the STAC catalogue lists «proprietary», while
swisstopo's terms of use permit use and modification with attribution. Coverage was
checked rather than assumed: all 2,087 municipalities are contained in edition
2026-01. Two maps built, each as a PNG and interactive. The change map had to be
corrected after the first run, see case 11. Measured: the grid operator explains 94 to
97 per cent of the price dispersion, the canton 23 to 60, the language region 0.4 to
3.0.

---

## Where something did not work with the help of AI

### 1. An entire working session in the cloud was lost (27/28 October 2026)

Between the two local sessions I carried on working in a cloud session. Around four
commits and eight files were created there, among them `punkteliste.md`,
`folien_entwurf_lenny.md`, `ai_dokumentation_lenny.md` and a first draft of the
notebook.

**None of it exists any more.** The cloud environment was not signed in to GitHub as
me and therefore could not push. The container was deleted afterwards. On 30 October I
had the entire user folder searched: not one of these files is present on my machine.
`git log origin/main..HEAD` showed zero local commits, the local state and GitHub were
identical.

**Lesson:** work that has not been pushed does not exist. A cloud session cannot see
your own machine and must be able to write its result into the repository itself.
Before starting a cloud session, check that it has write access.

**Cost:** around two hours that had to be done again.

### 2. One AI delivered figures that another AI could not reproduce (30 October 2026)

An external AI review delivered the – substantively correct and important – finding
that electricity prices are set per grid operator, not per municipality. It came with
concrete figures: 544, 504 and 481 grid operators in the three years.

Recomputing them, Claude arrived at 512, 496 and 485. **Eight different ways of
computing** were tried – four attribution rules for municipalities with several
operators, each over two base populations. None produced the delivered figures. Claude
said so, instead of adopting the figures or inventing an explanation.

The resolution: for municipalities with several grid operators, the first AI had taken
whichever one **happens to come first** in the CSV file. That result depends on the row
order and changes as soon as Metehan runs the SPARQL query again. The figures were
therefore not wrong in the sense of implausible, but they were not reproducible.

The document now holds the recomputed figures with the documented rule "the operator
with the smallest `netzbetreiber_id`". The statement itself remained unchanged:
between 95.6 and 98.0 per cent of the price dispersion lies between the operators, and
the effective number of cases is around 500 instead of 2,087.

**Lesson:** a figure without a documented method is not a figure. That the error was
noticed at all was due solely to a second AI wanting to recompute it and failing.
Plausible-looking figures are the most dangerous result, because nobody questions them.

### 3. A file that was not what its name said (27 October 2026)

I had put a file `pdf24_zusammengefügt.pdf` into the repository folder as a "summary of
all the data". The AI checked it before it was used: 1,795 pages, 309 MB, and in
substance not a data summary at all but lecture slides, exercise sheets – and **three
scanned, marked exams carrying the names, matriculation numbers and grades of three
students who are not us**.

Our repository is public. The file was removed from the repository folder and
additionally secured through `.gitignore`. It was never committed at any point.

**Lesson:** before committing, check what is really inside a file, especially with
merged PDFs and in a public repository.

### 4. Outdated material from a fellow student (30 October 2026)

A file passed on as a "summary" by a fellow student turned out to be the official
course material of **autumn semester 2024**. The AI compared it against the current
module description and found four places where the rules have changed since, among
them the grade weighting (70/30 instead of 60/40) and the obligation to hand in ten
weekly exercises, which no longer exist in autumn semester 2026.

A second file from the same student consisted only of images without a text layer and
was unreadable without OCR.

**Lesson:** material from earlier cohorts is good for the subject matter, not for the
rules. Only the current module description on Moodle is binding.

### 5. Limits the AI stated itself

Several times the AI said that it did not know something, instead of guessing:

- The list of 22 points could not be checked at first, because the source was only a
  screenshot on Moodle. The AI marked it as unverified instead of confirming it. Only
  with the exported PDF did the comparison become possible – and it then produced
  eight deviations.
- The appointment "8 December, 11:00, SW301" could not be confirmed from the Moodle
  page, because the page says the dates are only fixed after the group registration.
- On the question of how to activate the cloud credit, the AI said it did not know the
  exact command, instead of inventing one.

### 6. Documentation and code drifted apart (1 November 2026)

Comparing the project instructions against Metehan's collection script brought out
**three places** where the documentation says something different from the code. All
three come from statements that nobody had checked against the source.

**a) Wrong endpoint addresses.** The instructions named
`https://lindas.admin.ch/query` and `https://lindas.admin.ch/elcom/electricityprice`.
The script has `https://ld.admin.ch/query` and
`https://energy.ld.admin.ch/elcom/electricityprice`. Anyone trying the addresses from
our documentation would have come up empty.

**b) A claim about geodata that the AI had invented itself.** On 27 October the AI had
written into the instructions that usable municipal boundaries were lying in
Dr Gellrich's course repository. The basis for that was a note on Moodle, **not** a
look into the files. On 30 October someone looked: the KML file contains 166
municipalities with FSO numbers between 0 and 298, that is, only the canton of Zurich.
The claim stood unchallenged in the project instructions for four days.

**c) A limitation that was wrong.** The instructions and the planned report said that
the fixed costs were left out and that the analysis underestimates the costs for
municipalities with a high basic fee. The comment in the script said the opposite: the
fixed costs are already inside the grid usage charge. Clarified on the same day
against ElCom's guidance on tariff declaration 2026: basic and capacity prices are
converted into centimes per kWh, so the centime figures already contain the basic
fees. The script comment is right, the limitation was wrong and was deleted.

**A fourth contradiction, found in the same comparison:** section 4 of the
instructions assumed that the metering tariff did not exist before 2026. The script
said it had previously been contained in the grid usage charge. The direction of a
correction of 1.67 centimes depended on this. This point too was clarified on the same
day and turned out to be the most consequential of them all – see case 7.

**Lesson:** project instructions age against the code, and they do it unnoticed. Both
were written by humans and AI together, but never read against each other. That the
errors were noticed was due solely to an explicit line-by-line comparison. Whoever
writes documentation must check it against the source, not against their memory.

Case b is worth noting: here the AI did not adopt somebody else's statement, it put up
a plausible claim of its own without checking it – and then refuted it itself four days
later.

### 7. A wrong assumption was already built into the data (27 October to 1 November 2026)

This is the most instructive case so far, because the error was not in a text but **in
a file that was due to go to two team members**.

**The assumption.** On 27 October the AI recorded: the metering tariff is a new price
component from 2026 onwards which did not exist in 2021 and 2024, and is therefore to
be left out of the comparison over time. The observation behind it was correct: the
field `messtarif` is empty in 2021 and 2024 and filled in every row in 2027. The
conclusion drawn from it was plausible – and wrong.

**How far it had spread.** By 1 November the rule stood
- in section 4 of the project instructions,
- behind the figures in section 5 (mean for 2027, net increase, share of
  municipalities below the 2021 level),
- as three columns of their own, `vergleichbar_*`, in
  `daten/verbunden/strompreise_gemeinden.csv`,
- and in an explicit recommendation to Subraj to use precisely those columns for
  comparisons over time.

**How it was exposed.** Not by thinking it through, but by a comparison: while reading
Metehan's collection script, the comment «Erst ab 2026 separat ausgewiesen, vorher in
der Netznutzung enthalten» turned up – reported separately only from 2026, previously
contained in the grid usage charge. That contradicted the project instructions
directly. The AI reported the contradiction instead of picking a side, and marked both
versions as unresolved.

**How it was settled.** At the primary source. ElCom writes about the 2026 tariffs,
verbatim: «Der Messtarif wird neu separat ausgewiesen. Er war bislang im
Netznutzungstarif integriert.» That made the direction unambiguous: the metering costs
existed before as well, they were simply inside the grid usage charge.

**What would have been wrong.** Comparing 2027 without metering costs against 2021
with metering costs. That would have made 2027 about 1.67 centimes too cheap and would
have understated the price rise:

| | before | correct |
|---|---|---|
| Mean 2027 | 25.58 cts. | 27.25 cts. |
| Net 2021 to 2027 | +4.72 cts. | +6.39 cts. |
| Municipalities below the 2021 level | 14.5 % | 10.9 % |

**Lesson:** an assumption that has once been built into the data spreads. It did not
only stand in a document that can be corrected, it was already in a CSV file due to go
to two team members, together with the recommendation to use it. Anyone who had used
the file would have inherited the error without being able to see it.

Two things worked here: that the contradiction was **reported** instead of resolved,
and that the clarification happened at the **primary source** and not at the most
plausible explanation. The three affected columns were removed and not merely renamed
– a column nobody is supposed to use will sooner or later be used.

### 8. An AI tidied up and silently destroyed both notebooks in the process (7 November 2026)

Metehan's AI rearranged the folder structure and sorted the files neatly into
subfolders. The sorting itself was good. Only the paths in the notebooks were not
updated.

After that **both** notebooks aborted with `FileNotFoundError` on a fresh clone, and
did so from every working directory: from `scripts/`, `daten/bfs/...` was looked for
under `scripts/daten/bfs/...`; from the root, Metehan's notebook no longer found the
price files, because by then they were one level deeper.

**Why nobody noticed:** the outputs in the notebooks still came from before the
rearrangement and had been checked in with them. Anyone opening the files on GitHub
saw complete tables, figures and results. It looked correct. It was broken only when
you ran it – and nobody had run it since the rearrangement.

**Lesson:** an AI that changes a structure does not check by itself whether the code
still runs afterwards. Embedded outputs in a notebook are no proof that it still works
today; they are a photograph of yesterday.

The rule now stands in the README and in section 10 of the project instructions:
whoever moves files updates the paths in both notebooks and in the collection script
and lets both notebooks run through once completely.

### 9. A data source described without looking at it (27 October to 7 November 2026)

Section 2 of the project instructions said the FSO Regional portraits contained
population, area, density, **municipality typology, canton and language region**. The
last three are not true. The raw file has eight columns – `PERIOD_REF`, `PERIOD_COMP`,
`CODE_REGION`, `REGION`, `INDICATORS`, `UNIT_MES`, `VALUE`, `STATUS` – and none of
them is among the 41 indicators. The ElCom data does not contain them either.

It was noticed only on 7 November, while preparing the map. **A week** lay between the
wrong description and the discovery.

**Consequence:** sub-question 1 of the research question, the differences between
cantons and language regions, and the ANOVA that goes with it (bonus 4) cannot be
computed with the current data. A third data source is needed. Subraj is just starting
the analysis and would have run into exactly that wall.

**Lesson:** the description of a data source that comes from an AI and was never
checked against the file is a guess, not a fact. It reads like a fact, though, because
it sounds plausible and concrete. While working with the data it did not show up,
because we had used exactly those characteristics that really are present.

This is the same type of error as case 7, only with the sign reversed: there, an
unverified assumption stood in the data; here, an unverified claim stood about the
data.

### 10. Two cases in which checking before building paid off (7 November 2026)

This time nothing went wrong, and that is exactly what makes it worth documenting:
both times a check prevented an error that would otherwise have travelled into the
report.

**a) A source opened before downloading it.** Before building in the third source, the
file was loaded into a staging folder and its columns were read, instead of relying on
the description on the information page. Only that made it clear that it supplies
canton, language area **and** municipality typology at once – three characteristics
from one file instead of from three. After case 9, that was the direct consequence.

**b) A plausibility check that looked wrong at first.** Around three quarters
German-speaking municipalities were expected, 65.4 per cent came out. Instead of
accepting the figure or «correcting» it, it was computed against all 2,212 Swiss
municipalities: there it is 64.2 per cent. Our selection therefore matches Switzerland
as a whole; the expectation came from the **share of population**, not from the number
of municipalities. Confusing the two would have been an error in the report, and one
that could not have been explained away in the video.

**Lesson:** a figure that deviates from expectation is not automatically wrong. Only
the comparison with an independent base population shows whether the data or the
expectation is off.

### 11. A map that failed at its own job (7 November 2026)

The second map was supposed to show which municipalities are cheaper again in 2027
than in 2021 – according to section 5 that is 10.9 per cent. The first draft used a
symmetric colour scale around zero, which is the textbook solution for a diverging
display.

The result was unusable. The change ranges from −2.1 to +27.7 centimes. A scale from
−27.7 to +27.7 pushes all the negative values into a barely visible pale blue. The 227
municipalities the map was about were practically impossible to find on it. That same
map could have gone into the presentation like that, with a caption promising
something the picture does not show.

It was noticed only because the finished PNG file was **looked at**. The figures in the
output were correct, the notebook ran through without errors, and the colour scale was
chosen correctly by the textbook. No automated test would have found this.

Corrected with a scale whose zero point lies at the centre of the colours but whose
arms are of different length. The price for that is documented: equally strong blue and
red do not mean equally many centimes.

**Lesson:** with a graphic, no check replaces looking at it. A figure can be
recomputed, a picture has to be looked at – and it has to be the finished picture, not
the code that produces it.

### 12. An audit of my own part, and what it turned up (8 November 2026)

Before the submission, my part was checked completely against the assignment and
against the raw data, with the explicit condition that no figure from our own
documentation be taken as given. Four findings that would otherwise have travelled
into the report:

**a) A piece of evidence that did not exist.** Since 1 November, section 3 of the
project instructions had claimed that the basic fees are inside the centime price, and
named an ElCom address as the source. When checked, it returned **404**. In total six
checked ElCom addresses were dead – ElCom had moved its website to `/dam/de/sd-web/`.
The statement is correct, as the guidance for the 2027 tariffs that was eventually
found shows on page 10, but for ten days the document carried a piece of evidence that
nobody had opened. The section was marked «Clarified on 1 November 2026» while it did.

**b) A claim the test did not support.** The integration documentation said the
excluded municipalities were «clearly smaller and somewhat more expensive». A
permutation test with 20,000 draws shows: smaller yes, clearly established (p = 0.007
and p = 0.0003). More expensive no – among the merged municipalities the median is
indeed higher, but the mean is practically the same (20.83 against 20.86 centimes,
p = 0.91), and in the second group not even the median holds up (p = 0.25). The
statement rested on a comparison of three medians without a test.

**c) A table that could not be computed with.** Sub-question 1 asks which price
component accounts for the differences. The delivered table contained only `total`.
Subraj would have had to aggregate the components out of the raw data himself – and
would very probably have walked into the same metering-tariff trap as we did in
October. The same applied to the «size of the grid operator» from sub-question 2.

**d) Scattered time levels.** A single row of the table holds five territorial
statuses and six data years. That was documented in six places across four files, and
nowhere summarised. Nobody reading it would have seen that we explain prices from 2021
to 2027 with municipality characteristics from 2016 to 2019.

**Lesson:** documentation does not check itself. All four findings arose in documents
written with AI and read several times beforehand – and all four came to light only
when somebody checked deliberately against the primary source and against the raw
data instead of against their own text. The most treacherous was a): a marker such as
«Clarified on …» creates trust without anybody having clicked the link.

### 13. A version pin that made the whole project unusable (22 November 2026)

During the audit after the holidays the project was freshly cloned and set up in a
fresh virtual environment – that is, the way the lecturer will do it. The first command
failed:

```
ERROR: Ignored the following versions that require a different python version:
       1.18.1 Requires-Python >=3.12
ERROR: No matching distribution found for scipy>=1.18.1
```

While adding the new packages, `scipy>=1.18.1` had found its way into
`requirements.txt`. That version requires Python 3.12, the project runs on 3.11.4. The
pin presumably came about because a newer Python version was running on the machine
where it was created, and because `pip freeze` or an AI entered the version installed
there.

**The consequence:** a fresh clone could not be set up. It was not a notebook that
failed, it was the installation itself – before anything could even start. Two further
packages were missing entirely: `psycopg2-binary`, which is imported directly in
Metehan's PostgreSQL notebook, and `statsmodels`, which Subraj needs for a
cross-check.

**Why nobody noticed:** all three of us have a working environment on our own machine.
scipy had long been installed there, and a `pip install -r requirements.txt` would only
have reported that everything is present. The error shows up exclusively on a machine
where nothing is installed yet – that is, precisely at the lecturer's.

**Lesson:** a `requirements.txt` is only checked once it has run through **on a fresh
clone in a fresh environment**. You cannot test it on your own machine; there it is
always satisfied. The same goes for paths and for everything else that "works on my
machine".

A side finding of the same check: nowhere in the repository did it say which Python
version the project needs. It now says so in `requirements.txt` and in the README.

### 14. A suspicion that dissolved when it was checked (22 November 2026)

Before the audit, the suspicion was in the room that Subraj's model does not satisfy
mandatory requirement 6: his notebook contained neither `r2_score` nor
`mean_squared_error` nor `train_test_split`. A text search in the code confirmed that.

Checked properly, not one of the three points held. Subraj computes R², adjusted R²
and RMSE in a function he wrote himself, `ols_geclustert`, which at the same time
delivers standard errors clustered by grid operator. Instead of a single train-test
split he uses 5-fold cross-validation, additionally with folds **grouped** by grid
operator – for these data the methodologically stronger procedure, because a random
split would distribute municipalities of the same operator across both sides and
overstate the quality of fit.

**Lesson:** a search for function names checks which library somebody used, not
whether the requirement is satisfied. The absence of a familiar name is not a finding.
It takes reading the code and looking at the outputs.

This is the reverse of case 9: there, something stood in the document that was not in
the data. Here, something was in the data that was not found in the document.

---

### 15. An external dependency was silently broken (25 November 2026)

While translating the map texts, notebook 01 was run again. It reported **zero
errors** – and both interactive maps were unusable all the same.

A warning from folium stood in the outputs:

```
UserWarning: CartoDB tiles now require an API key.
Please provide one to continue using the tiles.
```

A warning is not an error. The notebook ran through, the HTML files were written, the
file sizes were right, every figure was right. Anyone looking only at the return value
sees nothing here.

Instead of merely classifying the warning, we **looked** at the map: a screenshot in
the browser showed that the block has long been active. The basemap consisted, across
its entire surface, of the words «API KEY REQUIRED». In January a marker would have
opened two maps on which Switzerland disappears under a grid of watermarks.

**The warning was not new.** A look into the tag `deutsche-fassung` showed it twice in
the stored outputs, that is, from before the translation. It had been sitting there
unnoticed, and I had overlooked it myself during the audit of 24 November: back then I
reported «0 errors, 0 cells without output» for this notebook and did not mention the
warning with a single word. What I had checked was whether the notebook *runs*, not
whether its result is *usable*.

The obvious replacement was OpenStreetMap: no key needed, one line of work. After
switching, the map was looked at again, and it was worse:

- The green and beige tiles push through the 15 per cent transparency of the areas.
  The light values, that is the municipalities without much change, therefore look
  dirty instead of white.
- On OSM the lakes are blue. But in our map blue means «became cheaper». Precisely
  those 227 municipalities, which we made visible with such effort in case 11, now sit
  next to lakes of the same blue.

Esri World Light Gray Base was therefore chosen. The service needs no key, and its own
description says what it was built for: *«This map draws attention to your thematic
content by providing a neutral background with minimal colors, labels, and features.»*
There, the lakes are grey. The attribution was taken from the service's metadata
(`copyrightText`), not formulated by us.

The repair went into the repository deliberately as a **commit of its own**, separate
from the translation. The log should keep showing what was translation and what was an
intervention in substance.

**Lesson:** «runs without errors» says nothing about the result. Warnings are dangerous
for exactly that reason, because they stop nothing – and an AI that reports the run
likes to report the success and overlooks the warning, just as I did during the audit.
The remedy is cheap: look at the result, do not just read the return value. And: take
the decision at the picture. Here the obvious replacement was the worse one, and you
would not have seen that in the line of code.

**Addendum of 25 November 2026: the same pattern a second time.** While translating the
notebook, the verification script built specifically for the job reported «all checks
green», while three German column headings had been left standing – it recognised
German *sentences*, but not individual *labels*, and those are exactly what a reader
sees first in any output. Both times it was not the result that was wrong, but **the
check that was weaker than its own report**: once a notebook that said «0 errors» and
delivered unusable maps, once a verification script that said «green» and let German
captions through. A green report proves only that the check found nothing – not that
there is nothing there.

---

## What worked well

- **Finding contradictions in our own texts.** The five errors in the project
  instructions and the eight deviations from the assignment I would not have found by
  reading through. A systematic line-by-line comparison is exactly what an AI endures
  better than a human.
- **Recomputing instead of believing.** Every figure that went into the document was
  checked against the CSV files beforehand. Among other things that revealed the
  missing grid surcharge row, without which one table column came to only 99.2 per
  cent.
- **Setting up the environment.** Virtual environment, `requirements.txt` and
  `.gitignore` were done and commented within a few minutes.
- **Opening up unreadable sources.** A screenshot 21,546 pixels high and a
  1,795-page PDF were cut up and searched mechanically.
- **A repair that could be verified (7 November 2026).** When the paths were updated,
  nothing was claimed, everything was shown: the sha256 hash of the result file before
  and after the run (identical), the control cell in Metehan's notebook with 0
  deviations across all eight columns, both notebooks executed with 0 errors from
  `scripts/`, and the anchor tested from three different working directories. A
  rearrangement of somebody else's code can be secured well enough that you do not
  have to hope.

## What was tedious

- **Loss of context between sessions.** Every new session begins without memory.
  Without the project instructions in the repository, everything would have to be
  explained again each time. That argues for recording decisions in writing in the
  repository instead of in the chat.
- **File limits.** Large PDFs and images had to be cut up before they were readable.
- **Version differences.** pandas 3.1.0 was installed, while the course slides assume
  pandas 2.x. No consequences so far, but a possible stumbling block with code
  examples from the lectures.

---

## Open points

- Metehan and Subraj keep AI notes of their own. These will be bundled by me before
  the submission (mandatory requirement 8).
- Examples 1 and 2 above belong in the slides and in the video (criterion 6).

---

*Last updated: 22 November 2026*
