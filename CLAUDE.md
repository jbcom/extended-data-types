# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Extended Data Types is a Python library that provides enhanced functionality for Python's standard data types. It offers utilities for handling YAML, JSON, TOML, HCL2, Base64, file paths, strings, lists, maps, and more. The project is in active development and has recently undergone a major architecture refactor (v5.0+), maintaining both legacy and modern APIs.

**Python Version**: Requires Python 3.10+

## Development Commands

### Environment Setup

```bash
# Install dependencies using uv (preferred)
uv sync

# Or using pip
pip install -e ".[tests,typing,docs]"

# Activate virtual environment
source .venv/bin/activate
```

### Running Tests

```bash
# Run all tests with coverage (uses pytest-xdist for parallel execution)
pytest -n auto --cov --cov=extended_data_types --cov-report=term-missing -vv

# Run a specific test file
pytest tests/core/test_dict.py -vv

# Run a specific test function
pytest tests/core/test_dict.py::test_extended_dict_basic -vv

# Run tests without coverage (faster for development)
pytest -n auto -vv

# Run tests for all Python versions using tox
tox

# Run tests for a specific Python version
tox -e py310
```

### Type Checking

```bash
# Type check with mypy (strict mode enabled)
mypy src

# Type check with pyright (used in CI)
tox -e pyright
```

### Linting and Formatting

```bash
# Format code with black
black .

# Lint and auto-fix with ruff
ruff check --fix
ruff format

# Run all pre-commit hooks
pre-commit run --all-files

# Or use tox
tox -e pre-commit
```

### Coverage Reports

```bash
# Generate coverage report locally
tox -e report

# View HTML coverage report
# Reports are generated in htmlcov/ directory
```

### Documentation

```bash
# Build documentation
tox -e docs

# Documentation is built to docs/_build/html/
```

## Architecture

### Dual API Design (v5.0+)

The codebase maintains **two parallel APIs** to ensure backward compatibility:

1. **Legacy API** (v4 and earlier): Module-level functions in root `*_utils.py` files
   - `base64_utils.py`, `json_utils.py`, `yaml_utils.py`, etc.
   - Simple function-based interface for common operations
   - Maintained for backward compatibility

2. **Modern API** (v5+): Object-oriented architecture under subpackages
   - `core/`: Enhanced collection types (`ExtendedDict`, `ExtendedList`, `ExtendedSet`)
   - `serialization/`: Pluggable serialization system with format registry
   - `transformations/`: Data transformation pipelines
   - `inspection/`: Type introspection and schema validation
   - `matching/`: Pattern matching utilities

Both APIs are fully supported and tested. The main `__init__.py` exports both for seamless use.

### Key Architectural Components

#### Core Collections (`src/extended_data_types/core/`)
- `ExtendedDict`, `ExtendedList`, `ExtendedSet`, `ExtendedFrozenSet`: Enhanced collection types
- `base.py`: Base class for all extended types
- `types.py`: Type conversion utilities (`strtoint`, `strtobool`, `strtodate`, etc.)
- `patterns.py`: Regex patterns for common data formats (dates, paths, numbers)

#### Serialization System (`src/extended_data_types/serialization/`)
- Format registry allowing custom serialization handlers
- Built-in support for: JSON (via orjson), YAML (via ruamel.yaml), TOML, HCL2
- Auto-format detection via `guess_format()`
- Type-aware serialization: handles dates, paths, and custom objects

#### Transformations (`src/extended_data_types/transformations/`)
- Functional transformation pipelines
- String case conversion (camelCase, snake_case, kebab-case, etc.)
- Number formatting (words, roman numerals, scientific notation)
- Collection operations (filtering, mapping, chaining)

#### File I/O (`src/extended_data_types/io/`)
- Path handling with encoding detection
- Git repository operations via GitPython
- Safe file operations with type preservation

#### CLI (`src/extended_data_types/cli/`)
- Command-line interface for format conversion and validation
- Uses Click framework
- Supports format conversion between YAML/JSON/TOML/HCL2

### Import Patterns

```python
# Legacy API (still supported)
from extended_data_types import decode_yaml, encode_json, flatten_map

# Modern API (recommended for new code)
from extended_data_types import ExtendedDict, get_serializer
from extended_data_types.serialization import serialize, deserialize
from extended_data_types.transformations import to_camel_case
```

## Testing Strategy

### Test Organization
- Tests mirror the `src/extended_data_types/` structure
- `tests/compat/`: Tests for legacy API compatibility
- `tests/core/`, `tests/serialization/`, etc.: Tests for modern API
- Comprehensive coverage requirement: 75% minimum (enforced in CI)

### Test Execution
- Parallel test execution via `pytest-xdist` (`-n auto`)
- Coverage tracking per Python version in CI
- Type checking in separate tox environment (mypy + pyright)
- Pre-commit hooks validate formatting, linting, and docstrings

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

1. **Package Build**: Build and verify package integrity
2. **Tests**: Run tests on Python 3.10, 3.11, 3.12, 3.13 (matrix)
3. **Type Checking**: Run pyright for strict type validation
4. **Linting**: Run pre-commit hooks (black, ruff, interrogate, codespell)
5. **Coverage**: Combine coverage from all Python versions, generate report
6. **Release**: Semantic versioning on main branch with signed attestation
7. **Publish**: Automatic PyPI publishing on successful release

## Configuration Files

- `pyproject.toml`: Project metadata, dependencies, and tool configurations
  - Black line length: 88
  - Ruff: Comprehensive linting with many rules enabled (see file for exceptions)
  - Mypy: Strict mode enabled
  - Coverage: 75% minimum, branch coverage enabled
- `tox.ini`: Test automation for multiple Python versions
- `.pre-commit-config.yaml`: Git hooks for code quality
- `uv.lock`: Locked dependencies (requires uv >= 0.5.0)

## Important Notes

### Type Handling
- The library handles special Python types (dates, paths, UUIDs) in serialization
- Use `convert_special_type()` and `reconstruct_special_type()` for custom type conversions
- YAML uses ruamel.yaml for round-trip preservation

### YAML Processing
- **BREAKING CHANGE in v5.0**: Switched from PyYAML to ruamel.yaml
- Preserves comments, formatting, and order
- Custom YAML tags supported via `yaml_utils/tag_classes.py`

### HCL2 Support
- Terraform configuration file format
- Bidirectional conversion: HCL2 ↔ Python dicts ↔ JSON/YAML
- Located in `serialization/languages/hcl2/`

### Git Operations
- `get_parent_repository()`: Find the root of a Git repository
- `clone_repository_to_temp()`: Clone repos to temporary locations
- Uses GitPython library

## Versioning

The project uses semantic versioning with automated releases:
- Version stored in `src/extended_data_types/__init__.py` as `__version__`
- Semantic release on main branch via python-semantic-release
- Conventional commit messages trigger version bumps
