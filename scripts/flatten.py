#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flatten Pleiades JSON
"""

from airtight.cli import configure_commandline
import json
import logging
from pleiades_json_geo.pleiades import PleiadesPlaceCollection
import sys

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    [
        "-l",
        "--loglevel",
        "NOTSET",
        "desired logging level ("
        + "case-insensitive string: DEBUG, INFO, WARNING, or ERROR",
        False,
    ],
    ["-v", "--verbose", False, "verbose output (logging level == INFO)", False],
    [
        "-w",
        "--veryverbose",
        False,
        "very verbose output (logging level == DEBUG)",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    places = sys.stdin.readlines()
    coll = PleiadesPlaceCollection(places=places)
    fcoll = coll.flattened()
    print(json.dumps(fcoll, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
