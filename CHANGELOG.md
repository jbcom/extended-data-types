# CHANGELOG


## v10.0.0 (2025-01-27)

### Features

- Python 3.13 support, CI/CD improvements
  ([`c147cf1`](https://github.com/jbcom/extended-data-types/commit/c147cf1afab6eb195166dc5d4021b66243f57cab))

* Improvements to structure for CI / CD and documentation * Support for Python 3.13 * Additional
  methods in stack_utils and map_utils


## v1.0.0 (2025-01-27)

### Features

- Adds reconstruction capabilities for converted data and several new type conversions from strings
  ([`b3b9b31`](https://github.com/jbcom/extended-data-types/commit/b3b9b3167bd695c75fdd7c8af2f3b06c4bf41876))

Strengthens conversion capabilities of the library greatly by adding bidirectional conversion /
  reconstruction of data

BREAKING CHANGE: Moving forward 3.8 will not be supported as it adds too much complexity maintaining
  backwards compatibility

### BREAKING CHANGES

- Moving forward 3.8 will not be supported as it adds too much complexity maintaining backwards
  compatibility


## v0.1.0 (2025-01-27)

### Features

- Initial commit establishing the extended-data-types project
  ([`b6b572f`](https://github.com/jbcom/extended-data-types/commit/b6b572fac6d0a4694e9c8dc3fda0d9b806f4b2e2))

This commit sets up the initial structure and configuration for the extended-data-types project,
  including the following key components:

- Added `pyproject.toml` with Poetry configuration, including project metadata, dependencies, and
  dynamic versioning setup. - Configured `pytest`, `pytest-mock`, `pytest-asyncio`, `ruff`, `mypy`,
  `sphinx`, and `sphinxawesome-theme` for development and documentation purposes. - Implemented
  dynamic versioning using `poetry-dynamic-versioning` with support for reading version from both
  SCM and file. - Set up semantic versioning with `commitizen`, including configuration for commit
  parsing, changelog generation, and release management. - Added initial utility functions and data
  structures for extended data types. - Configured GitHub Actions workflows for CI, including
  testing, coverage reporting, and publishing to PyPI and Test PyPI. - Added basic linting,
  formatting, and import sorting configurations using `ruff`. - Included the entire library
  implementation with comprehensive pytest tests for all components.

This commit lays the foundation for further development and ensures consistent versioning, release
  management, and testing
