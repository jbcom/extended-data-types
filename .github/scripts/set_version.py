#!/usr/bin/env python3
# ruff: noqa: T201, D103, EM101, PTH123
"""Auto-version script: Updates version based on GitHub run number.

Uses CalVer format: YYYY.MM.BUILD_NUMBER
Example: 2025.11.42

This ensures:
- Every push to main gets a unique, incrementing version
- No manual version management needed
- No git tags required
- Always publishable to PyPI
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_init_file():
    """Find the __init__.py file with __version__."""
    src = Path("src")
    if not src.exists():
        raise FileNotFoundError("src/ directory not found")

    # Find all __init__.py files in src/
    for init_file in src.rglob("__init__.py"):
        content = init_file.read_text()
        if "__version__" in content:
            return init_file

    raise FileNotFoundError("No __init__.py with __version__ found in src/")


def main():
    # Get GitHub run number (always incrementing)
    run_number = os.environ.get("GITHUB_RUN_NUMBER", "0")

    # Generate CalVer: YYYY.MM.BUILD
    new_version = f"{now.year}.{now.month:02d}.{run_number}"
    new_version = f"{now.year}.{now.month}.{run_number}"

    # Find and update __init__.py
    init_file = find_init_file()
    content = init_file.read_text()

    # Replace version line
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("__version__"):
            lines[i] = f'__version__ = "{new_version}"'
            break

    init_file.write_text("\n".join(lines))

    # Output for GitHub Actions
    print(f"VERSION={new_version}")
    print(f"Updated version in {init_file}")

    # Set output for workflow
    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with open(github_output, "a") as f:
            f.write(f"version={new_version}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
