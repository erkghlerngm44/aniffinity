from setuptools import setup
from codecs import open
from os import path
from sys import version_info


# Open up settings
here = path.abspath(path.dirname(__file__))

about = {}

with open(path.join(here, "README.rst"), encoding="utf-8") as file:
    long_description = file.read()

with open(path.join(here, "malaffinity", "__about__.py")) as file:
    exec(file.read(), about)


settings = {
    "name": about["__title__"],
    "version": about["__version__"],

    "description": about["__summary__"],
    "long_description": long_description,

    "url": about["__uri__"],

    "author": about["__author__"],
    "author_email": about["__email__"],

    "license": about["__license__"],

    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],

    "keywords": "affinity mal myanimelist",

    "packages": ["malaffinity"],

    "install_requires": [
        "bs4",
        "lxml",
        "requests"
    ]
}


# `statistics` is only included in Py3. Will need this for Py2.
# Tried adding to `extras_require` but that doesn't seem to be working...
if version_info[0] == 2:
    # Push the dep
    settings["install_requires"].append("statistics")


setup( **settings )
