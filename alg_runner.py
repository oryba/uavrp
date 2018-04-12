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
    g.run(silent=True)
    g.display()
    print(g.get_score())

    Q = g.get_score()

    print('p\ta\tb\tS\ttime\titer\tLS')
    for p in [0.5]:
        for a in [1.1]:
            for b in [40]:
                for wise in [True]:
                    start = time.time()
                    alg = ACO(data, ACOParams(Q, p, a, b, 100, wise))
                    best = alg.run(silent=True)
                    print('{p}\t{a}\t{b}\t{s}\t{t}\t{i}\t{ls}'.format(
                        p=p, a=a, b=b, s=best, t=time.time() - start,
                        i=alg.last_productive_iteration, ls=alg.ls_number))
                    del alg
                    # alg.output()

    print('Пошук здійснено за {}с'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    main()
