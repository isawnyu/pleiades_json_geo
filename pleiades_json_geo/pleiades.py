#
# This file is part of "pleiades_json_geo"
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#
"""
Handle Pleiades JSON
"""
from copy import deepcopy
import logging
import re
from uri import URI
from webiquette.webi import Webi, DEFAULT_HEADERS

rx_pleiades_uri = re.compile(r"^https?://pleiades.stoa.org/places/(?P<pid>\d+)$")


class PleiadesWebInterface(Webi):
    def __init__(self):
        headers = deepcopy(DEFAULT_HEADERS)
        headers[
            "User-Agent"
        ] = "pleiades_json_geo/0.1 (+https://github.com/isawnyu/pleiades_json_geo)"
        Webi.__init__(self, netloc="pleiades.stoa.org", headers=headers)


class PleiadesPlaceCollection:
    def __init__(self, source: str = None):
        pass


class PleiadesJSONPlace:
    def __init__(self, place, place_collection: PleiadesPlaceCollection = None):
        if not isinstance(place, (str, int)):
            raise TypeError(
                f"Expected a {str} object for 'place', but got {type(place)}."
            )
        if isinstance(place, int):
            s = str(place)
            n = int(s)
            if n == place:
                place_string = s
        else:
            place_string = place

        m = rx_pleiades_uri.match(place_string)
        if m:
            self._pleiades_uri = URI(place_string.replace("http://", "https://"))
            self.place_id = m.group("pid")
        else:
            try:
                n = int(place_string)
            except ValueError:
                raise ValueError(
                    f"Expected either a full Pleiades URI or a numeric Pleiades place ID for 'source', but got '{place_string}'."
                )
            self.place_id = place_string
            self._pleiades_uri = URI(f"https://pleiades.stoa.org/places/{place_string}")

        self.place_collection = place_collection
        if self.place_collection is None:
            webi = PleiadesWebInterface()
            r = webi.get(self.pleiades_uri + "/json")
            if r.status_code != 200:
                r.raise_for_status()
            self.pleiades_json = r.json()
        else:
            self.pleiades_json = place_collection.get_json(self.pleiades_uri)

    @property
    def pleiades_uri(self):
        return str(self._pleiades_uri)
