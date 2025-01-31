"""Command for formatting data files."""

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
@click.option(
    "--indent", "-i", type=int, default=2, help="Indentation spaces (default: 2)"
)
@click.option("--sort-keys", "-s", is_flag=True, help="Sort keys alphabetically")
@click.option("--in-place", "-w", is_flag=True, help="Write changes back to input file")
def format(
    files: tuple[Path, ...],
    format: str | None,
    indent: int,
    sort_keys: bool,
    in_place: bool,
):
    """Format data files for improved readability.

    If format is not specified, it will be detected from file extensions.

    Example:
        edt format config.json --indent 2 --sort-keys
        edt format *.yaml --format yaml --in-place
    """
    if not files:
        click.echo("Error: No input files specified", err=True)
        raise click.Abort()

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

            # Read and parse file
            content = file.read_text()
            data = serializer.decode(content)

            # Format and write output
            formatted = serializer.encode(data, indent_size=indent, sort_keys=sort_keys)

            if in_place:
                file.write_text(formatted)
                click.echo(f"Formatted {file}")
            else:
                click.echo(formatted)

    except Exception as e:
        click.echo(f"Error: {e!s}", err=True)
        raise click.Abort()
