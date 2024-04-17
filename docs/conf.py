import os
import sys

# Add the path to your module
sys.path.insert(0, os.path.abspath('../extended_data_types'))

# Project information
project = 'extended-data-types'
author = 'Jon Bogaty'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'autodoc2',
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "tests"]

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Napoleon settings
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

# sphinx-autodoc2 settings
autodoc2_packages = [
    {
        "path": "../extended_data_types"
    }
]

# Render docstrings as reStructuredText
autodoc2_docstring_parser_regexes = [
    (r".*", "rst"),
]
