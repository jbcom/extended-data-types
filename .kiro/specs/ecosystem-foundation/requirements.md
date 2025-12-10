# Requirements Document

## Introduction

This specification defines the transformation of extended-data-types from a standalone utility library into the foundational ecosystem package for all jbcom Python projects. Extended-data-types currently provides 80+ utility functions across serialization (YAML/JSON/TOML/HCL2), file operations, Git integration, string/number transformations, data structure manipulation, and type conversion. The transformation will add ecosystem awareness, release coordination, and MCP-based integration capabilities while preserving all existing functionality.

Current capabilities include:
- **Serialization**: YAML (with custom tags), JSON (via orjson), TOML, HCL2 encoding/decoding
- **File Operations**: Path resolution, Git repository detection, encoding detection, read/write with format auto-detection
- **Data Structures**: Deep merging, flattening, filtering for maps and lists, sorted collections
- **String Transformations**: Case conversion (snake_case, camelCase, kebab-case), pluralization, humanization
- **Type Utilities**: Safe type conversion, special type handling, validation
- **Export Utilities**: Format-aware data export with GitHub Actions syntax escaping

The ecosystem transformation will add:
- MCP server for API documentation and usage guidance
- Automated discovery of jbcom packages in ~/src
- Release coordination hooks for dependency management
- Local development environment integration

## Glossary

- **Extended_Data_Types**: The current utility library providing 80+ functions for data manipulation, serialization, and file operations
- **Ecosystem_Foundation**: The evolved package that adds ecosystem coordination capabilities to Extended_Data_Types
- **MCP_Server**: Model Context Protocol server providing stdio-based API documentation for all utility functions
- **Serialization_Utilities**: YAML, JSON, TOML, and HCL2 encoding/decoding functions with format auto-detection
- **File_Operations**: Path resolution, Git repository integration, encoding detection, and format-aware file I/O
- **Data_Transformations**: String case conversion, pluralization, number formatting, and data structure manipulation
- **Local_Ecosystem**: Collection of jbcom Python packages in ~/src directory for coordinated development
- **Downstream_Package**: Any jbcom Python package that depends on extended-data-types utilities
- **Release_Coordination**: Automated dependency management using semantic versioning and conventional commits
- **API_Surface**: The 80+ public functions exported via __all__ with complete type annotations
- **Development_Workflow**: uv-based environment with ruff/mypy/pytest and semantic-release automation

## Requirements

### Requirement 1

**User Story:** As a developer working on any jbcom Python package, I want access to a comprehensive MCP server that provides API documentation and usage guidance for extended-data-types utilities, so that I can efficiently discover and use the 80+ available functions.

#### Acceptance Criteria

1. WHEN a developer queries the MCP_Server for serialization functions THEN the system SHALL provide documentation for encode_yaml, decode_yaml, encode_json, decode_json, encode_toml, decode_toml, and decode_hcl2 with usage examples
2. WHEN a developer requests file operation help THEN the MCP_Server SHALL document read_file, write_file, decode_file, get_parent_repository, resolve_local_path, and match_file_extensions with parameter details
3. WHEN a developer asks about string transformations THEN the MCP_Server SHALL provide examples for to_snake_case, to_camel_case, pluralize, humanize, and other string utilities
4. WHEN the MCP_Server starts THEN the system SHALL load all 80+ functions from the __all__ exports with complete type signatures
5. WHERE a developer needs data structure help THEN the MCP_Server SHALL document deep_merge, flatten_map, filter_list, and collection utilities with practical examples

### Requirement 2

**User Story:** As the ecosystem maintainer, I want automated discovery and tracking of all jbcom Python packages in the local ~/src directory, so that I can coordinate releases and manage dependencies across the ecosystem.

#### Acceptance Criteria

