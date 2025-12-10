# Technology Stack

## Build System & Package Management

- **Package manager**: `uv` (fast, Rust-based Python package manager)
- **Build backend**: `hatchling` (modern Python packaging)
- **Configuration**: `pyproject.toml` (single source of truth)
- **Python versions**: 3.9+ (supports modern type hints)

## Core Dependencies

- **Serialization**: `pyyaml`, `ruamel.yaml`, `orjson`, `tomlkit`, `python-hcl2`
- **Data structures**: `deepmerge`, `sortedcontainers`
- **String processing**: `inflection`, `num2words`, `validators`
- **File operations**: `gitpython`, `wrapt`
- **Type system**: `typing_extensions` (for older Python versions)

## Development Tools

- **Linting & formatting**: `ruff` (replaces black, isort, flake8, etc.)
- **Type checking**: `mypy` with strict mode enabled
- **Testing**: `pytest` with coverage reporting
- **Documentation**: `sphinx` with custom theme
- **CI/CD**: GitHub Actions with automated releases

## Local Agent Environment

- **Git operations**: Use `--no-pager` flag and `GIT_EDITOR=true` for non-interactive operations
- **GitHub CLI**: Pre-authenticated, no token required (unlike Cursor environment)
- **Rebasing**: Use `GIT_EDITOR=true git rebase` to avoid external editor spawning

## Common Commands

```bash
# Environment setup
uv sync --extra tests

# Development workflow
uv run pytest tests/ -v                    # Run tests
uv run pytest tests/ --cov=src/           # Run with coverage
uvx ruff check src/ tests/                # Lint code
uvx ruff format src/ tests/               # Format code
uvx mypy src/                             # Type check

# Git operations (local agent)
git --no-pager log --oneline -10          # View recent commits
GIT_EDITOR=true git rebase -i HEAD~3      # Interactive rebase without editor

# GitHub operations (pre-authenticated)
gh repo list jbcom --json name,primaryLanguage  # List org repos
gh issue list --label ecosystem           # Check ecosystem issues

# Build and release
uv build                                  # Build package
semantic-release --noop version --print   # Check release status
```

## Code Quality Standards

- **Coverage**: Minimum 75% test coverage required
- **Type safety**: Full mypy compliance in strict mode
- **Linting**: Zero ruff violations allowed
- **Documentation**: Google-style docstrings required
- **Testing**: pytest with comprehensive test suites

## Ecosystem Integration

- **Foundational package**: This is the backbone for all jbcom Python packages
- **Downstream coordination**: Hooks for coordinating releases to dependent packages
- **MCP server**: Provides stdio MCP server for API documentation and usage guidance
- **Local ecosystem**: Maintains awareness of all jbcom Python packages in ~/src

## Release Process

- **Versioning**: Semantic versioning with conventional commits
- **Automation**: Fully automated via semantic-release
- **Publishing**: PyPI with GitHub Actions
- **Scope**: Use `edt` for conventional commit scope
- **Ecosystem coordination**: Triggers downstream package updates when foundational changes occur