# Project Structure

## Source Code Organization

```
src/extended_data_types/
├── __init__.py                 # Public API exports
├── py.typed                    # Type information marker
├── *_utils.py                  # Top-level utility modules
├── *_data_type.py             # Data type specific modules
├── *_transformations.py       # Transformation utilities
└── [category]/                # Organized by functionality
    ├── __init__.py
    └── *.py
```

## Module Categories

- **`compat/`**: Compatibility utilities for different Python versions
- **`core/`**: Core functionality and base classes
- **`inspection/`**: Code inspection and introspection utilities
- **`io/`**: Input/output operations and file handling
- **`matching/`**: Pattern matching and comparison utilities
- **`serialization/`**: Format-specific serialization (JSON, YAML, etc.)
- **`structures/`**: Data structure manipulation (lists, dicts, etc.)
- **`transformations/`**: Data transformation utilities
- **`types/`**: Type conversion and validation
- **`validation/`**: Data validation utilities
- **`yaml_utils/`**: YAML-specific functionality (legacy location)

## Testing Structure

Tests mirror the source structure exactly:

```
tests/
├── test_*.py                   # Direct module tests
└── [category]/                # Category-specific tests
    └── test_*.py
```

## Import Conventions

- **Public API**: Import from `extended_data_types` root
- **Internal imports**: Use absolute imports with full module path
- **Future annotations**: Always include `from __future__ import annotations`

```python
# ✅ Public usage
from extended_data_types import decode_yaml, encode_json

# ✅ Internal imports
from extended_data_types.serialization.yaml import YamlProcessor

# ✅ Required header
from __future__ import annotations
```

## File Naming Patterns

- **Utilities**: `*_utils.py` for standalone utility functions
- **Data types**: `*_data_type.py` for type-specific operations
- **Transformations**: `*_transformations.py` for data transformation
- **Tests**: `test_*.py` matching the source module name

## Ecosystem Integration

- **Foundational role**: This package forms the backbone of all jbcom Python packages
- **Local awareness**: Maintains knowledge of all Python repos in ~/src via GitHub API
- **MCP integration**: Provides stdio MCP server for downstream package integration
- **Hook coordination**: Bidirectional hooks for release coordination with dependent packages

## Key Files

- **`__init__.py`**: Defines public API via `__all__` exports
- **`py.typed`**: Indicates package includes type information
- **`pyproject.toml`**: Single source of configuration
- **`tox.ini`**: Multi-environment testing configuration
- **`.kiro/settings/mcp.json`**: MCP server configuration for ecosystem integration