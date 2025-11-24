Extended Data Types
=================

.. image:: _static/logo.png
   :alt: Extended Data Types Logo
   :align: center

*🐍 Supercharge your Python data types! 🚀*

Extended Data Types is a Python library that provides additional functionality for Python's standard data types.

Features
--------

- 🔒 **Base64 encoding and decoding** - Easily encode data to Base64 format
- 📁 **File path utilities** - Manipulate and validate file paths
- 🗄️ **Git operations** - Comprehensive Git repository management
- 🔍 **String matching** - Advanced string manipulation and validation
- 🎛️ **YAML utilities** - Handle custom YAML tags and data structures

Documentation
------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   installation
   overview
   guides/contributing
   guides/development
   guides/advanced_usage
   guides/testing
   guides/performance
   guides/security
   guides/deployment
   guides/yaml_utils

Quick Start
----------

Installation:

.. code-block:: bash

   pip install extended-data-types

Basic usage:

.. code-block:: python

   from extended_data_types import (
       FilePath,
       read_file,
       get_parent_repository,
       decode_yaml
   )

   # File operations
   content = read_file("config.yaml")

   # Git operations
   repo = get_parent_repository()
   if repo:
       print(f"Current branch: {get_current_branch(repo)}")

   # YAML handling
   data = decode_yaml(content)

Indices and Tables
----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
