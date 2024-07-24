import os
import sys

from importlib import metadata


# Add the path to your module
sys.path.insert(0, os.path.abspath("../extended_data_types"))

# Project information
project = "Extended Data Types"
author = "Jon Bogaty"
release = metadata.version("extended_data_types")
version = release.rsplit(".", 1)[0]

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    html_context = {"READTHEDOCS": True}

# Suppress warnings for non-local image URIs
suppress_warnings = ["image.nonlocal_uri"]

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
]

templates_path = ['_templates']

autosummary_generate = True
autosummary_imported_members = True

exclude_patterns = ["_build"]

# Options for HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_context = {
    "display_github": True,
    "github_user": "jbcom",
    "github_repo": "extended-data-types",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# HTML theme options
html_theme_options = {
    "logo_only": True,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "white",
}

markdown_http_base = "https://extended-data-types.readthedocs.io/en/latest"

# Autodoc settings
autodoc_mock_imports = ["numpy", "yaml"]
autodoc_member_order = "bysource"
autodoc_inherit_docstrings = True
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# Napoleon settings for Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Source suffix for reStructuredText files
source_suffix = [".rst"]

# Default role
default_role = "any"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
}
