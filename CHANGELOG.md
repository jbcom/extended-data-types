# CHANGELOG


## v5.1.2 (2025-11-23)

### Bug Fixes

- Add missing ruamel.yaml>=0.18.0 dependency
  ([`36d88d5`](https://github.com/jbcom/extended-data-types/commit/36d88d5ae260434e2c7feb71fe2a24829244296f))

This release fixes a critical dependency issue where `ruamel.yaml` was being used in `export_utils.py` but was not declared as a project dependency, causing `ModuleNotFoundError` in downstream packages.

### Changes

- Added `ruamel.yaml>=0.18.0` to project dependencies in `pyproject.toml`
- Updated Python version to 3.12 in development configuration
- Fixed ModuleNotFoundError in export_utils when using YAML export functionality

This resolves compatibility issues with lifecyclelogging and other downstream packages that depend on extended-data-types.

**Note**: This version was released on GitHub but not published to PyPI due to the release being created outside the automated workflow. The latest version available on PyPI remains 5.1.0.


## v5.1.0 (2025-11-23)

### Features

- Add make_raw_data_export_safe utility function
  ([`13b7f25`](https://github.com/jbcom/extended-data-types/commit/13b7f2573bda622c0e0420996d767c4d10f42723))

## What's Added

New function in that recursively converts complex types to export-safe primitives:

- datetime.date/datetime.datetime → ISO format strings - pathlib.Path → strings - YAML mode: applies
  GitHub Actions syntax escaping + literal strings for multiline

## Use Cases

1. **Datetime handling**: Convert date/datetime objects before JSON/YAML export 2. **Path
  normalization**: Ensure Path objects become strings 3. **YAML formatting**: Apply literal string
  format for multiline/command strings 4. **GitHub Actions**: Escape ${{ }} syntax automatically

## Example

```python from extended_data_types import make_raw_data_export_safe from datetime import datetime
  from pathlib import Path

data = { 'created': datetime(2025, 1, 1), 'log_path': Path('/var/log/app.log'), 'script': 'echo
  line1\necho line2' }

safe = make_raw_data_export_safe(data, export_to_yaml=True) # Result: # { # 'created':
  '2025-01-01T00:00:00', # 'log_path': '/var/log/app.log', # 'script': LiteralScalarString('echo
  line1\necho line2') # } ```

## Why This Matters

This function was implemented in terraform_modules/utils.py but belongs in extended-data-types as a
  core utility. Now available to all users.

Fixes: Circular import issues in terraform_modules

Closes: N/A

- Support tuples in make_raw_data_export_safe
  ([`e8e8906`](https://github.com/jbcom/extended-data-types/commit/e8e890648008f48d761f6637d9c218360adb1c6c))

Co-authored-by: jon <jon@jonbogaty.com>


## v5.0.3 (2025-01-28)

### Bug Fixes

- Coverage, linting, and typechecking in ci
  ([`b3ec354`](https://github.com/jbcom/extended-data-types/commit/b3ec354e46a16e012044e180de34733a9628052e))


## v5.0.2 (2025-01-28)

### Bug Fixes

- Ci improvements
  ([`ed816b7`](https://github.com/jbcom/extended-data-types/commit/ed816b72c558374617a8b337a55b288fb9f3ae9f))


## v5.0.1 (2025-01-28)

### Bug Fixes

- Pipeline issues
  ([`f86c139`](https://github.com/jbcom/extended-data-types/commit/f86c139312eddf57ca4725eda1e9cea4a59cb44b))

### Continuous Integration

- Improvements to testing
  ([`0433562`](https://github.com/jbcom/extended-data-types/commit/04335629a52cdb0710e5e16a950244f678304c0c))

* Streamlined tox configuration and CI / CD workflows * Ensured coverage reporting works both
  locally and in CI environment


## v5.0.0 (2025-01-27)

### Features

- Python 3.13 support, CI/CD improvements
  ([`2c48d9a`](https://github.com/jbcom/extended-data-types/commit/2c48d9afbbb7ab2b7dc947d8e81326c5d21d8de2))

* Improvements to structure for CI / CD and documentation * Support for Python 3.13 * Additional
  methods in stack_utils and map_utils


## v3.0.0 (2025-01-27)

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


## v1.0.0 (2025-01-27)

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
