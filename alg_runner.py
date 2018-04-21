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
    # g.display()
    print(g.get_score())

    Q = g.get_score()

    print('p\ta\tb\tS\ttime\titer\tLS\twise')
    for p in [0.8]:
        for a in [0.4]:
            for b in [4]:
                for wise in [True, False]:
                    for rand_seed in ['see', 'eed', 'it']:
                        start = time.time()
                        alg = ACO(data, ACOParams(Q, p, a, b, 200, wise), rand_seed)
                        best = alg.run(silent=True)
                        print('{p}\t{a}\t{b}\t{s}\t{t}\t{i}\t{ls}\t{w}'.format(
                            p=p, a=a, b=b, s=best, t=time.time() - start,
                            i=alg.last_productive_iteration, ls=alg.ls_number, w=wise))
                        del alg
                        # alg.output()

    print('Пошук здійснено за {}с'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    main()
