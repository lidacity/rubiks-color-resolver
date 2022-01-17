#!/usr/bin/env python3

from rubiks_color_resolver import resolve_colors
import logging
import sys


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)7s: %(message)s"
)

resolve_colors(sys.argv)
