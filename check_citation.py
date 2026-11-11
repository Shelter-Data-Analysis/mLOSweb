"""Check that the citation metadata agree:  python3 check_citation.py

Zenodo builds each release's record from .zenodo.json alone; GitHub's
"Cite this repository" button reads CITATION.cff.  This script stops with a
message for each place where the two disagree with each other, or with
pins.py, so a release never archives metadata that names a different version,
author, or dependency than the code holds.  The version is the one written in
CITATION.cff; .zenodo.json's version, title, and GitHub tree link are held to
it, and, run in a tag build, so is the tag.  Zenodo drops a field name it does
not know without saying so, and fails the archive on a file it cannot read,
which costs a version number to repair; hence the checks of field and relation
names.  Python 3.9 or later, no packages.
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


def folded(key):
    """A top-level folded scalar (`key: >-`) of CITATION.cff, as YAML reads it.

    Lines of one paragraph join with a space, and a blank line between
    paragraphs becomes a line break.  A line indented further than the first,
    which YAML keeps as written, is reported rather than read.
    """
    m = re.search(r"^{0}:\s*>-\s*\n((?:  .*\n|\s*\n)*)".format(re.escape(key)), cff, re.M)
    if not m:
        problems.append("{0} in CITATION.cff is not a folded block (`{0}: >-`)".format(key))
        return None
    paragraphs, lines = [], []
    for line in m.group(1).rstrip("\n").split("\n"):
        if not line.strip():
            paragraphs.append(" ".join(lines))
            lines = []
        elif line.startswith("   "):
            problems.append("{0} in CITATION.cff has a line indented past the others".format(key))
        else:
            lines.append(line[2:])
    paragraphs.append(" ".join(lines))
    return "\n".join(paragraphs)


# The field names Zenodo reads in .zenodo.json, and the relation names it
# accepts for a related work (DataCite's, in camel case).
ZENODO_FIELDS = {
    "upload_type", "publication_type", "title", "version", "creators",
    "contributors", "description", "notes", "keywords", "subjects", "license",
    "related_identifiers", "references", "language", "dates", "locations",
    "grants", "communities", "publication_date", "access_right",
    "imprint_publisher"}
ZENODO_RELATIONS = {
    "isCitedBy", "cites", "isSupplementTo", "isSupplementedBy",
    "isContinuedBy", "continues", "isDescribedBy", "describes", "hasMetadata",
    "isMetadataFor", "isNewVersionOf", "isPreviousVersionOf", "isPartOf",
    "hasPart", "isReferencedBy", "references", "isDocumentedBy", "documents",
    "isCompiledBy", "compiles", "isVariantFormOf", "isOriginalFormOf",
    "isIdenticalTo", "isReviewedBy", "reviews", "isDerivedFrom", "isSourceOf",
    "requires", "isRequiredBy", "isObsoletedBy", "obsoletes"}
RELATED_KEYS = {"identifier", "relation", "resource_type"}


def same(what, a, b):
    if a != b:
        problems.append("{0}: CITATION.cff has {1!r}, .zenodo.json has {2!r}".format(what, a, b))


version = top("version")
if not re.fullmatch(r"\d+\.\d+\.\d+", version or ""):
    problems.append("version {0!r} in CITATION.cff is not a bare version such as 0.1.0".format(version))

for field in sorted(set(zen) - ZENODO_FIELDS):
    problems.append("{0!r} is not a field Zenodo reads in .zenodo.json".format(field))
for r in zen.get("related_identifiers", []):
    if r.get("relation") not in ZENODO_RELATIONS:
        problems.append("{0!r}, the relation of {1}, is not one Zenodo accepts".format(
            r.get("relation"), r.get("identifier")))
    for key in sorted(set(r) - RELATED_KEYS):
        problems.append("{0!r}, in the related work {1}, is not a key Zenodo reads".format(
            key, r.get("identifier")))
if not zen.get("related_identifiers"):
    problems.append(".zenodo.json lists no related works")
if not (here / "LICENSE").exists():
    problems.append("LICENSE is missing, and .zenodo.json names no license, so Zenodo reads it from there")

same("version", version, zen.get("version"))
same("title with its version", "{0} (Version {1})".format(top("title"), version), zen.get("title"))
tree = "{0}/tree/v{1}".format(top("repository-code"), version)
if not any(r.get("identifier") == tree and r.get("relation") == "isSupplementTo"
           for r in zen.get("related_identifiers", [])):
    problems.append(".zenodo.json does not link the tree of tag v{0}, {1}, as isSupplementTo".format(
        version, tree))
same("abstract (description in .zenodo.json)", folded("abstract"), zen.get("description"))
same("message (notes in .zenodo.json)", folded("message"), zen.get("notes"))
same("keywords", re.findall(r"^  - (.+)$", block("keywords"), re.M), zen.get("keywords"))
same("authors (creators in .zenodo.json)",
     ["{0}, {1} | {2}".format(f, g, o.rsplit("/", 1)[-1]) for f, g, o in re.findall(
         r"family-names:\s*\"([^\"]+)\"\s*\n\s*given-names:\s*\"([^\"]+)\"\s*\n\s*orcid:\s*\"([^\"]+)\"",
         block("authors"))],
     ["{0} | {1}".format(c.get("name"), c.get("orcid")) for c in zen.get("creators", [])])

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

related = {r.get("identifier") for r in zen.get("related_identifiers", [])}
cited = {r["doi"] for r in refs.values() if r["doi"]}
for d in sorted(cited - related):
    problems.append("{0} is a reference in CITATION.cff but not a related identifier in .zenodo.json".format(d))
for d in sorted(i for i in related if i and i.startswith("10.") and i not in cited):
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
    if tag != "v" + str(version):
        problems.append("the tag {0} is not v{1}, the tag .zenodo.json's tree link names".format(tag, version))

if problems:
    print("The citation metadata disagree:")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("CITATION.cff, .zenodo.json, and pins.py agree on version {0}.".format(version))
