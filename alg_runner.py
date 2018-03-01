"""
Description
"""

import click

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush"]


@click.command()
@click.option('--input', help='Path to input file', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', help='Path to output file', type=click.Path(exists=False, file_okay=False))
@click.option('--iteration', help='Number of iteration', type=int)
def main():
    pass


if __name__ == '__main__':
    main()
