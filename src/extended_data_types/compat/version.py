"""Version compatibility helpers."""

from __future__ import annotations

import sys


def check_compatibility(
    min_major: int | None = None, min_minor: int | None = None
) -> bool:
    major, minor = sys.version_info[:2]
    if min_major is not None and major < min_major:
        return False
    if min_major is not None and major > min_major:
        return True
    if min_minor is not None and minor < min_minor:
        return False
    return True
