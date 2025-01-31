"""Main CLI entry point for extended-data-types."""

import click

from .commands.convert import convert
from .commands.format import format
from .commands.hcl2 import hcl2
from .commands.validate import validate


@click.group()
def cli():
    """Extended Data Types CLI.
    
    Command line interface for working with extended data types and formats.
    """
    pass

# Register commands
cli.add_command(convert)
cli.add_command(validate)
cli.add_command(format)
cli.add_command(hcl2)

if __name__ == '__main__':
    cli() 