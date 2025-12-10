# Active Context

## extended-data-types

Extended data type utilities for Python with transformations and helpers.

### Features
- **Serialization**: YAML (with custom tags), JSON (via orjson), TOML, HCL2
- **File Operations**: Path resolution, Git repository detection, encoding detection
- **Data Structures**: Deep merging, flattening, filtering for maps and lists
- **String Transformations**: Case conversion, pluralization, humanization
- **Type Utilities**: Safe type conversion, special type handling, validation
- **Export Utilities**: Format-aware data export with GitHub Actions syntax escaping

### Package Status
- **Registry**: PyPI
- **Python**: 3.9+
- **Version**: 5.2.1
- **Tests**: 302 test cases, 85.72% coverage
- **Functions**: 90+ public functions in `__all__`

### Development
```bash
uv sync --extra tests
uv run pytest tests/ -v
uvx ruff check src/ tests/
uvx ruff format src/ tests/
uvx mypy src/
```

### Outstanding Work

#### Local Commits (4 ahead of origin/main)
```
2328d3d chore: centralize AI agent instructions with Ruler
0c5055e Remove Kiro MCP settings
b7d12eb fix(edt): remove inappropriate ecosystem-specific imports from public API
86b2ea1 feat(edt): add comprehensive ecosystem foundation specification
```
These need to be moved to a feature branch and merged via PR. See issue #62.

#### MCP Server Development (Issue #61)
Design an MCP server similar to Context7 that provides:
- `resolve-function-id` - Search for functions by name/description
- `get-function-docs` - Get comprehensive documentation for a function

The server should expose all 90+ functions organized by category:
- Serialization (9 functions)
- File Operations (10 functions)
- Git Integration (4 functions)
- String Transformations (9 functions)
- String Utilities (8 functions)
- Map Operations (10 functions)
- List Operations (4 functions)
- State Utilities (8 functions)
- Type Utilities (15 functions)
- Matcher Utilities (2 functions)
- Stack Utilities (6 functions)
- Export/Import (3 functions)
- Data Types (2 classes)

#### Ecosystem Foundation (Issue #63)
Full spec in `.kiro/specs/ecosystem-foundation/` covering:
- Package Discovery component
- Release Coordination component
- Ecosystem Status component
- Development Integration component

### Key Files
- `src/extended_data_types/__init__.py` - Public API exports
- `.kiro/specs/ecosystem-foundation/` - Ecosystem foundation spec
- `.ruler/` - AI agent instruction sources

---
*Last updated: 2025-12-10*
