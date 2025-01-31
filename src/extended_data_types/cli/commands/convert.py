"""Command for converting between different data formats."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from extended_data_types.serialization import get_serializer, list_serializers


@click.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path))
@click.option(
    '--from-format', '-f',
    type=click.Choice(list_serializers()),
    help='Input format (detected from extension if not specified)'
)
@click.option(
    '--to-format', '-t',
    type=click.Choice(list_serializers()),
    help='Output format (detected from extension if not specified)'
)
@click.option('--indent', '-i', type=int, default=2, help='Indentation spaces (default: 2)')
@click.option('--sort-keys', '-s', is_flag=True, help='Sort keys alphabetically')
def convert(
    input_file: Path,
    output_file: Path,
    from_format: Optional[str],
    to_format: Optional[str],
    indent: int,
    sort_keys: bool
):
    """Convert between different data formats.
    
    If formats are not specified, they will be detected from file extensions.
    
    Example:
        edt convert config.json config.yaml
        edt convert --from-format json --to-format yaml input.txt output.txt
    """
    try:
        # Detect formats from file extensions if not specified
        if not from_format:
            from_format = input_file.suffix.lstrip('.')
        if not to_format:
            to_format = output_file.suffix.lstrip('.')
            
        if from_format not in list_serializers():
            raise click.BadParameter(f"Unsupported input format: {from_format}")
        if to_format not in list_serializers():
            raise click.BadParameter(f"Unsupported output format: {to_format}")
        
        # Get serializers
        from_serializer = get_serializer(from_format)
        to_serializer = get_serializer(to_format)
        
        # Read and parse input
        content = input_file.read_text()
        data = from_serializer.decode(content)
        
        # Convert and write output
        result = to_serializer.encode(data, indent_size=indent, sort_keys=sort_keys)
        output_file.write_text(result)
        
        click.echo(f"Successfully converted {input_file} ({from_format}) to {output_file} ({to_format})")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort() 