1. WHEN the Ecosystem_Foundation scans ~/src THEN the system SHALL identify Python packages by detecting pyproject.toml files and package directories
2. WHEN analyzing package dependencies THEN the system SHALL parse pyproject.toml files to identify which packages depend on extended-data-types
3. WHEN a new jbcom package is cloned to ~/src THEN the system SHALL automatically detect it using file system monitoring or periodic scans
4. WHEN querying ecosystem status THEN the system SHALL provide current version information by reading pyproject.toml version fields and git tags
5. WHEN validating ecosystem health THEN the system SHALL check semantic version compatibility and identify packages with outdated extended-data-types dependencies

### Requirement 3

**User Story:** As the ecosystem maintainer, I want automated release coordination that leverages the existing semantic-release workflow, so that extended-data-types updates can be safely propagated to dependent packages.

#### Acceptance Criteria

1. WHEN extended-data-types releases a new version using semantic-release THEN the system SHALL analyze the conventional commit history to determine if changes affect public APIs
2. WHEN breaking changes are detected in serialization, file operations, or transformation utilities THEN the system SHALL generate migration guides with before/after examples
3. WHEN a minor version is released with new utility functions THEN the system SHALL notify downstream packages about available enhancements
4. WHEN coordinating releases THEN the system SHALL respect the existing CI/CD pipeline using GitHub Actions and PyPI publishing
5. WHERE API compatibility issues are detected THEN the system SHALL provide specific guidance on updating import statements and function calls

### Requirement 4

**User Story:** As a developer setting up a new jbcom Python package, I want standardized project templates that include extended-data-types and proper MCP configuration, so that I can immediately use serialization, file operations, and transformation utilities.

#### Acceptance Criteria

1. WHEN creating a new jbcom Python package THEN the system SHALL provide pyproject.toml templates with extended-data-types dependency and proper version constraints
2. WHEN setting up MCP integration THEN the system SHALL configure .kiro/settings/mcp.json with the extended-data-types MCP server entry
3. WHEN initializing the development environment THEN the system SHALL configure uv, ruff, mypy, and pytest to match the extended-data-types workflow
4. WHEN importing foundation utilities THEN the system SHALL provide type-safe access to all serialization, file, and transformation functions
5. WHERE project-specific needs arise THEN the system SHALL allow customization while maintaining compatibility with the ecosystem foundation

### Requirement 5

**User Story:** As a developer working across multiple jbcom packages, I want ecosystem status visibility and dependency management tools, so that I can maintain consistency and coordinate updates across all packages.

#### Acceptance Criteria

1. WHEN querying ecosystem status THEN the system SHALL provide a dependency graph showing which packages use extended-data-types and their version constraints
2. WHEN checking for updates THEN the system SHALL identify packages with outdated extended-data-types dependencies and suggest upgrade paths
3. WHEN performing bulk operations THEN the system SHALL support running uv sync, pytest, or ruff commands across multiple packages in ~/src
4. WHEN validating ecosystem health THEN the system SHALL detect version conflicts, missing dependencies, and incompatible constraints
5. WHERE cross-package changes are needed THEN the system SHALL provide tools to update import statements and function calls consistently

### Requirement 6

**User Story:** As a developer, I want the MCP server to provide comprehensive documentation for all extended-data-types utilities, so that I can quickly understand and use serialization, file operations, and transformation functions.

#### Acceptance Criteria

1. WHEN querying serialization functions THEN the MCP_Server SHALL document YAML utilities (encode_yaml, decode_yaml, LiteralScalarString, YamlTagged), JSON functions (encode_json with orjson options), TOML operations, and HCL2 decoding
2. WHEN requesting file operation help THEN the MCP_Server SHALL provide examples for read_file, write_file, decode_file with format auto-detection, Git repository functions, and path resolution utilities
3. WHEN exploring transformation utilities THEN the MCP_Server SHALL document string case conversion (to_snake_case, to_camel_case, to_kebab_case), pluralization, humanization, and number formatting
4. WHEN asking about data structures THEN the MCP_Server SHALL explain deep_merge, flatten_map, filter_list, SortedDefaultDict, and collection manipulation functions
5. WHERE type conversion is needed THEN the MCP_Server SHALL document convert_special_types, make_hashable, and safe type conversion utilities

