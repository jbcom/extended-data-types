# Documentation Guidelines

This directory contains Sphinx documentation for `extended_data_types`.

## Structure

```
docs/
├── _static/              # Static assets (CSS, images)
├── _templates/           # Sphinx templates
├── api/                  # API reference (auto-generated)
├── development/          # Development guides
├── getting-started/      # User guides
├── conf.py               # Sphinx configuration
├── index.rst             # Documentation home
└── Makefile              # Build commands
```

## Building Documentation

```bash
# Build HTML docs
cd docs && make html

# Or using tox
tox -e docs

# View locally
open _build/html/index.html
```

## Writing Documentation

### File Formats

- `.rst` - reStructuredText (preferred for API docs)
- `.md` - Markdown (preferred for guides, enabled via MyST)

### Docstrings

Documentation is auto-generated from Google-style docstrings:

```python
def function_name(param: type) -> return_type:
    """Short description.

    Longer description with details about behavior.

    Args:
        param: Description of the parameter.

    Returns:
        Description of what is returned.

    Raises:
        ValueError: When param is invalid.

    Example:
        >>> function_name("input")
        "output"
    """
```

### Cross-References

Link to other parts of the documentation:

```rst
# RST
See :func:`extended_data_types.decode_yaml` for YAML parsing.
See :class:`extended_data_types.FilePath` for file handling.

# Markdown (MyST)
See {func}`extended_data_types.decode_yaml` for YAML parsing.
```

### Code Examples

Include runnable examples:

```rst
.. code-block:: python

    from extended_data_types import decode_yaml

    data = decode_yaml("key: value")
    print(data)  # {'key': 'value'}
```

### Admonitions

Use admonitions for important notes:

```rst
.. note::
   This is a note.

.. warning::
   This is a warning.

.. deprecated:: 5.0
   Use :func:`new_function` instead.
```

## API Documentation

API docs are auto-generated from source code docstrings.

### Adding New Modules

1. Ensure module has proper docstrings
2. Add to `api/` directory if needed
3. Reference in `index.rst` toctree

### Updating

After adding new public functions:

```bash
# Rebuild autosummary stubs
sphinx-autogen docs/api/*.rst
```

## Style Guide

- Write for users, not developers
- Lead with common use cases
- Include code examples for every function
- Keep paragraphs short
- Use active voice
