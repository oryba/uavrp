"""
Description
"""

import click

from alg.reader import KnapsnackReader
from alg.knapsnack_alg import Knapsnack

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush"]


@click.command()
@click.option('--input-file', help='Path to input file', type=click.Path(exists=True, dir_okay=False), required=True)
@click.option('--output-file', help='Path to output file', type=click.Path(exists=False, dir_okay=False), required=True)
@click.option('--iteration', help='Number of iteration', type=int, required=True)
@click.option('--child-number', help='Number of childs', type=int, required=True)
@click.option('--population-number', help='Number of population', type=int, required=True)
@click.option('--chance-number', help='Number of chance', type=int, required=True)
def main(input_file, output_file, iteration, child_number, population_number, chance_number):

    reader = KnapsnackReader(input_file)
    reader.process()
    data = reader.get()

    knapsnack = Knapsnack(data, iteration, child_number, population_number, chance_number)
    knapsnack.run()

    print(knapsnack.result)


if __name__ == '__main__':
    main()
