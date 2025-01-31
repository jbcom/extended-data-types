"""CLI commands for HCL2 operations."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from extended_data_types.serialization import get_serializer
from extended_data_types.serialization.languages.hcl2 import HCL2


@click.group()
def hcl2():
    """HCL2 (HashiCorp Configuration Language) operations."""
    pass

@hcl2.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path))
@click.option('--from-format', '-f', default='hcl2', help='Input format (default: hcl2)')
@click.option('--to-format', '-t', default='json', help='Output format (default: json)')
@click.option('--indent', '-i', type=int, default=2, help='Indentation spaces (default: 2)')
@click.option('--sort-keys', '-s', is_flag=True, help='Sort keys alphabetically')
def convert(
    input_file: Path,
    output_file: Path,
    from_format: str,
    to_format: str,
    indent: int,
    sort_keys: bool
):
    """Convert between HCL2 and other formats.
    
    Example:
        edt hcl2 convert main.tf output.json --from-format hcl2 --to-format json
    """
    try:
        # Get serializers
        from_serializer = get_serializer(from_format)
        to_serializer = get_serializer(to_format)
        
        # Read and parse input
        content = input_file.read_text()
        data = from_serializer.decode(content)
        
        # Convert and write output
        result = to_serializer.encode(data, indent_size=indent, sort_keys=sort_keys)
        output_file.write_text(result)
        
        click.echo(f"Successfully converted {input_file} to {output_file}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@hcl2.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file (default: merged.tf)')
@click.option('--indent', '-i', type=int, default=2, help='Indentation spaces')
@click.option('--sort-keys', '-s', is_flag=True, help='Sort keys alphabetically')
def merge(
    files: tuple[Path, ...],
    output: Optional[Path],
    indent: int,
    sort_keys: bool
):
    """Merge multiple HCL2 files into a single file.
    
    Example:
        edt hcl2 merge main.tf variables.tf outputs.tf -o combined.tf
    """
    if not files:
        click.echo("Error: No input files specified", err=True)
        raise click.Abort()
    
    try:
        hcl = HCL2(indent_size=indent, sort_keys=sort_keys)
        merged = hcl.merge_files(list(files))
        
        output = output or Path('merged.tf')
        hcl.generate_file(merged, output)
        
        click.echo(f"Successfully merged {len(files)} files into {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@hcl2.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
def validate(file: Path):
    """Validate HCL2 file syntax.
    
    Example:
        edt hcl2 validate main.tf
    """
    try:
        hcl = HCL2()
        content = file.read_text()
        
        if hcl.validate(content):
            click.echo(f"{file} contains valid HCL2 syntax")
        else:
            click.echo(f"Error: {file} contains invalid HCL2 syntax", err=True)
            raise click.Abort()
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@hcl2.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
@click.option('--indent', '-i', type=int, default=2, help='Indentation spaces')
@click.option('--sort-keys', '-s', is_flag=True, help='Sort keys alphabetically')
def format(file: Path, indent: int, sort_keys: bool):
    """Format HCL2 file.
    
    Example:
        edt hcl2 format main.tf --indent 2 --sort-keys
    """
    try:
        hcl = HCL2(indent_size=indent, sort_keys=sort_keys)
        
        # Parse and regenerate to format
        content = file.read_text()
        config = hcl.parse(content)
        formatted = hcl.generate(config)
        
        # Write back to file
        file.write_text(formatted)
        
        click.echo(f"Successfully formatted {file}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort() 