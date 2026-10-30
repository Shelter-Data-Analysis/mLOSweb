"""Serve the built site locally:  python3 serve.py  then open http://localhost:8000

Python's own `http.server` also works, except that some Python versions serve
.wasm and .mjs files with a type browsers refuse; this script sets both.
"""

import functools
import http.server
import sys
from pathlib import Path

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
site = Path(__file__).resolve().parent / "_site"
handler = http.server.SimpleHTTPRequestHandler
handler.extensions_map[".wasm"] = "application/wasm"
handler.extensions_map[".mjs"] = "text/javascript"
print("serving {0} at http://localhost:{1}".format(site, port))
http.server.ThreadingHTTPServer(
    ("127.0.0.1", port), functools.partial(handler, directory=str(site))).serve_forever()
