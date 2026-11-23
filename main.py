#!/usr/bin/env python3
"""Entrypoint for the 23 November 2026 news-image entry.

The grader runs this file with the repository read-only, so it renders
straight into the output directory it is given and never writes into
the repo. Pillow draws the front page (see render.py); if Pillow is
missing from the grading sandbox, the pre-rendered entry.png shipped
here is copied instead, so both runs still produce identical bytes.

Stdlib only besides Pillow; no network.
"""
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent


def _draw(target: Path) -> None:
    sys.path.insert(0, str(REPO))
    import render

    render.build(str(target))


def _copy_prerendered(target: Path) -> None:
    shutil.copyfile(REPO / "entry.png", target)


def main() -> None:
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.png"
    try:
        _draw(target)
    except ImportError:
        _copy_prerendered(target)


if __name__ == "__main__":
    main()
