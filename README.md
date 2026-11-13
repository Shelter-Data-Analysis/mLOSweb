# mLOS Web

A web page that runs ShelterDataPrep and mLOS in the browser, for animal shelters without an R or Python installation. The shelter loads an export of its stays, as a CSV file or an Excel workbook, answers a few questions about it, and gets the mLOS plots, tables, and workbook. Each plot is captioned with its file name and, beneath it, the title mLOS draws on the figure. The plots shown first are the overall length-of-stay curve and the in-care tenure curve, which carry their summary statistics on the plot, followed by those that answer the example questions at the top of the page: length of stay by period, by intake type, and by animal group; the remaining stay and the outcome mix by days already in care; and the animals in care by days already in care, by animal group or, with none, by intake type. A list offers every other plot. A ShelterDataPrep configuration or an mLOS settings file, whether the page wrote it or it was prepared by hand, can stand in for the questions; the page lists each change it makes to such a file, such as turning off a feature the site does not run. Everything runs in the visitor's browser: the data is not uploaded anywhere. Each button that starts work, from loading a demo export to saving the zip, shows until the work ends that it is under way: it turns into a turning ring with a label saying what is being done, such as "Preparing the data...", and takes no second press. Each step offers its files for download where they appear, each plot with its picture and, where mLOS writes one, the CSV of its numbers, and a last step saves all of them in one zip; leaving the page with files made and not downloaded asks the visitor to confirm. An optional last step opens a new email to the mLOS team in the visitor's own email program, holding a summary of the run that the page shows first: how the page was used and how the study was set up (counts, dates, choices, and group names, with no results), one `key: value` per line so the replies can be read by a program. The step asks the visitor, prominently, for comments on the page; they fill the `comments:` line at the end of the summary, the one entry that may run over several lines, and a visitor can also write them in the email itself. The step is open from the start, so a visitor who stops partway can still send comments: until mLOS has run, the email holds the comments and what the page knows so far: the versions, the date, and how far the visitor got (`stage`); once an export is loaded, how it was loaded, the species, and the export's numbers of rows and columns; and once the data is prepared, the number of prepared rows. The visitor can delete any line, and chooses whether to send it.

The page opens with a plain description of the questions it answers, for readers new to length-of-stay analysis. It runs a subset of mLOS, and says so at its top, in a section for analysts that folds open: it leaves out the Weibull regression and the confidence bounds of the conditional outcome curves, compares at most four periods, six intake groups, and six animal groups drawn from one column, and builds the slide deck with its default settings. The full mLOS runs on the user's own computer, from [GitHub](https://github.com/Shelter-Data-Analysis/mLOS) or its Zenodo archive ([10.5281/zenodo.22083814](https://doi.org/10.5281/zenodo.22083814)).

The page prepares the export with ShelterDataPrep, running in Pyodide (Python compiled to WebAssembly), then analyzes it with mLOS, running in webR (R compiled to WebAssembly). A last, separate step runs mLOS's deck builder, `mlos_review`, in the same Python to write a slide deck and a workbook of its tables, and shows the tables the user picks. All three programs run unchanged. A workbook (.xlsx or .xlsm) goes to ShelterDataPrep as it is, with a `sheet:` line naming the sheet that holds the stays: the sheet whose row of column names names the most of the columns the page asks for, or the one the user picks from the list of sheets. The page reads a sheet through ShelterDataPrep's own reader, `shelterprep.read_source`, so it sees the rows and column names a run reads: the names from the first row with a value in any column, and no row without a value. The same reader repairs two things in a workbook, and the page says what it did: a heading merged across columns names the column of values under it, where the heading's own column is empty, and font families above 14, which Excel writes and openpyxl refuses, are left out of a copy it reads, with no cell value changed. A column with no name and no values, such as a spacer between columns, is left off the page; ShelterDataPrep reads only the columns its configuration names, so it never reads one either. A row with no values is left off the page as well, as ShelterDataPrep leaves it out and counts it in its statistics table. The demo exports, which the page offers in a list, are raw files in public deposits: the Irvine Animal Care Center's workbook of 2025-10-08 (figshare, 10.6084/m9.figshare.34875669.v2) and its earlier `CIall_raw.csv.gz` (Zenodo, 10.5281/zenodo.22051091). An export with no size or date-of-birth column, such as `CIall_raw.csv.gz`, gets a configuration without the size and age rules.

The analysis compares animals by one column, the animal group. In step 3 the user ticks which of the export's columns with 2 to 100 values, and the age group, the prepared data carries; step 8 chooses one of them, and can choose again without preparing the data again. Its values are merged into at most six groups, or left out, as the intake labels are, and the page writes the choice as mLOS's own `animal_group_columns`, `animal_group_map`, and `animal_group_filter_pass`. With no column chosen, the settings leave out `animal_group_columns`, and mLOS compares no animal groups.

