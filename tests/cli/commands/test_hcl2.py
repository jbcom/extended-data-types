"""Tests for HCL2 CLI commands."""

from __future__ import annotations

import json

from pathlib import Path
from textwrap import dedent

import pytest

from click.testing import CliRunner
from extended_data_types.cli.commands.hcl2 import convert, format, merge, validate


@pytest.fixture()
def runner():
    """Fixture for CLI runner."""
    return CliRunner()


@pytest.fixture()
def sample_tf(tmp_path: Path) -> Path:
    """Fixture for sample Terraform file."""
    content = dedent(
        """\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
        """
    )

    file_path = tmp_path / "main.tf"
    file_path.write_text(content)
    return file_path


@pytest.fixture()
def sample_variables(tmp_path: Path) -> Path:
    """Fixture for sample variables file."""
    content = dedent(
        """\
        variable "environment" {
          type    = string
          default = "dev"
        }
        """
    )

    file_path = tmp_path / "variables.tf"
    file_path.write_text(content)
    return file_path


def test_convert_hcl2_to_json(runner: CliRunner, tmp_path: Path, sample_tf: Path):
    """Test converting HCL2 to JSON."""
    output_file = tmp_path / "output.json"

    result = runner.invoke(
        convert,
        [
            str(sample_tf),
            str(output_file),
            "--from-format",
            "hcl2",
            "--to-format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()

    # Verify JSON content
    with output_file.open() as f:
        data = json.load(f)
        assert "resource" in data
        assert "aws_instance" in data["resource"]
        assert "web" in data["resource"]["aws_instance"]


def test_convert_json_to_hcl2(runner: CliRunner, tmp_path: Path):
    """Test converting JSON to HCL2."""
    # Create sample JSON file
    input_file = tmp_path / "input.json"
    json_content = {
        "resource": {"aws_instance": {"web": {"instance_type": "t2.micro"}}}
    }
    input_file.write_text(json.dumps(json_content))

    output_file = tmp_path / "output.tf"

    result = runner.invoke(
        convert,
        [
            str(input_file),
            str(output_file),
            "--from-format",
            "json",
            "--to-format",
            "hcl2",
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert 'resource "aws_instance" "web"' in output_file.read_text()


def test_merge_files(
    runner: CliRunner, tmp_path: Path, sample_tf: Path, sample_variables: Path
):
    """Test merging multiple Terraform files."""
    output_file = tmp_path / "merged.tf"

    result = runner.invoke(
        merge, [str(sample_tf), str(sample_variables), "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()

    content = output_file.read_text()
    assert 'resource "aws_instance" "web"' in content
    assert 'variable "environment"' in content


def test_validate_valid_file(runner: CliRunner, sample_tf: Path):
    """Test validating a valid HCL2 file."""
    result = runner.invoke(validate, [str(sample_tf)])

    assert result.exit_code == 0
    assert "valid HCL2 syntax" in result.output


def test_validate_invalid_file(runner: CliRunner, tmp_path: Path):
    """Test validating an invalid HCL2 file."""
    invalid_file = tmp_path / "invalid.tf"
    invalid_file.write_text("resource aws_instance {")  # Missing quotes

    result = runner.invoke(validate, [str(invalid_file)])

    assert result.exit_code != 0
    assert "invalid HCL2 syntax" in result.output


def test_format_file(runner: CliRunner, tmp_path: Path):
    """Test formatting an HCL2 file."""
    # Create unformatted file
    unformatted = tmp_path / "unformatted.tf"
    unformatted.write_text(
        dedent(
            """\
        resource "aws_instance" "web" {
        instance_type="t2.micro"
          tags={
        Name="web-server"
        }
        }
        """
        )
    )

    result = runner.invoke(format, [str(unformatted), "--indent", "2", "--sort-keys"])

    assert result.exit_code == 0

    formatted_content = unformatted.read_text()
    assert 'instance_type = "t2.micro"' in formatted_content
    assert "  tags = {" in formatted_content
    assert '    Name = "web-server"' in formatted_content


def test_convert_with_invalid_format(
    runner: CliRunner, tmp_path: Path, sample_tf: Path
):
    """Test converting with invalid format specification."""
    output_file = tmp_path / "output.json"

    result = runner.invoke(
        convert,
        [
            str(sample_tf),
            str(output_file),
            "--from-format",
            "invalid",
            "--to-format",
            "json",
        ],
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_merge_no_files(runner: CliRunner):
    """Test merge command with no input files."""
    result = runner.invoke(merge, [])

    assert result.exit_code != 0
    assert "No input files specified" in result.output


def test_format_with_invalid_file(runner: CliRunner, tmp_path: Path):
    """Test formatting an invalid HCL2 file."""
    invalid_file = tmp_path / "invalid.tf"
    invalid_file.write_text("invalid { syntax")

    result = runner.invoke(format, [str(invalid_file)])

    assert result.exit_code != 0
    assert "Error" in result.output


def test_convert_with_nonexistent_file(runner: CliRunner, tmp_path: Path):
    """Test converting a nonexistent file."""
    output_file = tmp_path / "output.json"

    result = runner.invoke(convert, ["nonexistent.tf", str(output_file)])

    assert result.exit_code != 0
    assert "Error" in result.output


def test_merge_with_mixed_formats(runner: CliRunner, tmp_path: Path, sample_tf: Path):
    """Test merging files with different formats."""
    # Create a JSON file
    json_file = tmp_path / "config.json"
    json_content = {"variable": {"region": {"default": "us-west-2"}}}
    json_file.write_text(json.dumps(json_content))

    output_file = tmp_path / "merged.tf"

    result = runner.invoke(
        merge, [str(sample_tf), str(json_file), "--output", str(output_file)]
    )

    assert result.exit_code != 0
    assert "Error" in result.output
