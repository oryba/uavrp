"""
Description
"""

import click

from alg.reader import KnapsackReader
from alg.knapsnack_alg import Knapsnack
from greedy import Greedy

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush"]


@click.command()
@click.option('--file', help='Path to input file', type=click.Path(dir_okay=False), required=True)
def main(file):

    reader = KnapsackReader('input/{}.in'.format(file))
    reader.process()
    data = reader.get()

    g = Greedy(data.header, data.rides)
    g.run()
    g.output("output/{}.out".format(file))

    # knapsnack = Knapsnack(data, iteration, child_number, population_number, chance_number)
    # knapsnack.run()
    #
    # print(knapsnack.result)


if __name__ == '__main__':
    main()
