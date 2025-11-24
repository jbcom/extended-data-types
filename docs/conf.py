import os

project = "Extended Data Types"
author = "Jon Bogaty"
copyright = f"2025, {author}"
version = "5.1.0"

extensions = [
    "autodoc2",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

suppress_warnings = [
    "misc.highlighting_failure",
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

# Type aliases for documentation
autodoc_type_aliases = {
    "FilePath": "extended_data_types.file_data_type.FilePath",
    "ReturnType": "extended_data_types.file_operations.ReturnType",
    "VT": "extended_data_types.map_data_type.VT",
    "KT": "extended_data_types.map_data_type.KT",
}

# Essential ignores for external dependencies
nitpick_ignore = [
    ("py:class", "git.Repo"),
    ("py:obj", "orjson"),
    ("py:obj", "wrapt.ObjectProxy"),
    ("py:obj", "yaml.SafeDumper"),
    ("py:obj", "yaml.SafeLoader"),
    ("py:class", "yaml.Node"),
    ("py:class", "yaml.ScalarNode"),
    ("py:class", "yaml.MappingNode"),
    ("py:obj", "defaultdict"),
    ("py:class", "extended_data_types.file_data_type.FilePath"),
    ("py:class", "extended_data_types.map_data_type.VT"),
    ("py:class", "extended_data_types.file_operations.ReturnType"),
]

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sortedcontainers": ("https://grantjenks.com/docs/sortedcontainers/", None),
    "ruamel.yaml": ("https://yaml.readthedocs.io/en/latest/", None),
}
