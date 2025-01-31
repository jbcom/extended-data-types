Installation
===========

Requirements
-----------

Extended Data Types requires Python 3.8 or later.

Basic Installation
----------------

Install using pip:

.. code-block:: bash

    pip install extended-data-types

Or using poetry:

.. code-block:: bash

    poetry add extended-data-types

Optional Dependencies
------------------

Install with specific format support:

.. code-block:: bash

    # YAML support
    pip install extended-data-types[yaml]

    # All formats
    pip install extended-data-types[all]

Development Installation
---------------------

For development, install with testing dependencies:

.. code-block:: bash

    # Clone repository
    git clone https://github.com/jbcom/extended-data-types.git
    cd extended-data-types

    # Install with development dependencies
    pip install -e ".[tests,typing,docs]"

Verification
----------

Verify installation:

.. code-block:: python

    >>> import extended_data_types
    >>> print(extended_data_types.__version__)
    1.0.0

Next Steps
---------

- Read the :doc:`overview` for feature highlights
- Check the :doc:`getting_started` guide
- Review :doc:`api/index` for detailed documentation
