import os

project = "Extended Data Types"
author = "Jon Bogaty"
copyright = f"2025, {author}"
version = "5.0.2"

extensions = [
    "autodoc2",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

autodoc2_packages = [
    "../src/extended_data_types",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Default role
default_role = "py:obj"

# HTML output settings
html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

if os.environ.get("READTHEDOCS", "") == "True":
    html_context = {"READTHEDOCS": True}
else:
    html_context = {
        "display_github": True,
        "github_user": "jbcom",
        "github_repo": "extended-data-types",
        "github_version": "main",
    }

html_logo = "_static/logo.png"

html_permalinks_icon = "<span>⚓</span>"

autodoc_typehints = "description"
autodoc_typehints_format = "fully-qualified"  # Add this line
autodoc_type_aliases = {
    "FilePath": "extended_data_types.file_data_type.FilePath",
}

nitpick_ignore = [
    ("py:class", "git.Repo"),
    ("py:class", "ObjectProxy"),
    ("py:class", "yaml.SafeDumper"),
    ("py:class", "yaml.SafeLoader"),
    ("py:obj", "wrapt.ObjectProxy"),
    ("py:obj", "yaml.SafeDumper"),
    ("py:obj", "yaml.SafeLoader"),
    ("py:obj", "orjson"),
    ("py:obj", "defaultdict"),
    ("py:class", "extended_data_types.map_data_type.VT"),
    ("py:class", "extended_data_types.map_data_type.KT"),
]

nitpick_ignore_regex = [
    ("py:class", r"Safe.*"),
    ("py:class", r".*Node"),
    ("py:class", r"yaml\..*\.Safe.*"),
    ("py:obj", r"extended_data_types\.yaml_utils\..*\.Pure.*"),
    ("py:obj", r"extended_data_types\.yaml_utils\.tag_classes\..*.__init__"),
    ("py:obj", r"orjson"),
    (r"py:.*", r"extended_data_types\.file_data_type\.FilePath"),
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sortedcontainers": ("https://grantjenks.com/docs/sortedcontainers/", None),
}
