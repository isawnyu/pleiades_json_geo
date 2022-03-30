#
# This file is part of "pleiades_json_geo"
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2022 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pleiades_json_geo",
    version="0.0.1",
    author="Tom Elliot",
    author_email="tom.elliott@nyu.edu",
    description="Prepare Pleiades JSON export data for use in QGIS.",
    license="AGPL-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isawnyu/pleiades_json_geo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10.3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "airtight",
        "uri @ git+https://github.com/marrow/uri.git@5b58db87451ca4680004a8993a56bfc4dafff4d4",
        "webiquette @ git+https://github.com/paregorios/webiquette.git",
    ],
    python_requires=">=3.10.3",
)
