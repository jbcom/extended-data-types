# Extended Data Types - AI Agent Instructions

This is the central source of truth for AI agent instructions in this repository.
Rules defined here are distributed to all supported AI coding assistants via Ruler.

## Project Overview

Extended Data Types is a Python utility library providing enhanced functionality for working with common data formats and types. It serves as a reliable, typed utility layer for Python applications.

### Core Purpose

- **Serialization utilities**: Safe, typed helpers for YAML, JSON, TOML, HCL, and Base64
- **File system operations**: Platform-aware path handling, Git discovery, encoding detection
- **Data structure manipulation**: Enhanced list and dictionary operations
- **String transformations**: Case conversion, humanization, pluralization
- **Type utilities**: Safe type conversion and validation

### Key Design Principles

- **Type safety**: Full type annotations and mypy compliance
- **Reliability**: Comprehensive test coverage with automated CI/CD
- **Ergonomics**: Clean, intuitive APIs
- **Platform awareness**: Handles cross-platform differences gracefully
- **Production ready**: No shortcuts, placeholders, or experimental features

## Technology Stack

- **Package manager**: `uv` (fast, Rust-based)
- **Build backend**: `hatchling`
- **Configuration**: `pyproject.toml`
- **Python versions**: 3.9+
- **Linting & formatting**: `ruff`
- **Type checking**: `mypy` (strict mode)
- **Testing**: `pytest`
- **CI/CD**: GitHub Actions with semantic-release
