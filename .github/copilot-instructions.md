# GitHub Copilot Instructions for extended-data-types

## CI/CD Workflow - Read This First! 🚨

This repository uses a **unified CI workflow** in `.github/workflows/ci.yml`. This is the **REFERENCE IMPLEMENTATION** for all ecosystem repositories.

### ✅ What is CORRECT (Do not suggest changing):

1. **No `[tool.semantic_release]` in pyproject.toml** - Configuration is in workflow YAML
2. **`commit: false`** - We don't want automated version bump commits
3. **`changelog: false`** - Changelogs are managed manually for better quality
4. **`push: false`** - Tags are already in GitHub, no need to push back
5. **`build: false`** - We use `hynek/build-and-inspect-python-package` instead

### ❌ Do NOT Suggest:

- Adding semantic-release config to pyproject.toml
- Splitting ci.yml into multiple workflow files
- Enabling automatic changelog generation
- Changing release workflow parameters
- "Fixing" the artifact download action versions (both v4 and v6 are intentional)

## Code Guidelines

### Type Hints
Use modern type hints with `from __future__ import annotations`:
```python
# ✅ Good
from __future__ import annotations
from collections.abc import Mapping

def func(data: Mapping[str, Any]) -> dict[str, Any]:

# ❌ Avoid
from typing import Dict
def func(data: Dict[str, Any]) -> Dict[str, Any]:
```

### API Design
- Maintain backward compatibility
- Use descriptive function names
- Provide comprehensive docstrings
- Include type hints for all public APIs

### Testing
- Always run tests locally before suggesting changes
- Maintain 100% test coverage
- Test across Python 3.9-3.13
- Use pytest fixtures appropriately

## Utility Functions

When adding new utilities:
- Follow existing naming conventions
- Add comprehensive tests
- Update `__all__` in `__init__.py`
- Document with examples

## Version Management

Version is defined in `src/extended_data_types/__init__.py`:
```python
__version__ = "5.1.2"
```

DO NOT suggest automated version bumping. Semantic-release reads this for version detection but does not write back to it.

## Questions?

See `AGENTS.md` for detailed explanations of our workflow design. This is the REFERENCE implementation for all ecosystem repos.
