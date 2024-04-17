import os
import sys

# Add the path to your module
sys.path.insert(0, os.path.abspath('../extended_data_types'))

# Project information
project = 'Extended Data Types'
author = 'Jon Bogaty'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_markdown_builder',
]

autosummary_generate = True
autosummary_imported_members = True

exclude_patterns = []

# Options for HTML output
html_theme = 'sphinx_rtd_theme'

html_context = {
    'display_github': True,
    'github_user': 'jbcom',
    'github_repo': 'extended-data-types',
    'github_version': 'main',
    'conf_py_path': '/docs/',
}

markdown_http_base = "https://extended-data-types.readthedocs.io/en/latest"

# Autodoc settings
autodoc_mock_imports = ["numpy", "yaml"]
autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = True
autodoc_typehints = 'description'

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
