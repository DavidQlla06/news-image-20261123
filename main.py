#!/usr/bin/env python3
"""Launcher for the Monday 23 November 2026 front page build."""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import generate


def run() -> None:
    generate.main()


if __name__ == "__main__":
    run()