An export is often cut by date: by intake date, holding the animals admitted in a range; by outcome date, holding the animals that left in a range, and so none still in care; or by both. Each cut misses stays the analysis needs near the ends of the range. The page guesses the cut from the dates: a cut by intake date makes the intakes begin at their usual pace while the outcomes build up, a cut by outcome date the reverse, and a cut by outcome date at the end leaves almost no stay without an outcome date. An export holding its whole history looks like one cut by intake date. The default study window follows the guess. It starts a horizon's length (`restricted_stay_cap`) after the first intake for a cut by intake date, or at the first outcome for a cut by outcome date. It stops before the export's last intake and last outcome, and a horizon's length before the last outcome for a cut by outcome date at the end. Whatever the guess, the page warns, for each cut the dates leave possible, when the window reaches past what that cut covers, and says what it would miss.

## What the repository holds

| Path | Contents |
|---|---|
| `web/` | The page and the mLOS settings template it fills in |
| `pins.py` | The exact versions the site is built from: the mLOS and ShelterDataPrep commits, webR, the R packages, Pyodide, the deck builder's Python packages with their checksums, and the demo exports with their checksums and labels |
| `build_site.py` | Downloads everything `pins.py` names and assembles the site in `_site/` |
| `serve.py` | Serves `_site/` on this computer, for testing |
| `.github/workflows/pages.yml` | Builds the site and publishes it to GitHub Pages on every push to `main` |
| `CHANGELOG.md` | What changed in each release, for a visitor to the page, and whether any change can move a number in a result |
| `CITATION.cff` | Citation metadata, for GitHub's "Cite this repository" button |
| `.zenodo.json` | The same metadata in the form Zenodo reads when it archives a release, with the related works it lists |
| `check_citation.py` | Checks that `CITATION.cff`, `.zenodo.json`, and `pins.py` agree, that `.zenodo.json` uses only names Zenodo reads, and, in a tag build, that the tag names the same version |
| `.github/workflows/citation.yml` | Runs `check_citation.py` on every push to `main`, every pull request, and every tag, apart from publishing |

No program's code, webR, the packages, nor the demo data is stored in this repository; each build downloads them at the versions in `pins.py`. Downloads are kept in `.cache/`, so a second build is fast.

## Building and testing on this computer

Python 3.9 or later, with no packages to install:

```
python3 build_site.py
python3 serve.py
```

Then open http://localhost:8000. The first build downloads about 85 MB.

## Publishing

Once, in the repository's settings on GitHub: **Settings > Pages > Build and deployment > Source: GitHub Actions**. After that, every push to `main` rebuilds and republishes the site.

## Changing a version

Edit `pins.py` and build. A pinned R package that the webR repository no longer lists, or a Python wheel or demo export whose checksum does not match, stops the build with a message saying what to change.

A new version of Pyodide or webR, or a demo export from a new deposit, also changes its reference in `CITATION.cff` and `.zenodo.json`; `python3 check_citation.py` names each reference that no longer matches `pins.py`.

## Citing

mLOSweb is archived at [10.5281/zenodo.24124646](https://doi.org/10.5281/zenodo.24124646). Cite that with the version the page's footer reports: the DOI resolves to the newest release. A footer that reads "plus unreleased changes" belongs to a build made after that release, from a `main` whose `CHANGELOG.md` has an "Unreleased" section; results from such a build are cited with the commit the footer gives as well. `CITATION.cff` gives the citation for this page. Results computed with it come from mLOS and ShelterDataPrep, which run unchanged inside it, so a work that reports them also cites those two, at the versions the page's footer reports.

## Releasing

Zenodo archives each GitHub release of this repository and gives it a DOI. It builds the record from `.zenodo.json` alone: title, version, author, description, notes, keywords, related works, and references, with the license read from `LICENSE`. Nothing is entered by hand on Zenodo. The checklist at the top of `CITATION.cff` gives the reasons behind these steps.

1. In `CITATION.cff`, set `version` and `date-released`, the date in UTC (`TZ=UTC date +%F`), since GitHub stamps tags in UTC. In `.zenodo.json`, set `version`, the version in `title`, and the tag in the GitHub tree link to the same version.
2. In `CHANGELOG.md`, rename the "Unreleased" heading to the version and the same date, such as `## 0.1.0 (2026-11-11)`. Run `python3 check_citation.py`, then merge these changes into `main` through a pull request.
3. On GitHub, create a release whose tag is `v` followed by the version, such as `v0.1.0`, the tag the tree link names. The record's description comes from `.zenodo.json`, not from the release notes.
4. When Zenodo has archived it, check the record: the title `mLOSweb (Version X.Y.Z)`, the version with no leading `v`, the related works, the two references, and the license.
5. After the first archived release, add Zenodo's concept DOI, the one that resolves to the newest release, as `doi:` in `CITATION.cff` and as a link in this README.

The repository is switched on in Zenodo; Zenodo archives no release made before that.

## License

MIT; see `LICENSE`.
