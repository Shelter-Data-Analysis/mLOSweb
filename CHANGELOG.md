# Changelog

Each release lists what changed for a visitor to the page, and whether any change can move a number in a result.

## Unreleased

**Numbers.** Two changes can move a number. Step 3 lists columns with up to 100 values, rather than 20, as ways to compare animals, and ticks the size column to start with. For a file whose size column has 21 to 100 values and that has no date of birth, a run with the starting answers compares animals by size, where it compared no animal groups before. The page reads a two-digit year from 69 to 99 as 1969 to 1999, as ShelterDataPrep does, where it read 2069 to 2099. For a file in the month/day/two-digit year format with intake or outcome dates before 2000, the window that step 5 starts with changes, and with it the results of a run that keeps that window. A run with the same answers otherwise gives the same results.

**Step 3, choosing the animals.**

- "Ways to compare animals" lists the columns with 2 to 100 values. Step 8 still merges the chosen column's values into at most six groups.
- The species list and the values of a column of records that are not shelter stays list up to 100 values, most frequent first, for a column with any number of values. A line under the list gives the number of rarer values, their rows, and their share of the rows; they cannot be chosen. When the listed values cover less than 90% of the rows, the page says the column is not well suited for categories.

**Fixes.**

- "Write the email" in step 11 no longer raises the warning about leaving the page with files not downloaded. Opening an email leaves the page where it is.
- A column whose name has two spaces in a row, or a line break, can be chosen in steps 2 and 3. Before, the page looked for the name with single spaces, found no such column, and the preparation stopped. No numbers move.
- Dates before 2000 written with a two-digit year, such as a date of birth of 6/15/98, are no longer reported in step 5 as dates after today.
- When ShelterDataPrep stops, the page shows its whole message, under the visitor's own file name. A message of several lines, such as the one naming a column the file lacks and listing the columns it has, was cut to its first line. The messages for a workbook, a configuration, or a settings file that cannot be read are whole in the same way. No numbers move.
- Results of a run during which the data was prepared again are marked out of date when they appear, and are saved with the configuration and the prepared data they were made from. They were shown as current, and saved with the newer configuration and data. No numbers move.
- "Download everything" names its zip, and the file named in its README, after the file the run was made from. After another file was loaded, they carried that file's name. No numbers move.

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
