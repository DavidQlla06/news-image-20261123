#!/usr/bin/env python3
"""Entry point for news-image-20261123: draws entry.png via generate.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import main

if __name__ == "__main__":
    main()
