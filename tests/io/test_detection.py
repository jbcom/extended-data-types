"""Tests for file type detection utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

from extended_data_types.io.detection import (get_encoding_for_file_path,
                                              is_config_file)


class TestGetEncodingForFilePath:
    """Tests for get_encoding_for_file_path function."""
    
    @pytest.mark.parametrize(
        "file_path,expected",
        [
            # YAML files
            ("config.yaml", "yaml"),
            ("config.yml", "yaml"),
            ("path/to/config.yaml", "yaml"),
            ("path/to/config.YML", "yaml"),
            
            # JSON files
            ("data.json", "json"),
            ("path/to/data.json", "json"),
            ("path/to/data.JSON", "json"),
            
            # HCL files
            ("main.tf", "hcl"),
            ("config.hcl", "hcl"),
            ("path/to/main.tf", "hcl"),
            ("path/to/config.HCL", "hcl"),
            
            # TOML files
            ("config.toml", "toml"),
            ("config.tml", "toml"),
            ("path/to/config.toml", "toml"),
            ("path/to/config.TML", "toml"),
            
            # Raw/unknown files
            ("file.txt", "raw"),
            ("file", "raw"),
            ("path/to/file.unknown", "raw"),
            ("", "raw"),
            (".", "raw"),
        ],
    )
    def test_file_extensions(self, file_path, expected):
        """Test encoding detection for various file extensions."""
        assert get_encoding_for_file_path(file_path) == expected
    
    def test_path_objects(self):
        """Test encoding detection with Path objects."""
        assert get_encoding_for_file_path(Path("config.yaml")) == "yaml"
        assert get_encoding_for_file_path(Path("data.json")) == "json"
        assert get_encoding_for_file_path(Path("main.tf")) == "hcl"
        assert get_encoding_for_file_path(Path("config.toml")) == "toml"
    
    def test_case_insensitivity(self):
        """Test case-insensitive extension matching."""
        assert get_encoding_for_file_path("config.YAML") == "yaml"
        assert get_encoding_for_file_path("data.JSON") == "json"
        assert get_encoding_for_file_path("main.TF") == "hcl"
        assert get_encoding_for_file_path("config.TOML") == "toml"

class TestIsConfigFile:
    """Tests for is_config_file function."""
    
    @pytest.mark.parametrize(
        "file_path,expected",
        [
            # Config files
            ("config.yaml", True),
            ("config.yml", True),
            ("data.json", True),
            ("main.tf", True),
            ("config.hcl", True),
            ("config.toml", True),
            ("config.tml", True),
            
            # Non-config files
            ("file.txt", False),
            ("script.py", False),
            ("image.png", False),
            ("file", False),
            ("", False),
            (".", False),
        ],
    )
    def test_config_detection(self, file_path, expected):
        """Test config file detection for various paths."""
        assert is_config_file(file_path) == expected
    
    def test_path_objects(self):
        """Test config detection with Path objects."""
        assert is_config_file(Path("config.yaml")) is True
        assert is_config_file(Path("script.py")) is False
    
    def test_case_insensitivity(self):
        """Test case-insensitive config detection."""
        assert is_config_file("CONFIG.YAML") is True
        assert is_config_file("DATA.JSON") is True
        assert is_config_file("MAIN.TF") is True 