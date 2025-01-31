"""Tests for core CLI commands (convert, format, validate)."""

from __future__ import annotations

import json

from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from click.testing import CliRunner
from extended_data_types.cli.commands.convert import convert
from extended_data_types.cli.commands.format import format
from extended_data_types.cli.commands.validate import validate


@pytest.fixture()
def runner():
    """Fixture for CLI runner."""
    return CliRunner()


@pytest.fixture()
def sample_json(tmp_path: Path) -> Path:
    """Fixture for sample JSON file."""
    content = {"name": "test", "numbers": [3, 1, 2], "nested": {"c": 3, "a": 1, "b": 2}}

    file_path = tmp_path / "sample.json"
    file_path.write_text(json.dumps(content))
    return file_path


@pytest.fixture()
def sample_yaml(tmp_path: Path) -> Path:
    """Fixture for sample YAML file."""
    content = """
    name: test
    numbers:
      - 3
      - 1
      - 2
    nested:
      c: 3
      a: 1
      b: 2
    """

    file_path = tmp_path / "sample.yaml"
    file_path.write_text(dedent(content))
    return file_path


def test_convert_json_to_yaml(runner: CliRunner, tmp_path: Path, sample_json: Path):
    """Test converting JSON to YAML."""
    output_file = tmp_path / "output.yaml"

    result = runner.invoke(
        convert,
        [
            str(sample_json),
            str(output_file),
            "--from-format",
            "json",
            "--to-format",
            "yaml",
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()

    # Verify YAML content
    with output_file.open() as f:
        data = yaml.safe_load(f)
        assert data["name"] == "test"
        assert data["numbers"] == [3, 1, 2]
        assert data["nested"]["a"] == 1


def test_convert_auto_format_detection(
    runner: CliRunner, tmp_path: Path, sample_json: Path
):
    """Test format auto-detection in convert command."""
    output_file = tmp_path / "output.yaml"

    result = runner.invoke(convert, [str(sample_json), str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()


def test_convert_with_options(runner: CliRunner, tmp_path: Path, sample_json: Path):
    """Test convert command with formatting options."""
    output_file = tmp_path / "output.yaml"

    result = runner.invoke(
        convert, [str(sample_json), str(output_file), "--indent", "4", "--sort-keys"]
    )

    assert result.exit_code == 0
    content = output_file.read_text()
    assert "    a: 1" in content  # Check indentation
    # Verify keys are sorted
    a_pos = content.find("a: 1")
    b_pos = content.find("b: 2")
    c_pos = content.find("c: 3")
    assert a_pos < b_pos < c_pos


def test_format_json(runner: CliRunner, sample_json: Path):
    """Test formatting JSON file."""
    result = runner.invoke(
        format, [str(sample_json), "--format", "json", "--indent", "2", "--sort-keys"]
    )

    assert result.exit_code == 0
    assert '"a": 1' in result.output
    assert '"b": 2' in result.output
    assert '"c": 3' in result.output


def test_format_in_place(runner: CliRunner, tmp_path: Path):
    """Test in-place formatting."""
    # Create unformatted JSON file
    file_path = tmp_path / "unformatted.json"
    file_path.write_text('{"c":3,"a":1,"b":2}')

    result = runner.invoke(format, [str(file_path), "--in-place", "--sort-keys"])

    assert result.exit_code == 0
    content = file_path.read_text()
    assert '"a": 1' in content
    assert '"b": 2' in content
    assert '"c": 3' in content


def test_format_multiple_files(runner: CliRunner, tmp_path: Path):
    """Test formatting multiple files."""
    # Create test files
    file1 = tmp_path / "file1.json"
    file2 = tmp_path / "file2.json"
    file1.write_text('{"b":2,"a":1}')
    file2.write_text('{"d":4,"c":3}')

    result = runner.invoke(
        format, [str(file1), str(file2), "--in-place", "--sort-keys"]
    )

    assert result.exit_code == 0
    assert '"a": 1' in file1.read_text()
    assert '"c": 3' in file2.read_text()


def test_validate_valid_files(runner: CliRunner, sample_json: Path, sample_yaml: Path):
    """Test validating valid files."""
    result = runner.invoke(validate, [str(sample_json), str(sample_yaml)])

    assert result.exit_code == 0
    assert "Valid JSON syntax" in result.output
    assert "Valid YAML syntax" in result.output


def test_validate_invalid_json(runner: CliRunner, tmp_path: Path):
    """Test validating invalid JSON."""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text('{"invalid": json')

    result = runner.invoke(validate, [str(invalid_file)])

    assert result.exit_code != 0
    assert "Invalid JSON syntax" in result.output


def test_validate_invalid_yaml(runner: CliRunner, tmp_path: Path):
    """Test validating invalid YAML."""
    invalid_file = tmp_path / "invalid.yaml"
    invalid_file.write_text("invalid: : yaml")

    result = runner.invoke(validate, [str(invalid_file)])

    assert result.exit_code != 0
    assert "Invalid YAML syntax" in result.output


def test_validate_unsupported_format(runner: CliRunner, tmp_path: Path):
    """Test validating file with unsupported format."""
    test_file = tmp_path / "test.unsupported"
    test_file.write_text("some content")

    result = runner.invoke(validate, [str(test_file)])

    assert "unsupported format" in result.output


def test_convert_error_handling(runner: CliRunner, tmp_path: Path):
    """Test error handling in convert command."""
    # Test nonexistent input file
    result = runner.invoke(convert, ["nonexistent.json", "output.yaml"])
    assert result.exit_code != 0
    assert "Error" in result.output

    # Test invalid format
    result = runner.invoke(
        convert,
        [
            str(tmp_path / "test.txt"),
            str(tmp_path / "output.txt"),
            "--from-format",
            "invalid",
            "--to-format",
            "json",
        ],
    )
    assert result.exit_code != 0
    assert "Error" in result.output


def test_format_error_handling(runner: CliRunner):
    """Test error handling in format command."""
    # Test no files specified
    result = runner.invoke(format, [])
    assert result.exit_code != 0
    assert "No input files specified" in result.output


def test_validate_error_handling(runner: CliRunner):
    """Test error handling in validate command."""
    # Test no files specified
    result = runner.invoke(validate, [])
    assert result.exit_code != 0
    assert "No input files specified" in result.output


def test_convert_with_different_indentation(
    runner: CliRunner, tmp_path: Path, sample_json: Path
):
    """Test converting with different indentation levels."""
    output_file = tmp_path / "output.yaml"

    result = runner.invoke(
        convert, [str(sample_json), str(output_file), "--indent", "4"]
    )

    assert result.exit_code == 0
    content = output_file.read_text()
    assert "    name:" in content  # Check 4-space indentation


def test_format_with_different_indentation(runner: CliRunner, sample_json: Path):
    """Test formatting with different indentation levels."""
    result = runner.invoke(format, [str(sample_json), "--indent", "4"])

    assert result.exit_code == 0
    assert '    "name":' in result.output  # Check 4-space indentation
