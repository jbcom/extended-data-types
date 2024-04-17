import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

# Project information
project = "Extended Data Types"
author = "Jon Bogaty"
copyright = f"2024, {author}"
version = "1.0.0"

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    html_context = {"READTHEDOCS": True}

# General configuration
extensions = [
    "autodoc2",
    "seed_intersphinx_mapping",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

autodoc2_packages = [
    "../src/extended_data_types",
]

templates_path = ["_templates"]

# Source suffixes for both reStructuredText and Markdown files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Default role
default_role = "any"

# HTML output settings
html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]

html_context = {
    "display_github": True,
    "github_user": "jbcom",
    "github_repo": "extended-data-types",
    "github_version": "main",
}

html_logo = "_static/logo.png"

html_permalinks_icon = "<span>⚓</span>"

# Nitpick ignore for unresolved references
nitpick_ignore = [
    ("py:class", "FilePath"),
    ("py:class", "ObjectProxy"),
    ("py:class", "yaml.SafeDumper"),
    ("py:class", "yaml.SafeLoader"),
    ("py:obj", "wrapt.ObjectProxy"),
    ("py:obj", "yaml.SafeDumper"),
    ("py:obj", "yaml.SafeLoader"),
]

nitpick_ignore_regex = [
    ("py:class", r"Safe.*"),
    ("py:class", r".*Node"),
    ("py:class", r"yaml\..*\.Safe.*"),
    ("py:obj", r"extended_data_types\.yaml_utils\..*\.Pure.*"),
    ("py:obj", r"extended_data_types\.yaml_utils\.tag_classes\..*.__init__"),
]

# Intersphinx configuration to link to Python standard library documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Define alias paths
TYPE_ALIASES = {
    "FilePath": "extended_data_types.file_data_type.",
}


def keep_only_data(soup: BeautifulSoup):
    def has_children(tag: Tag, txt1: str, txt2: str):
        if tag.name != "dt":
            return False

        # Get the prename and name elements of the signature
        ch1 = tag.select_one("span.sig-prename.descclassname span.pre")
        ch2 = tag.select_one("span.sig-name.descname span.pre")

        return ch1 and ch2 and ch1.string == txt1 and ch2.string == txt2

    for alias, module in TYPE_ALIASES.items():
        if dt := soup.find("dt", id=f"{module}{alias}"):
            # Copy class directive's a
            a = dt.find("a").__copy__()
            dt.parent.decompose()
        else:
            continue

        if dt := soup.find(lambda tag: has_children(tag, module, alias)):
            # ID and a for data directive
            dt["id"] = f"{module}{alias}"
            dt.append(a)


def edit_html(app, exception):
    if app.builder.format != "html":
        return

    for pagename in app.env.found_docs:
        if not isinstance(pagename, str):
            continue

        with (Path(app.outdir) / f"{pagename}.html").open("r") as f:
            # Parse HTML using BeautifulSoup html parser
            soup = BeautifulSoup(f.read(), "html.parser")
            keep_only_data(soup)

        with (Path(app.outdir) / f"{pagename}.html").open("w") as f:
            # Write back HTML
            f.write(str(soup))


def setup(app):
    app.connect("build-finished", edit_html)
