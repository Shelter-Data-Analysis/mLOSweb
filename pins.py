"""The exact versions the site is assembled from.

`build_site.py` reads this file and nothing else to decide what to download, so
a change of version is a change here and nowhere else. Each entry is checked as
it is fetched, and a download that does not match stops the build.
"""

# The two programs, as commits of their public repositories under
# github.com/Shelter-Data-Analysis. A release replaces each commit with the
# release's tag.
MLOS_REF = "f3bdf618f0e6512fa84394fe09f4b390fd25182d"
SDP_REF = "9daa223235c81b0b7c50ba7c7f1aa64a41a1989c"

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
# and PyYAML, from the jsDelivr content delivery network.
PYODIDE_VERSION = "0.29.5"

# The demo export: Mission Viejo Animal Services, deposited as MV_raw.csv.gz in
# Zenodo record 10.5281/zenodo.22051091. The checksum is of the uncompressed
# contents, as ShelterDataPrep's run log states it.
DEMO_URL = "https://zenodo.org/records/22051091/files/MV_raw.csv.gz?download=1"
DEMO_SHA256 = "bd448e8789ef82acd96354997d2a796f935f0ef960c7b623975bf29fadf8a880"
