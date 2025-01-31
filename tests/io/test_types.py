"""Tests for I/O type definitions."""

from __future__ import annotations

import os
from pathlib import Path

from extended_data_types.io.types import EncodingType, FilePath


def test_file_path_type():
    """Test FilePath type compatibility."""
    # These assignments should type-check
    path1: FilePath = "string/path"
    path2: FilePath = Path("path/object")
    path3: FilePath = os.fspath("os/path")
    
    # Just assert they exist to satisfy pytest
    assert path1
    assert path2
    assert path3

def test_encoding_type():
    """Test EncodingType literal values."""
    # These assignments should type-check
    encoding1: EncodingType = "yaml"
    encoding2: EncodingType = "json"
    encoding3: EncodingType = "toml"
    encoding4: EncodingType = "hcl"
    encoding5: EncodingType = "raw"
    
    # Just assert they exist to satisfy pytest
    assert encoding1
    assert encoding2
    assert encoding3
    assert encoding4
    assert encoding5 