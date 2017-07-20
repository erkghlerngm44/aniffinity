from setuptools import setup
from codecs import open
from os import path


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
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],

    "keywords": "affinity mal myanimelist",

    "packages": ["malaffinity"],

    "setup_requires": ["pytest-runner >=2.11, <3"],

    "install_requires": [
        "beautifulsoup4 >=4.6, <5",
        "lxml >=3.8, <4",
        "requests >=2.18, <3",
        # Meh, fuck it. Should just default to the inbuilt
        # if it exists, otherwise it'll use this
        "statistics >=1.0, <2"
    ],

    "extras_require": {
        "doc": [
            "sphinx >=1.6, <2",
            "sphinx_rtd_theme",
        ],
        "test": [
            "coverage >=4.4, <5",
            "mock >=2.0, <3",
            "pytest >=3.1, <4",
        ]
    },

    "test_suite": "tests",

    "tests_require": []
}

# Mirror the extras_require.test in tests_require
settings["tests_require"].extend(settings["extras_require"]["test"])


setup(**settings)
