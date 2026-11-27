"""news-image-20261127 — entry point.

The front page itself is rendered ahead of time by tools/generate.py
and shipped as assets/entry.png. This module only moves that file to
the directory the harness asks for (MAKEFUN_OUTPUT_DIR), then checks
the copy landed byte-identical. Standard library only: no network,
no subprocess, no clock, no randomness.
"""

import os
import shutil
from pathlib import Path


def rendered_page() -> Path:
    """Absolute path of the pre-rendered front page in this repo."""
    return Path(__file__).resolve().parent / "assets" / "entry.png"


def destination() -> Path:
    """Output path the harness requested, entry.png inside it."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(wanted) / "entry.png"


def place_entry() -> Path:
    """Copy the rendered page to the harness output path."""
    src = rendered_page()
    dst = destination()
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def main() -> int:
    """Place the entry and confirm the copy is byte-identical."""
    src = rendered_page()
    if not src.is_file():
        print("rendered page missing: %s" % src)
        print("build it first: python3 tools/generate.py")
        return 1
    dst = place_entry()
    if dst.stat().st_size != src.stat().st_size:
        print("copy failed size check: %s" % dst)
        return 1
    print("entry.png -> %s" % dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
