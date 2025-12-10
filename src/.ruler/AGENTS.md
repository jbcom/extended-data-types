# Source Code Guidelines

This directory contains the `extended_data_types` package source code.

## Module Organization

```
src/extended_data_types/
├── __init__.py              # Public API exports
├── py.typed                 # PEP 561 type marker
├── *_utils.py               # Utility modules
├── *_data_type.py           # Data type operations
├── *_transformations.py     # Transformation utilities
└── [category]/              # Organized subpackages
    ├── __init__.py
    └── *.py
```

## Categories

| Directory | Purpose |
|-----------|---------|
| `compat/` | Python version compatibility |
| `core/` | Core functionality |
| `inspection/` | Code introspection |
| `io/` | File I/O operations |
| `matching/` | Pattern matching |
| `serialization/` | Format serialization (JSON, YAML, etc.) |
| `structures/` | Data structure manipulation |
| `transformations/` | Data transformation |
| `types/` | Type conversion/validation |
| `validation/` | Data validation |
| `yaml_utils/` | YAML-specific utilities |

## Public API

All public exports are defined in `__init__.py`. When adding new functionality:

1. Implement in the appropriate module
2. Add to `__all__` in `__init__.py`
3. Add import statement in `__init__.py`

## Module Conventions

### File Naming

- `*_utils.py` - Standalone utility functions
- `*_data_type.py` - Type-specific operations (file, list, map, string)
- `*_transformations.py` - Data transformation functions

### Required Headers

Every module must start with:

```python
from __future__ import annotations
```

### Import Style

```python
# Absolute imports only
from extended_data_types.serialization.yaml import YamlProcessor

# Never relative imports
from .yaml import YamlProcessor  # Wrong!
```

### Type Annotations

All public functions require complete type hints:

```python
def process_data(
    items: list[dict[str, Any]],
    *,
    validate: bool = True,
) -> dict[str, int]:
    """Process items with validation."""
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param: type) -> return_type:
    """Short description.

    Longer description if needed.

    Args:
        param: Description of parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param is invalid.
    """
```
