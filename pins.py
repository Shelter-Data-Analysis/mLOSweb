"""The exact versions the site is assembled from.

`build_site.py` reads this file and nothing else to decide what to download, so
a change of version is a change here and nowhere else. Each entry is checked as
it is fetched, and a download that does not match stops the build.
"""

# The two programs, as commits of their public repositories under
# github.com/Shelter-Data-Analysis. A release replaces each commit with the
# release's tag. The mLOS commit supplies both the R analysis and the deck
# builder, mlos_review.
MLOS_REF = "dc8ec2de616a4fccb7a4b893428276c02c2eeb7d"
SDP_REF = "c539d45b81cf52eecfa68b01456392e11ec65290"

# webR, the build of R for WebAssembly, from its npm package. Its R version
# decides which directory of repo.r-wasm.org the packages come from.
WEBR_VERSION = "0.6.0"
WEBR_R_VERSION = "4.6"

# R packages, as the file names in repo.r-wasm.org, so each version is pinned:
# what mLOS needs (survival, yaml, jsonlite, digest, openxlsx) and what those
# depend on. flexsurv is left out because the site turns off the Weibull fit.
R_PACKAGES = [
    "survival_3.8-12.tgz",
    "Matrix_1.7-6.tgz",
    "lattice_0.23-1.tgz",
    "yaml_2.3.12.tgz",
    "jsonlite_2.0.0.tgz",
    "digest_0.6.39.tgz",
    "openxlsx_4.2.9.tgz",
    "Rcpp_1.1.2.tgz",
    "stringi_1.8.9.tgz",
    "zip_3.0.2.tgz",
    "cli_3.6.6.tgz",
]

# Pyodide, the build of Python for WebAssembly. The page loads it, with pandas
# and PyYAML, from the jsDelivr content delivery network; the deck builder
# adds matplotlib, lxml, Pillow, and typing-extensions from the same place.
PYODIDE_VERSION = "0.29.5"

# The deck builder's pure-Python packages that Pyodide does not carry, as
# wheels from PyPI with their published SHA-256 checksums. The site serves them
# itself, and the page installs them without looking up dependencies.
PYPI_WHEELS = [
    ("https://files.pythonhosted.org/packages/d9/4f/00be2196329ebbff56ce564aa94efb0fbc828d00de250b1980de1a34ab49/python_pptx-1.0.2-py3-none-any.whl",
     "160838e0b8565a8b1f67947675886e9fea18aa5e795db7ae531606d68e785cba"),
    ("https://files.pythonhosted.org/packages/fa/34/a22e6664211f0c8879521328000bdcae9bf6dbafa94a923e531f6d5b3f73/xlsxwriter-3.2.5-py3-none-any.whl",
     "4f4824234e1eaf9d95df9a8fe974585ff91d0f5e3d3f12ace5b71e443c1c6abd"),
    ("https://files.pythonhosted.org/packages/c0/da/977ded879c29cbd04de313843e76868e6e13408a94ed6b987245dc7c8506/openpyxl-3.1.5-py2.py3-none-any.whl",
     "5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2"),
    ("https://files.pythonhosted.org/packages/c1/8b/5fe2cc11fee489817272089c4203e679c63b570a5aaeb18d852ae3cbba6a/et_xmlfile-2.0.0-py3-none-any.whl",
     "7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa"),
]

# The demo exports, in the order the page lists them, each a file in a public
# deposit named by its DOI. The checksum is of the contents as the site serves
# them: uncompressed for a gzipped CSV, as ShelterDataPrep's run log states it,
# and the file as deposited for a workbook. "file" is the name the site serves
# it under, and "label" what the page's list shows.
DEMOS = [
    {"file": "irvine_2025-10-08.xlsx",
     "label": "Irvine Animal Care Center, all species (workbook of 2025-10-08, outcomes 2018-01-01 to early October 2025)",
     "doi": "10.6084/m9.figshare.34875669.v2",
     "url": "https://ndownloader.figshare.com/files/70947090",
     "sha256": "7bd9d1b971b56118aa02fbd8a06a4c892da9ec686485662516f8ef94997b7aa4"},
    {"file": "irvine_all_species.csv",
     "label": "Irvine Animal Care Center, all species (CIall_raw.csv.gz, outcomes to 2025-02-02)",
     "doi": "10.5281/zenodo.22051091",
     "url": "https://zenodo.org/records/22051091/files/CIall_raw.csv.gz?download=1",
     "sha256": "9a1cc20d24c1987564ea9ae59ac17d219b47232823ad472130c692b403eb6b7d"},
]
