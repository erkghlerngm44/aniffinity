import datetime
import sys

sys.path.insert(0, "..")

from malaffinity import __about__  # NOQA

now = datetime.datetime.now()


# Common stuff
_author = __about__.__author__
_title = __about__.__title__
_version = __about__.__version__


project = _title
copyright = "{}, {}".format(now.year, _author)
author = _author


version = ".".join(_version.split(".")[:2])
release = _version


extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"


language = None


exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


htmlhelp_basename = project


# Force it to document ``__init__`, because it doesn't do that by default
# https://stackoverflow.com/a/5599712
def skip(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
