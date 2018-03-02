"""
Description
"""

import click

from reader import VehicleAssignmentReader
from greedy import Greedy

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba", "oyarush"]


@click.command()
@click.option('--file', help='Path to input file without extension',
              default='a_example', required=True)
def main(file):
    reader = VehicleAssignmentReader('input/{}.in'.format(file))
    data = reader.process()

    g = Greedy(data.header, data.rides)
    g.run()
    g.output("output/{}.out".format(file))


if __name__ == '__main__':
    main()
