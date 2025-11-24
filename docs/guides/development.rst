Development Workflow
====================

This guide covers the development workflow and release process for Extended Data Types.

For detailed contributor and AI agent guidelines, see the `AGENTS.md <https://github.com/jbcom/extended-data-types/blob/main/AGENTS.md>`_ file in the repository root.

Project Structure & Modules
----------------------------

- **Source**: Lives in ``src/extended_data_types/`` with subpackages for serialization, transformations, compat, and CLI commands.
- **Tests**: Live in ``tests/`` mirroring the package layout (e.g., ``tests/serialization/...``, ``tests/transformations/...``).
- **Virtualenv**: Expected at ``.venv/``; use its binaries for tooling (``.venv/bin/python3.14``, ``.venv/bin/pytest``).
- **Documentation**: RST files in ``docs/`` directory, built with Sphinx.

Build, Test, and Development Commands
---------------------------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    # Install dependencies (prefer existing venv; avoid global installs)
    .venv/bin/pip install -e .

Testing
~~~~~~~

.. code-block:: bash

    # Run all tests
    .venv/bin/pytest -q

    # Run specific test suites
    .venv/bin/pytest tests/serialization -q
    .venv/bin/pytest tests/transformations/numbers -q
    .venv/bin/pytest tests/transformations/strings -q

    # Run with pattern matching
    .venv/bin/pytest -k <pattern>

Code Quality
~~~~~~~~~~~~

.. code-block:: bash

    # Format code
    black src tests

    # Run linter
    ruff check src tests

    # Type checking
    mypy src

Coding Style & Naming
---------------------

- **Language**: Python with type annotations; follow PEP 8 with 4-space indentation.
- **Naming**: Use descriptive names; prefer explicit imports over wildcards.
- **Modules**: Keep modules small and mirrored by tests.
- **Comments**: Inline comments only for non-obvious logic; keep docstrings short and imperative.
- **Encoding**: No trailing whitespace; default to ASCII unless existing code uses Unicode.
- **Imports**: Use absolute imports throughout the codebase (no relative imports).

Testing Guidelines
-------------------

- **Framework**: ``pytest`` with plain assertions; tests mirror package paths.
- **Naming**: Name tests descriptively (``test_<behavior>.py``; functions ``test_*``).
- **Coverage**: Keep new helpers covered; for regressions add focused tests beside existing ones.
- **Formats/Parsers**: When adding formats/parsers, ensure round-trip tests and import/export paths are exercised.
- **Stability**: Maintain stable output formatting; indentation and ordering are asserted in tests.

Commit & Pull Request Guidelines
----------------------------------

Commits
~~~~~~~

- **Format**: Concise, present-tense summaries (e.g., "Fix HCL2 serializer indentation").
- **Grouping**: Group related changes together.
- **Conventional Commits**: Follow conventional commits format for semantic-release:
  - ``feat:`` for new features
  - ``fix:`` for bug fixes
  - ``docs:`` for documentation changes
  - ``refactor:`` for code refactoring
  - ``test:`` for test changes
  - ``chore:`` for maintenance tasks

Pull Requests
~~~~~~~~~~~~~

- **Summary**: Include a short summary of changes.
- **Testing**: List test commands run (``.venv/bin/pytest -q``).
- **Edge Cases**: Document any edge cases or known gaps.
- **Issues**: Link related issues when applicable.
- **Scope**: Avoid large mixed changes; prefer separate commits/PRs for refactors vs. features vs. fixes.

Release Architecture
--------------------

Overview
~~~~~~~~

Extended Data Types uses a **single-workflow, tag-only release** process. Releases are automatically triggered when code is merged to the ``main`` branch, provided all CI checks pass.

Release Flow
~~~~~~~~~~~~

1. Developer creates PR
2. PR merged to main
3. CI workflow triggers:
   - build-package (creates "Packages" artifact)
   - tests (all Python versions in parallel)
   - typechecking
   - linting
   - coverage
   - [ALL PASS] → release job (main branch only)
     - semantic-release: Calculate version, create tag
     - Create GitHub Release
     - Build signed packages ("Packages-signed" artifact)
   - publish job (if release occurred)
     - Upload to PyPI

Key Configuration
~~~~~~~~~~~~~~~~~

**semantic-release settings** (``.github/workflows/ci.yml``):
- ``commit: false`` - Don't create version bump commits
- ``tag: true`` - Create Git tags
- ``push: false`` - Don't push to repository
- ``changelog: false`` - Don't create changelog commits
- ``vcs_release: true`` - Create GitHub releases
- ``build: false`` - Don't build (we use hynek's action)

**Build artifacts**:
- ``Packages``: Unsigned builds for CI testing
- ``Packages-signed``: Signed builds with attestations for PyPI

Design Decisions
~~~~~~~~~~~~~~~~

