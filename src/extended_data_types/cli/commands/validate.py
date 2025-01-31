"""Command for validating data files."""

from __future__ import annotations

from pathlib import Path

import click

from extended_data_types.serialization import get_serializer, list_serializers


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "-f",
    type=click.Choice(list_serializers()),
    help="File format (detected from extension if not specified)",
)
def validate(files: tuple[Path, ...], format: str | None):
    """Validate data files for correct syntax.

    If format is not specified, it will be detected from file extensions.

    Example:
        edt validate config.json
        edt validate *.yaml --format yaml
    """
    if not files:
        click.echo("Error: No input files specified", err=True)
        raise click.Abort()

    exit_code = 0

    try:
        for file in files:
            # Detect format from file extension if not specified
            file_format = format or file.suffix.lstrip(".")

            if file_format not in list_serializers():
                click.echo(
                    f"Warning: Skipping {file} - unsupported format: {file_format}"
                )
                continue

            # Get serializer
            serializer = get_serializer(file_format)

            try:
                # Read and validate file
                content = file.read_text()
                serializer.decode(content)
                click.echo(f"{file}: Valid {file_format.upper()} syntax")

            except Exception as e:
                click.echo(
                    f"{file}: Invalid {file_format.upper()} syntax - {e!s}", err=True
                )
                exit_code = 1

    except Exception as e:
        click.echo(f"Error: {e!s}", err=True)
        raise click.Abort()

    if exit_code != 0:
        raise click.Abort()
