# mLOS Web

A web page that runs ShelterDataPrep and mLOS in the browser, for animal shelters without an R or Python installation. The shelter loads an export of its stays, as a CSV file or an Excel workbook, answers a few questions about it, and gets the mLOS plots, tables, and workbook. A ShelterDataPrep configuration or an mLOS settings file, whether the page wrote it or it was prepared by hand, can stand in for the questions; the page lists each change it makes to such a file, such as turning off a feature the site does not run. Everything runs in the visitor's browser: the data is not uploaded anywhere.

The page prepares the export with ShelterDataPrep, running in Pyodide (Python compiled to WebAssembly), then analyzes it with mLOS, running in webR (R compiled to WebAssembly). A last, separate step runs mLOS's deck builder, `mlos_review`, in the same Python to write a slide deck and a workbook of its tables, and shows the tables the user picks. All three programs run unchanged. A workbook (.xlsx or .xlsm) goes to ShelterDataPrep as it is, with a `sheet:` line naming the sheet that holds the stays: the sheet whose row of column names names the most of the columns the page asks for, or the one the user picks from the list of sheets. The page reads a sheet through ShelterDataPrep's own reader, `shelterprep.read_source`, so it sees the rows and column names a run reads: the names from the first row with a value in any column, and no row without a value. The same reader repairs two things in a workbook, and the page says what it did: a heading merged across columns names the column of values under it, where the heading's own column is empty, and font families above 14, which Excel writes and openpyxl refuses, are left out of a copy it reads, with no cell value changed. A column with no name and no values, such as a spacer between columns, is left off the page; ShelterDataPrep reads only the columns its configuration names, so it never reads one either. A row with no values is left off the page as well, as ShelterDataPrep leaves it out and counts it in its statistics table. The demo exports, which the page offers in a list, are raw files in public deposits: the Irvine Animal Care Center's workbook of 2025-10-08 (figshare, 10.6084/m9.figshare.34875669.v2) and its earlier `CIall_raw.csv.gz`, and Mission Viejo Animal Services' `MV_raw.csv.gz` (both Zenodo, 10.5281/zenodo.22051091). An export with no size or date-of-birth column, such as `CIall_raw.csv.gz`, gets a configuration without the size and age rules.

The analysis compares animals by one column, the animal group. In step 3 the user ticks which of the export's columns with 2 to 20 values, and the age group, the prepared data carries; step 8 chooses one of them, and can choose again without preparing the data again. Its values are merged into at most six groups, or left out, as the intake labels are, and the page writes the choice as mLOS's own `animal_group_columns`, `animal_group_map`, and `animal_group_filter_pass`. With no column chosen, the settings leave out `animal_group_columns`, and mLOS compares no animal groups.

An export is often cut by date: by intake date, holding the animals admitted in a range; by outcome date, holding the animals that left in a range, and so none still in care; or by both. Each cut misses stays the analysis needs near the ends of the range. The page guesses the cut from the dates: a cut by intake date makes the intakes begin at their usual pace while the outcomes build up, a cut by outcome date the reverse, and a cut by outcome date at the end leaves almost no stay without an outcome date. An export holding its whole history looks like one cut by intake date. The default study window follows the guess. It starts a horizon's length (`restricted_stay_cap`) after the first intake for a cut by intake date, or at the first outcome for a cut by outcome date. It stops before the export's last intake and last outcome, and a horizon's length before the last outcome for a cut by outcome date at the end. Whatever the guess, the page warns, for each cut the dates leave possible, when the window reaches past what that cut covers, and says what it would miss.

## What the repository holds

| Path | Contents |
|---|---|
| `web/` | The page and the mLOS settings template it fills in |
| `pins.py` | The exact versions the site is built from: the mLOS and ShelterDataPrep commits, webR, the R packages, Pyodide, the deck builder's Python packages with their checksums, and the demo exports with their checksums and labels |
| `build_site.py` | Downloads everything `pins.py` names and assembles the site in `_site/` |
| `serve.py` | Serves `_site/` on this computer, for testing |
| `.github/workflows/pages.yml` | Builds the site and publishes it to GitHub Pages on every push to `main` |

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

## License

MIT; see `LICENSE`.
