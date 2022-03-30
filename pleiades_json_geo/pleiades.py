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
import json
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

    def flattened(self):
        """Move useful extension objects to properties on each feature."""
        logger = logging.getLogger(self.__class__.__name__ + ".flatten")
        flat = dict()
        j = self.pleiades_json
        for k in ["features", "type"]:
            flat[k] = deepcopy(j[k])
        for i, feature in enumerate(j["features"]):
            ffp = flat["features"][i]["properties"]

            # copy useful place information
            crosswalk = {
                "place_uri": "uri",
                "place_id": "id",
                "place_title": "title",
                "feature_type_uris": "placeTypeURIs",
                "place_description": "description",
                "place_details": "details",
            }
            for destk, sourcek in crosswalk.items():
                ffp[destk] = j[sourcek]

            # copy useful information from names
            names = dict()
            for pname in j["names"]:
                name_strings = list()
                if pname["attested"]:
                    name_strings.append(pname["attested"])
                name_strings.extend([n.strip() for n in pname["romanized"].split(",")])
                if (
                    pname["associationCertainty"] != "certain"
                    or pname["transcriptionAccuracy"] != "accurate"
                ):
                    name_strings = [f"{n}?" for n in name_strings]
                name_key = pname["nameType"]
                if pname["end"] >= 1700:
                    name_key = "associated_modern"
                try:
                    names[name_key]
                except KeyError:
                    names[name_key] = set()
                else:
                    names[name_key].update(name_strings)
            for k in [
                "associated_modern",
                "ethnic",
                "geographic",
                "label",
                "unknown",
                "undefined",
            ]:
                destk = f"{k}_names"
                if k == "label":
                    destk = "labels"
                try:
                    names[k]
                except KeyError:
                    ffp[destk] = []
                else:
                    ffp[destk] = list(names[k])

            # copy useful properties from the "location" to feature:properties

            feature_uri = feature["properties"]["link"]
            location = [
                l for l in self.pleiades_json["locations"] if l["uri"] == feature_uri
            ][0]
            crosswalk = {
                "association_certainty_uri": "associationCertaintyURI",
                "feature_type_uris": "featureTypeURI",
                "archaeological_remains": "archaeologicalRemains",
                "accuracy_meters": "accuracy_value",
                "location_types": "locationType",
                "start_year": "start",
                "end_year": "end",
            }
            for destk, sourcek in crosswalk.items():
                try:
                    ffp[destk]
                except KeyError:
                    ffp[destk] = location[sourcek]
                else:
                    if isinstance(ffp[destk], list) and isinstance(
                        location[sourcek], list
                    ):
                        ffp[destk].extend(location[sourcek])
                        ffp[destk] = list(set(ffp[destk]))
                    elif isinstance(ffp[destk], str) and isinstance(
                        location[sourcek], str
                    ):
                        if ffp[destkt] != location[sourcek]:
                            ffp[destk] = " ".join((ffp[destk], location[sourcek]))
                    else:
                        raise TypeError()

        return flat

    @property
    def pleiades_uri(self):
        return str(self._pleiades_uri)
