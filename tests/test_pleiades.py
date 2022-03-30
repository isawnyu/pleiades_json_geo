#
# This file is part of "pleiades_json_geo"
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#
"""
Test the pleiades_json_geo.pleiades module
"""
import logging
from pleiades_json_geo.pleiades import PleiadesJSONPlace
from pprint import pformat
import pytest


class TestPleiadesJSONPlace:
    def test_place_pid(self):
        p = PleiadesJSONPlace(place="295374")
        assert p.place_id == "295374"
        assert p.pleiades_uri == "https://pleiades.stoa.org/places/295374"

    def test_place_pid_int(self):
        p = PleiadesJSONPlace(place=295374)
        assert p.place_id == "295374"
        assert p.pleiades_uri == "https://pleiades.stoa.org/places/295374"

    def test_place_uri(self):
        p = PleiadesJSONPlace(place="https://pleiades.stoa.org/places/295374")
        assert p.place_id == "295374"
        assert p.pleiades_uri == "https://pleiades.stoa.org/places/295374"

    def test_place_uri_old(self):
        p = PleiadesJSONPlace(place="http://pleiades.stoa.org/places/295374")
        assert p.place_id == "295374"
        assert p.pleiades_uri == "https://pleiades.stoa.org/places/295374"

    def test_bad_place_string(self):
        with pytest.raises(ValueError):
            PleiadesJSONPlace(place="banana")

    def test_flat(self):
        p = PleiadesJSONPlace(place="http://pleiades.stoa.org/places/295374")
        keys = ["placeTypes", "description", "names"]
        f = p.flattened(keys=keys)
        logger = logging.getLogger(self.__class__.__name__ + ".test_flat")
        logger.debug(pformat(f["features"], indent=4))
