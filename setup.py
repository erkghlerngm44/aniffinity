from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

about = {}

with open(path.join(here, "README.rst"), encoding="utf-8") as file:
    long_description = file.read()

with open(path.join(here, "aniffinity", "__about__.py")) as file:
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
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],

    "keywords": "anilist affinity kitsu myanimelist scores pearson",

    "packages": ["aniffinity"],

    "setup_requires": ["pytest-runner >=2.11, <3"],

    "install_requires": [
        "json-api-doc >=0.7, <0.8",
        "requests >=2.18, <3"
    ],

    "extras_require": {
        "conventions": [
            "flake8 >=3.4, <4",
            "pydocstyle >=3.0, <4",
        ],
        "docs": [
            "sphinx >=1.6, <2",
            "sphinx_rtd_theme",
        ],
        "tests": [
            "coverage >=4.4, <5",
            "mock >=2.0, <3",
            "pytest >=4.1, <5",
            "vcrpy >=2.0, <3",
        ],
        "travis": [
            "codecov >=2.0, <3",
        ],
    },

    "test_suite": "tests",

    "tests_require": []
}

# Mirror the extras_require.test in tests_require
settings["tests_require"].extend(settings["extras_require"]["tests"])


setup(**settings)
