"""Assemble the site into _site/ from the versions in pins.py.

    python3 build_site.py

Downloads go to .cache/, so a second build is fast and works offline. The site
is the page in web/ plus:

    webr/      the webR runtime
    repo/      the R packages, laid out as a webR package repository
    mlos/      the mLOS scripts the run sources, and the deck builder mlos_review
    wheels/    the deck builder's Python packages that Pyodide does not carry
    sdp/       the ShelterDataPrep package
    data/      the demo export, uncompressed
    manifest.json  the versions and file lists the page reads at startup

Python 3.9 or later, standard library only.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import re
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

import pins

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
SITE = HERE / "_site"
GITHUB = "https://codeload.github.com/Shelter-Data-Analysis/{0}/tar.gz/{1}"
WEBR_NPM = "https://registry.npmjs.org/webr/-/webr-{0}.tgz"
WEBR_REPO = "https://repo.r-wasm.org/bin/emscripten/contrib/{0}/"


def fetch(url: str, name: str) -> bytes:
    """The bytes at `url`, kept in the cache under `name`."""
    path = CACHE / name
    if not path.exists():
        print("download", url)
        with urllib.request.urlopen(url) as response:
            data = response.read()
        CACHE.mkdir(exist_ok=True)
        path.write_bytes(data)
    return path.read_bytes()


def tar_members(data: bytes) -> dict[str, bytes]:
    """Every regular file in a .tar.gz, keyed by its path inside the archive."""
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            if member.isfile():
                out[member.name] = archive.extractfile(member).read()
    return out


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def strip_top(files: dict[str, bytes]) -> dict[str, bytes]:
    """Drop the single top-level directory that GitHub and npm archives add."""
    return {name.split("/", 1)[1]: data for name, data in files.items() if "/" in name}


def mlos() -> tuple[list[str], list[str], str]:
    files = strip_top(tar_members(fetch(GITHUB.format("mLOS", pins.MLOS_REF),
                                        "mLOS-{0}.tar.gz".format(pins.MLOS_REF))))
    runner = files["mlos_run_complete.R"].decode()
    sourced = re.findall(r'^source\("([^"]+)"\)', runner, flags=re.M)
    names = sourced + ["mlos_run_complete.R"]
    for name in names:
        write(SITE / "mlos" / name, files[name])
    # The deck builder: its modules, and the files it opens beside them.
    review = sorted(name for name in files
                    if re.fullmatch(r"mlos_review/[a-z_]+\.(py|png|svg)", name))
    for name in review:
        write(SITE / "mlos" / name, files[name])
    version = re.search(r'^MLOS_VERSION\s*<-\s*"([^"]+)"', files["mlos_common.R"].decode(), flags=re.M)
    return names, review, version.group(1)


def shelterprep() -> tuple[list[str], str]:
    files = strip_top(tar_members(fetch(GITHUB.format("ShelterDataPrep", pins.SDP_REF),
                                        "ShelterDataPrep-{0}.tar.gz".format(pins.SDP_REF))))
    names = sorted(name.split("/", 1)[1] for name in files
                   if re.fullmatch(r"shelterprep/[a-z_]+\.py", name) and not name.endswith("__main__.py"))
    for name in names:
        write(SITE / "sdp" / "shelterprep" / name, files["shelterprep/" + name])
    version = re.search(r'^__version__\s*=\s*"([^"]+)"', files["shelterprep/version.py"].decode(), flags=re.M)
    return names, version.group(1)


def webr() -> None:
    files = tar_members(fetch(WEBR_NPM.format(pins.WEBR_VERSION), "webr-{0}.tgz".format(pins.WEBR_VERSION)))
    for name, data in files.items():
        if name.startswith("package/dist/"):
            write(SITE / "webr" / name[len("package/dist/"):], data)
    # The package's webr.mjs is its Node build, which imports Node modules and
    # fails in a browser; webr.js is the browser build of the same module.
    shutil.copyfile(SITE / "webr" / "webr.js", SITE / "webr" / "webr.mjs")


def r_packages() -> None:
    base = WEBR_REPO.format(pins.WEBR_R_VERSION)
    index = fetch(base + "PACKAGES", "PACKAGES-{0}".format(pins.WEBR_R_VERSION)).decode()
    blocks = {}
    for block in index.split("\n\n"):
        name = re.search(r"^Package: (\S+)", block, flags=re.M)
        version = re.search(r"^Version: (\S+)", block, flags=re.M)
        if name and version:
            blocks["{0}_{1}.tgz".format(name.group(1), version.group(1))] = block.strip()
    missing = [f for f in pins.R_PACKAGES if f not in blocks]
    if missing:
        sys.exit("pins.R_PACKAGES names versions that {0} no longer lists: {1}. "
                 "Update them to the versions in that index.".format(base, ", ".join(missing)))
    target = SITE / "repo" / "bin" / "emscripten" / "contrib" / pins.WEBR_R_VERSION
    for f in pins.R_PACKAGES:
        write(target / f, fetch(base + f, f))
    write(target / "PACKAGES", ("\n\n".join(blocks[f] for f in pins.R_PACKAGES) + "\n").encode())


def wheels() -> list[str]:
    names = []
    for url, sha256 in pins.PYPI_WHEELS:
        name = url.rsplit("/", 1)[1]
        data = fetch(url, name)
        digest = hashlib.sha256(data).hexdigest()
        if digest != sha256:
            sys.exit("{0} has checksum {1}, not {2} as pins.py states. Delete "
                     ".cache/{0} and build again.".format(name, digest, sha256))
        write(SITE / "wheels" / name, data)
        names.append(name)
    return names


def demo_data() -> None:
    data = gzip.decompress(fetch(pins.DEMO_URL, "MV_raw.csv.gz"))
    digest = hashlib.sha256(data).hexdigest()
    if digest != pins.DEMO_SHA256:
        sys.exit("The demo export's checksum is {0}, not {1} as pins.py states. "
                 "Delete .cache/MV_raw.csv.gz and build again; if it persists, "
                 "the deposit has changed.".format(digest, pins.DEMO_SHA256))
    write(SITE / "data" / "mission_viejo_export.csv", data)


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    for source in (HERE / "web").iterdir():
        text = source.read_bytes()
        if source.suffix == ".html":
            text = text.replace(b"{{PYODIDE_VERSION}}", pins.PYODIDE_VERSION.encode())
        write(SITE / source.name, text)
    mlos_files, review_files, mlos_version = mlos()
    sdp_files, sdp_version = shelterprep()
    webr()
    r_packages()
    wheel_files = wheels()
    demo_data()
    manifest = {
        "mlos": {"version": mlos_version, "commit": pins.MLOS_REF, "files": mlos_files,
                 "review_files": review_files},
        "shelterprep": {"version": sdp_version, "commit": pins.SDP_REF, "files": sdp_files},
        "webr": pins.WEBR_VERSION,
        "pyodide": pins.PYODIDE_VERSION,
        "r_packages": [f[:-len(".tgz")] for f in pins.R_PACKAGES],
        "wheels": wheel_files,
    }
    write(SITE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    size = sum(p.stat().st_size for p in SITE.rglob("*") if p.is_file())
    print("built {0} ({1:.1f} MB)".format(SITE, size / 1e6))


if __name__ == "__main__":
    main()
