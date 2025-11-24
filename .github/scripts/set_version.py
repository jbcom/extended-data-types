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
import re
import sys

from datetime import datetime, timezone
from pathlib import Path


def find_init_file():
    """Find the __init__.py file with a valid __version__ declaration."""
    src = Path("src")
    if not src.exists():
        raise FileNotFoundError("src/ directory not found")

    # Regex pattern to match __version__ assignment
    version_pattern = re.compile(r'^\s*__version__\s*=\s*["\'].*["\']')

    # Find all __init__.py files in src/
    for init_file in src.rglob("__init__.py"):
        content = init_file.read_text()
        # Check if file has an actual __version__ assignment line
        # Use same regex pattern as replacement logic to avoid false positives
        for line in content.splitlines():
            if version_pattern.match(line):
                return init_file

    raise FileNotFoundError("No __init__.py with __version__ found in src/")


def update_docs_version(new_version: str) -> None:
    """Update version in docs/conf.py."""
    docs_conf = Path("docs/conf.py")
    if not docs_conf.exists():
        # Docs config is optional - don't fail if it doesn't exist
        print("docs/conf.py not found, skipping docs version update")
        return

    content = docs_conf.read_text()
    lines = content.splitlines(keepends=True)

    # Match: version = "x.y.z" with optional spaces
    version_pattern = re.compile(r'^(\s*)version\s*=\s*["\'].*["\']')

    updated = False
    for i, line in enumerate(lines):
        match = version_pattern.match(line)
        if match:
            indent = match.group(1)
            remainder = line[match.end() :]
            lines[i] = f'{indent}version = "{new_version}"{remainder}'
            updated = True
            break

    if updated:
        docs_conf.write_text("".join(lines))
        print(f"Updated version in {docs_conf}")
    else:
        print(f"Warning: Could not find version assignment in {docs_conf}")


def main():
    # Get GitHub run number (always incrementing)
    run_number = os.environ.get("GITHUB_RUN_NUMBER", "0")

    # Get current date in UTC
    now = datetime.now(timezone.utc)

    # Generate CalVer: YYYY.MM.BUILD (with zero-padded month)
    new_version = f"{now.year}.{now.month:02d}.{run_number}"

    # Find and update __init__.py
    init_file = find_init_file()
    content = init_file.read_text()

    lines = content.splitlines(keepends=True)
    # Regex to match exactly "__version__" assignment, not __version_info__ or similar
    # Matches: __version__ = "..." or __version__="..." (with/without spaces)
    version_pattern = re.compile(r'^(\s*)__version__\s*=\s*["\'].*["\']')

    updated = False
    for i, line in enumerate(lines):
        match = version_pattern.match(line)
        if match:
            # Preserve original indentation
            indent = match.group(1)
            # Preserve everything after the closing quote (including newline)
            remainder = line[match.end() :]
            lines[i] = f'{indent}__version__ = "{new_version}"{remainder}'
            updated = True
            break

    if not updated:
        raise ValueError(f"Failed to update __version__ in {init_file}")

    init_file.write_text("".join(lines))

    # Update docs/conf.py version
    update_docs_version(new_version)

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