### Requirement 7

**User Story:** As the ecosystem maintainer, I want integration with the existing GitHub CLI and Git workflows, so that ecosystem operations work seamlessly with the current development environment.

#### Acceptance Criteria

1. WHEN accessing GitHub repositories THEN the system SHALL use pre-authenticated gh commands without requiring additional token configuration
2. WHEN performing Git operations THEN the system SHALL leverage existing get_parent_repository, get_repository_name, and get_tld functions from extended-data-types
3. WHEN scanning for packages THEN the system SHALL use Git repository detection to identify jbcom packages in ~/src
4. WHEN validating ecosystem state THEN the system SHALL use git commands with GIT_EDITOR=true for non-interactive operation
5. WHERE repository operations are needed THEN the system SHALL integrate with the existing clone_repository_to_temp functionality

### Requirement 8

**User Story:** As a developer using extended-data-types utilities, I want comprehensive testing and CI/CD validation, so that I can rely on the 302 test cases and 85.72% coverage for production use.

#### Acceptance Criteria

1. WHEN running the test suite THEN the system SHALL execute 302 test cases covering all utility categories with minimum 75% coverage requirement (currently achieving 85.72%)
2. WHEN validating CI/CD pipeline THEN the system SHALL run tests on Python 3.9-3.13, perform ruff linting/formatting, and execute automated releases via semantic-release
3. WHEN testing serialization functions THEN the system SHALL validate round-trip compatibility for YAML (including LiteralScalarString, YamlTagged), JSON with orjson options, TOML, and HCL2 formats
4. WHEN verifying file operations THEN the system SHALL test read_file, write_file, decode_file with format auto-detection, Git repository functions, and cross-platform path resolution
5. WHERE transformation utilities are tested THEN the system SHALL validate string case conversion (snake_case, camelCase, kebab-case), pluralization, data structure manipulation (deep_merge, flatten_map), and type conversion functions

### Requirement 9

**User Story:** As the ecosystem maintainer, I want integration with the existing tox-based multi-environment testing and GitHub Actions CI/CD pipeline, so that ecosystem coordination works seamlessly with current development workflows.

#### Acceptance Criteria

1. WHEN running multi-environment tests THEN the system SHALL use tox with uv backend to test across Python 3.9-3.13 environments as configured in tox.ini
2. WHEN executing CI/CD pipeline THEN the system SHALL follow the existing GitHub Actions workflow with build, test, lint, and release jobs using hynek/build-and-inspect-python-package and semantic-release
3. WHEN performing code quality checks THEN the system SHALL use ruff for linting/formatting and mypy for type checking as configured in the current pipeline
4. WHEN coordinating releases THEN the system SHALL leverage the existing semantic-release automation with conventional commits, PyPI publishing, and GitHub release creation
5. WHERE ecosystem integration is needed THEN the system SHALL extend the current CI/CD pipeline without disrupting the established build, test, and release processes

### Requirement 10

**User Story:** As a developer working with the ecosystem foundation, I want comprehensive integration testing that validates the interaction between different utility categories, so that I can trust complex workflows involving multiple extended-data-types functions.

#### Acceptance Criteria

1. WHEN testing serialization workflows THEN the system SHALL validate end-to-end scenarios like reading files with decode_file, processing with transformation utilities, and exporting with make_raw_data_export_safe
2. WHEN validating Git integration THEN the system SHALL test workflows combining get_parent_repository, resolve_local_path, and file operations within actual Git repositories
3. WHEN testing data transformation pipelines THEN the system SHALL validate scenarios combining map operations (deep_merge, flatten_map), string transformations (case conversion), and type utilities (convert_special_types)
4. WHEN verifying export utilities THEN the system SHALL test complex scenarios with nested data structures containing datetime objects, Path instances, and GitHub Actions syntax requiring escaping
5. WHERE cross-platform compatibility is required THEN the system SHALL validate file operations, path resolution, and encoding detection across different operating systems in the CI matrix