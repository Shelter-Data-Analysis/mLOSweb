"""Check that the citation metadata agree:  python3 check_citation.py

Zenodo builds each release's record from .zenodo.json alone; GitHub's
"Cite this repository" button reads CITATION.cff.  This script stops with a
message for each place where the two disagree with each other, or with
pins.py, so a release never archives metadata that names a different version,
author, or dependency than the code holds.  Run in a tag build, it also checks
that the tag names the same version.  Python 3.9 or later, no packages.
"""

import json
import os
import re
import runpy
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
cff = (here / "CITATION.cff").read_text()
zen = json.loads((here / ".zenodo.json").read_text())
pins = runpy.run_path(str(here / "pins.py"))
problems = []


def top(key):
    """A top-level scalar of CITATION.cff, unquoted."""
    m = re.search(r"^{0}:\s*\"?([^\"\n]*)\"?\s*$".format(re.escape(key)), cff, re.M)
    return m.group(1).strip() if m else None


def block(key):
    """The indented lines under a top-level key of CITATION.cff."""
    m = re.search(r"^{0}:\s*\n((?:[ #].*\n|\n)*)".format(re.escape(key)), cff, re.M)
    return m.group(1) if m else ""


def same(what, a, b):
    if a != b:
        problems.append("{0}: CITATION.cff has {1!r}, .zenodo.json has {2!r}".format(what, a, b))


version = top("version")
if not re.fullmatch(r"\d+\.\d+\.\d+", version or ""):
    problems.append("version {0!r} in CITATION.cff is not a bare version such as 0.1.0".format(version))
same("version", version, zen.get("version"))
same("title", top("title"), zen.get("title"))
same("license", (top("license") or "").lower(), (zen.get("license") or "").lower())
same("keywords", re.findall(r"^  - (.+)$", block("keywords"), re.M), zen.get("keywords"))
same("author ORCIDs",
     sorted(o.rsplit("/", 1)[-1] for o in re.findall(r"orcid:\s*\"([^\"]+)\"", block("authors"))),
     sorted(c.get("orcid", "") for c in zen.get("creators", [])))

# Each reference in CITATION.cff, by its title, with its DOI and version.
# A title folded over several lines is not needed by name, so it is kept by
# its position instead.
refs = {}
for k, entry in enumerate(re.split(r"^  - type:", block("references"), flags=re.M)[1:]):
    title = re.search(r"^    title:\s*\"([^\"]+)\"", entry, re.M)
    doi = re.search(r"^    doi:\s*\"([^\"]+)\"", entry, re.M)
    ver = re.search(r"^    version:\s*\"([^\"]+)\"", entry, re.M)
    url = re.search(r"^    repository-code:\s*\"([^\"]+)\"", entry, re.M)
    refs[title.group(1) if title else k] = {
        "doi": doi and doi.group(1), "version": ver and ver.group(1), "url": url and url.group(1)}

related = {r["identifier"] for r in zen.get("related_identifiers", [])}
cited = {r["doi"] for r in refs.values() if r["doi"]}
for d in sorted(cited - related):
    problems.append("{0} is a reference in CITATION.cff but not a related identifier in .zenodo.json".format(d))
for d in sorted(i for i in related if i.startswith("10.") and i not in cited):
    problems.append("{0} is a related identifier in .zenodo.json but not a reference in CITATION.cff".format(d))
for d in sorted({demo["doi"] for demo in pins["DEMOS"]} - cited):
    problems.append("{0}, a demo export's deposit in pins.py, is not a reference in CITATION.cff".format(d))

for name, pinned in (("Pyodide", pins["PYODIDE_VERSION"]), ("webR", pins["WEBR_VERSION"])):
    got = refs.get(name, {}).get("version")
    if got != pinned:
        problems.append("{0} is {1} in pins.py but {2!r} in CITATION.cff".format(name, pinned, got))
webr_url = refs.get("webR", {}).get("url")
if webr_url not in related:
    problems.append("webR's repository {0!r} is not a related identifier in .zenodo.json".format(webr_url))

ref = os.environ.get("GITHUB_REF", "")
if ref.startswith("refs/tags/"):
    tag = ref[len("refs/tags/"):]
    if tag not in (version, "v" + str(version)):
        problems.append("the tag {0} does not name version {1}".format(tag, version))

if problems:
    print("The citation metadata disagree:")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("CITATION.cff, .zenodo.json, and pins.py agree on version {0}.".format(version))
