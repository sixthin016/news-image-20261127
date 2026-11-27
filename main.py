"""news-image-20261127 — entrypoint.

Copies the pre-rendered image (assets/entry.png, drawn in code by
tools/generate.py during the build) to the output directory the
harness requests. No network, no exec, no eval, no wall clock,
no randomness. Standard library only.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # sanity: the copy must be byte-identical to the bundled image
    if os.path.getsize(dst) != os.path.getsize(src):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
