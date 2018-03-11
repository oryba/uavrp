"""
Description
"""

import click
import time

from reader import FlightsReader
from algs import Greedy, ACO
from entities import ACOParams

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba", "oyarush"]


@click.command()
@click.option('--file', help='Path to input file without extension',
              default='a_example', required=True)
def main(file):
    reader = FlightsReader('input/{}.in'.format(file))
    data = reader.process()

    g = Greedy(data)
    g.run()
    g.display()

    Q = g.get_score()

    start = time.time()
    a = ACO(data, ACOParams(Q, 0.2, 0.5, 0.8))
    a.run()
    print('It takes {} s'.format(time.time() - start))

    # g.output("output/{}.out".format(file))


if __name__ == '__main__':
    main()
