# Changelog

Each release lists what changed for a visitor to the page, and whether any change can move a number in a result.

## Unreleased

**Numbers.** Three changes can move a number. Step 3 lists columns with up to 100 values, rather than 20, as ways to compare animals, and ticks the size column to start with. For a file whose size column has 21 to 100 values and that has no date of birth, a run with the starting answers compares animals by size, where it compared no animal groups before. The page reads a two-digit year from 69 to 99 as 1969 to 1999, as ShelterDataPrep does, where it read 2069 to 2099. For a file in the month/day/two-digit year format with intake or outcome dates before 2000, the window that step 5 starts with changes, and with it the results of a run that keeps that window. Step 4 reads dates that carry a time. For a file in which some dates carry a time, the dates read change, and with them the stays prepared; a file whose dates carry no time is read as before. A run with the same answers otherwise gives the same results. ShelterDataPrep moves from 0.5.1 to 0.5.2, which adds a format for each date column; its changelog states that no numbers move for a configuration without one.

**Step 3, choosing the animals.**

- "Ways to compare animals" lists the columns with 2 to 100 values. Step 8 still merges the chosen column's values into at most six groups.
- The species list and the values of a column of records that are not shelter stays list up to 100 values, most frequent first, for a column with any number of values. A line under the list gives the number of rarer values, their rows, and their share of the rows; they cannot be chosen. When the listed values cover less than 90% of the rows, the page says the column is not well suited for categories.

**Step 4, the date format.**

- A date with a time beside it, such as 1/31/2024 14:30, 1/31/2024 0:00:00, or 1/31/24 2:30 PM, is read, and the time is left out. Before, the page read no such date, and a file written this way could not be prepared. A year-month-day date with a time was already read.
- The date columns need not be written alike: intake and outcome dates may carry a time beside a date of birth that carries none. The page finds how each column writes its time, and the configuration gives a column that differs its own line under `date_format_override`.
- The list shows the formats that read at least one date, the one that reads the most first, each with a date from the file as its example. Before, it showed all four formats, with fixed examples.
- When no format reads any date, the page says so, shows up to three of the file's dates, and prepares nothing.

**Fixes.**

- "Write the email" in step 11 no longer raises the warning about leaving the page with files not downloaded. Opening an email leaves the page where it is.
- A column whose name has two spaces in a row, or a line break, can be chosen in steps 2 and 3. Before, the page looked for the name with single spaces, found no such column, and the preparation stopped. No numbers move.
- Dates before 2000 written with a two-digit year, such as a date of birth of 6/15/98, are no longer reported in step 5 as dates after today.
- When ShelterDataPrep stops, the page shows its whole message, under the visitor's own file name. A message of several lines, such as the one naming a column the file lacks and listing the columns it has, was cut to its first line. The messages for a workbook, a configuration, or a settings file that cannot be read are whole in the same way. No numbers move.
- "Prepare the data" names each required piece of information that has no column chosen in step 2 (animal ID, intake date, outcome date, intake type, or outcome type) and prepares nothing until each has one. Before, ShelterDataPrep started and stopped with a message about a column the file lacks. No numbers move.
- Results of a run during which the data was prepared again are marked out of date when they appear, and are saved with the configuration and the prepared data they were made from. They were shown as current, and saved with the newer configuration and data. No numbers move.
- "Download everything" names its zip, and the file named in its README, after the file the run was made from. After another file was loaded, they carried that file's name. No numbers move.
- A step that waits on an earlier one takes no keyboard input, as it already took no click. The Tab key reached its buttons, and pressing one, such as "Run mLOS" before any data was prepared, failed without a message. A screen reader passes over a waiting step until it opens. No numbers move.
- When the page, Python, or R cannot start, or a file of the page cannot be loaded, the page says so and asks for a reload. The line under the title kept saying that Python and R were starting, and "Prepare the data" and "Run mLOS" kept turning without end. No numbers move.
- The results of the last run stay on the page when "Run mLOS" is pressed with an answer of step 8 still to fix, and come back, marked out of date, when a run stops. They were cleared in both cases, while "Download everything" still held them. No numbers move.
- The page's footer reads "mLOSweb X.Y.Z plus unreleased changes" when the page carries changes made after release X.Y.Z, those this file lists under "Unreleased". It read as the release itself. No numbers move.
- An age group or a carried column whose name YAML reads as something other than text, such as NO, ON, TRUE, or 1_2, is written to the configuration in quotes, so ShelterDataPrep reads the name as typed. No numbers move for other names.
- Each run of mLOS frees the memory the run before it held in the tab: its folder of results and the plots and download links made from it. A run that stops frees its own folder. Before, every run's results stayed in memory until the tab closed. No numbers move.

**Wording of steps 4 to 11.** The help text and messages of steps 4 to 11 use plain words, as steps 1 to 3 do. A technical term stays where it names something in the files: in parentheses, or in a section for analysts. No numbers move.

- Step 4 says why the format matters: 3/4/2024 is March 4 in one file and April 3 in another. When no format reads every date, the message says that step 7's table gives the number of dates not read in each date column.
- Step 5 has a short line under "First day" and under "Stop date" saying what each is. The messages about a file cut by date say first what the file seems to hold or to lack, and name the cut in parentheses.
- Step 6 says how an animal is placed in an age group, and that a file with no date-of-birth column gets no age groups.
- Step 7 says what preparing the data does and that the answers are saved in one file, the ShelterDataPrep configuration. The source of the fixed rules is named under "Show the configuration file". When the preparation stops, the message says so before giving ShelterDataPrep's own message.
- Step 8 calls the values of the outcome and intake columns "outcome types" and "intake types", as step 2 does, where it said "labels". The horizon is labeled "Horizon (days)", and the help text defines it before naming `restricted_stay_cap`. The help text on reference groups says what a reference group is and how to read a hazard ratio. Each menu and number box has a short line under its label.
- The button of step 8 reads "Run the analysis", where it read "Run mLOS"; the banner above it, the tab's title during a run, and the messages of steps 8, 10, and 11 say "the analysis". When the analysis stops, the message says so before giving mLOS's own message.
- The checks shown with the results say "the animals in care" where they said "the residents", and name the mLOS User Guide in full.
- Step 9 says what it makes, a slide deck and a workbook of tables; the deck builder, `mlos_review`, and its command are in a section for analysts that folds open. The line under the tables says what the marks H, L, and F stand for.
- Step 10 says that the two files at the top of the zip record the answers and can be loaded in step 1 on a later visit.
- Step 11 is headed "Send your comments and a summary of your study to the mLOS team" and speaks of "the mLOS team" where it said "us" and "we". In the email, the line above `comments:` ends "They help the mLOS team improve the page."; the keys are the same, and `summary_format` stays 4.

**Email to the mLOS team (step 11).** The summary names the version of the page, as the footer does, on an `mlosweb_version:` line that takes the place of `site_commit:`. `summary_format` is 4. No numbers move.

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
