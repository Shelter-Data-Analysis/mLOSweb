# mLOS Web

A web page that runs ShelterDataPrep and mLOS in the browser, for animal shelters without an R or Python installation. The shelter loads a CSV export of its stays, answers a few questions about it, and gets the mLOS plots, tables, and workbook. Everything runs in the visitor's browser: the data is not uploaded anywhere.

The page prepares the export with ShelterDataPrep, running in Pyodide (Python compiled to WebAssembly), then analyzes it with mLOS, running in webR (R compiled to WebAssembly). A last, separate step runs mLOS's deck builder, `mlos_review`, in the same Python to write a slide deck and a workbook of its tables, and shows the tables the user picks. All three programs run unchanged. The demo uses the Mission Viejo Animal Services export deposited in Zenodo (10.5281/zenodo.22051091).

## What the repository holds

| Path | Contents |
|---|---|
| `web/` | The page and the mLOS settings template it fills in |
| `pins.py` | The exact versions the site is built from: the mLOS and ShelterDataPrep commits, webR, the R packages, Pyodide, the deck builder's Python packages with their checksums, and the demo export with its checksum |
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
