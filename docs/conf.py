import datetime
import sys

sys.path.insert(0, "..")

from aniffinity import __about__  # noqa: E402

year = datetime.datetime.now().year


author = __about__.__author__
project = __about__.__title__
release = __about__.__version__


copyright = "{}, {}".format(year, author)


version = ".".join(release.split(".")[:2])


extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"


language = None


exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"


html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]


htmlhelp_basename = project


# Force it to document ``__init__`, because it doesn't do that by default
# https://stackoverflow.com/a/5599712
def skip(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
