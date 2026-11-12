# Changelog

Each release lists what changed for a visitor to the page, and whether any change can move a number in a result.

## 0.2.0 (2026-11-12)

**Numbers.** One change can move a number. In 0.1.0, a run made after changing an answer in steps 2 to 6 (the columns, the date format, the species, the records left out, or the age groups) analyzed the data prepared from the earlier answers. The page now asks to prepare the data again, so such a run uses the answers shown on the page. A run with unchanged answers gives the same results as in 0.1.0. mLOS moves from 0.5.0 to 0.5.1, which adds the plot titles and changes no number: on the Irvine workbook run of 2026-11-11, every number in `results.json` agreed with the 0.5.0 run.

**Opening and wording.**

- The page opens with the title "How long do animals stay in your shelter?" and four example questions the results answer. The programs behind the page, and what it leaves out of mLOS, are in a section for analysts that folds open.
- Steps 1 to 3, and the messages the page writes, call the visitor's spreadsheet "your shelter's records" and "your file". Each column in step 2 has a short line saying what it holds.
- Step 7 says that its fixed rules are the same for every file.

**Results.**

- Each plot is captioned with its file name and the title mLOS draws on it, and offers its picture and, where mLOS writes one, the CSV of its numbers for download.
- The plots shown first are the overall length-of-stay and in-care tenure curves, which carry their statistics on the plot, followed by the plots that answer the four example questions: eight plots with an animal group, seven without.
- Choosing which plots to show no longer marks the results out of date.

**Buttons.** Each button that starts work shows a turning ring and a label saying what it is doing until the work ends, and the work starts even when the tab is out of sight.

**Email to the mLOS team (step 11).**

- The step is open from the start and asks the visitor for comments, which fill a `comments:` line at the end of the email.
- Before a run, the email holds what the page knows so far, including how far the visitor got (`stage`) and, once the data is prepared, `prepared_rows`.
- After a run, every line of the summary describes that run, even when answers change afterward.
- `summary_format` moves from 1 to 3. A program that reads the emails needs the keys `comments`, `stage`, and `prepared_rows`.

**Fixes.**

- A ShelterDataPrep configuration that runs as written, one edited after the page wrote it or prepared by hand, failed on every CSV file before reading any data. It now prepares the file.
- Results of a run during which an answer in steps 2 to 6 changed are marked out of date when they appear.

**Citation.** `CITATION.cff` and the README record the concept DOI, 10.5281/zenodo.24124646, which resolves to the newest release.

## 0.1.0 (2026-11-11)

The first release, archived at Zenodo.
