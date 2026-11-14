"""Run the tests of the page's pure functions:  python3 run_tests.py

The page's script is one block inside web/index.html, so nothing can import
it.  This script copies the named functions and constants out of the page as
text, puts tests/pure_functions.js after them, and runs the result in Node,
or, where Node is not installed, in the JavaScriptCore shell that macOS
includes.  It needs no package.

An optional argument names another copy of the page to test.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

# What the tests call, and what those functions use, in the order the page
# defines them.  A constant must fit on one line of the page; a list starts
# with 'const NAME = [' and ends with a line that holds '];' alone.
CONSTANTS = ["fullYear", "EDGE", "addDay"]
LISTS = ["FORMATS", "TIMES"]
FUNCTIONS = ["parseCSV", "checksum", "timeOk", "timeShape", "readDate", "validDate", "cutShape"]


def extract(page):
    """The source of each named constant and function, as the page has it."""
    parts = []
    for name in CONSTANTS:
        found = re.findall(r"^const {0} = .*;$".format(name), page, re.M)
        if len(found) != 1:
            sys.exit("run_tests.py: expected one line 'const {0} = ...;' in the page, found {1}".format(name, len(found)))
        parts.append(found[0])
    for name in LISTS:
        found = re.findall(r"^const {0} = \[$.*?^\];$".format(name), page, re.M | re.S)
        if len(found) != 1:
            sys.exit("run_tests.py: expected one list 'const {0} = [' in the page, found {1}".format(name, len(found)))
        parts.append(found[0])
    for name in FUNCTIONS:
        found = re.findall(r"^function {0}\(.*?^}}$".format(name), page, re.M | re.S)
        if len(found) != 1:
            sys.exit("run_tests.py: expected one 'function {0}(' in the page, found {1}".format(name, len(found)))
        parts.append(found[0])
    return "\n".join(parts)


def main():
    page = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "web" / "index.html"
    runtime = shutil.which("node") or (JSC if Path(JSC).exists() else None)
    if runtime is None:
        sys.exit("run_tests.py: needs Node, or the JavaScriptCore shell of macOS")
    source = extract(page.read_text(encoding="utf-8")) + "\n" + (ROOT / "tests" / "pure_functions.js").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as folder:
        script = Path(folder) / "tests.js"
        script.write_text(source, encoding="utf-8")
        result = subprocess.run([runtime, str(script)], capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    # The last line the tests print is the verdict; a script that stops early prints none.
    lines = result.stdout.strip().splitlines()
    if result.returncode != 0 or not lines or not lines[-1].startswith("ok: "):
        sys.exit(1)


if __name__ == "__main__":
    main()
