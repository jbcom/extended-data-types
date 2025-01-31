Contributing
===========

Thank you for considering contributing to Extended Data Types! This guide will help you get started.

Development Setup
--------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/jbcom/extended-data-types.git
       cd extended-data-types

2. Create a virtual environment:

   .. code-block:: bash

       python -m venv .venv
       source .venv/bin/activate  # Linux/macOS
       # or
       .venv\Scripts\activate  # Windows

3. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[tests,typing,docs]"

Code Style
---------

We use several tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run the quality checks:

.. code-block:: bash

    # Format code
    black src tests

    # Run linter
    ruff check src tests

    # Type checking
    mypy src

Testing
------

We use pytest for testing. Run the test suite:

.. code-block:: bash

    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=extended_data_types

    # Run specific test file
    pytest tests/test_yaml_utils.py

Documentation
-----------

Build the documentation locally:

.. code-block:: bash

    # Install docs dependencies
    pip install -e ".[docs]"

    # Build documentation
    cd docs
    make html

The built documentation will be in ``docs/_build/html``.

Pull Request Process
-----------------

1. Create a new branch for your feature:

   .. code-block:: bash

       git checkout -b feature-name

2. Make your changes and commit them:

   .. code-block:: bash

       git add .
       git commit -m "Description of changes"

3. Push to your fork:

   .. code-block:: bash

       git push origin feature-name

4. Open a Pull Request on GitHub

Best Practices
------------

1. **Code Quality**

   - Write clear, documented code
   - Include type hints
   - Follow PEP 8 guidelines

2. **Testing**

   - Write unit tests for new features
   - Maintain test coverage
   - Test edge cases

3. **Documentation**

   - Update relevant documentation
   - Include docstrings
   - Add examples when appropriate

4. **Git Commits**

   - Write clear commit messages
   - Keep commits focused
   - Reference issues when applicable