No Version Bump Commits
^^^^^^^^^^^^^^^^^^^^^^^

**Rationale**:
1. **Branch Protection**: Main branch has protection rules requiring status checks. Version bump commits haven't passed checks yet, creating a catch-22.
2. **Efficiency**: Version bump commits would trigger double CI runs, wasting resources.
3. **Git Tags as Source of Truth**: Build tools can extract version from git tags; PyPI packages are tagged correctly.

**Trade-offs**:
- ✅ No branch protection conflicts
- ✅ Single CI run per release
- ✅ Simpler workflow
- ⚠️ Version in ``__init__.py`` may lag behind latest release (acceptable)

Consolidated Workflow
^^^^^^^^^^^^^^^^^^^^^^

Single ``ci.yml`` workflow handles both CI and releases, eliminating ``workflow_run`` delays and ensuring all jobs use the same checkout SHA.

Separate Signed Artifacts
^^^^^^^^^^^^^^^^^^^^^^^^^^

- CI creates unsigned "Packages" for testing
- Release creates signed "Packages-signed" for PyPI
- Clear separation of test vs. production builds

Version Management
-------------------

How Versions Work
~~~~~~~~~~~~~~~~~

1. **Git Tags**: Authoritative version source
   - Created by semantic-release based on commit messages
   - Example: ``v5.1.3``

2. **PyPI Packages**: Built from tagged commits
   - Package metadata uses git tag version
   - Correct version appears on PyPI

3. **Source Files**: May lag behind
   - ``src/extended_data_types/__init__.py``: May show older version
   - Latest PyPI: Has correct version
   - This is acceptable for public distribution

Version Lag Rationale
~~~~~~~~~~~~~~~~~~~~~~

1. **Primary Distribution**: PyPI (has correct version)
2. **Source Builds**: Rare, users typically install from PyPI
3. **Documentation**: Can reference git tags for latest version
4. **Developer Clarity**: git tags always show true version

Troubleshooting Releases
~~~~~~~~~~~~~~~~~~~~~~~~

**Release doesn't trigger**:
- Check commit messages follow conventional commits format
- Ensure push is to ``main`` branch
- Verify all tests/lint/coverage pass

**Artifact conflicts**:
- Ensure ``upload-name-suffix: "-signed"`` is set in release job
- Check both artifacts appear in workflow run

**Wrong version on PyPI**:
- Verify git tag was created correctly
- Check semantic-release output for version calculation
- Ensure tag follows semver format

Agent-Specific Notes
---------------------

Environment Setup
~~~~~~~~~~~~~~~~~

- **Branch**: Current work should be specified in handoff notes
- **Python**: Use ``.venv/bin/python3.14`` and ``.venv/bin/pytest`` from virtualenv
- **Dependencies**: Honor existing virtualenv; do not upgrade tooling without discussion

Backward Compatibility
~~~~~~~~~~~~~~~~~~~~~~

- **Legacy APIs**: Maintain backward compatibility for legacy APIs (<=5.x) when touching transformations or serialization
- **Shims**: Add shims rather than removing surfaces
- **No Breaking Changes**: Never drop <=5 APIs; if functionality is unknown, prefer a no-op or pass-through that keeps the surface area intact

Code Organization
~~~~~~~~~~~~~~~~~

- **Module Structure**: Keep implementation code in proper module files, not in ``__init__.py``
- **Imports**: Use absolute imports throughout (e.g., ``from extended_data_types.serialization.registry import register_serializer``)
- **Serializers**: Format-specific serializers live in ``src/extended_data_types/serialization/formats/`` submodules

Testing Requirements
~~~~~~~~~~~~~~~~~~~~

- **Stability**: Keep CLI output stable; indentation and ordering are asserted in tests
- **Coverage**: Maintain test coverage; all new code should have corresponding tests
- **Regression**: When fixing bugs, add focused tests to prevent regressions

Dependencies
~~~~~~~~~~~~

- **Required**: All dependencies must be listed in ``pyproject.toml``
- **Optional**: Handle optional dependencies gracefully (e.g., babel for currency formatting)
- **No New Dependencies**: Avoid adding new dependencies unless absolutely necessary

Common Patterns
~~~~~~~~~~~~~~~

- **Type Checking**: Use strict type checking; ensure all functions have proper type annotations
- **Error Handling**: Raise appropriate exceptions (``ValueError``, ``TypeError``, etc.) with clear messages
- **Validation**: Validate inputs early; provide helpful error messages
- **Formatting**: Maintain consistent formatting across serialization formats

References
-----------

- **Semantic Release**: https://python-semantic-release.readthedocs.io/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **PEP 8**: https://pep8.org/
- **Project Repository**: https://github.com/jbcom/extended-data-types
- **Documentation**: https://jbcom.github.io/extended-data-types/
