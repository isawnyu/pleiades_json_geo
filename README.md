# Pleiades JSON Geo

Prepare *[Pleiades](https://pleiades.stoa.org)* JSON export data for use in QGIS.

## Authorship

By [Tom Elliott](https://github.com/paregorios) for the [Institute for the Study of the Ancient World](https://isaw.nyu.edu). (c) Copyright 2022 by New York University. Licensed under the AGPL-3.0; see LICENSE.txt file.

## Features

- Selectively rewrite *Pleiades* extension data into the "properties" object on each contained feature so that they become available attributes in the GIS.
- Flatten all the locations associated with an arbitrary list of *Pleiades* places into a single GeoJSON FeatureCollection.

## Install

1. Create a python 3.10.3 virtual environment and activate it.
2. Upgrade pip with `pip install -U pip`.
3. Get the code with `git clone https://github.com/isawnyu/pleiades_json_geo.git` or by downloading the zip file from https://github.com/isawnyu/pleiades_json_geo/archive/refs/heads/main.zip and unzipping it. 
4. Change directories into the `pleiades_json_geo` directory.
5. Install the pleiades_json_geo package and its prerequisites: `pip install -U -r requirements_dev.txt`.
6. Run the tests: `pytest`.

## Use

### On the command line

Scripts write the resulting GeoJSON to stdout. 

```
python scripts/flatten_one.py 295374
python scripts/flatten.py < tests/data/apollonia.txt
```

To capture the output to a file, use IO redirection like:

```
python scripts/flatten_one.py 295374 > /my/spatial/files/295374.geojson
```

### In code

See the tests.

