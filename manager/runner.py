import sys
import time
from collections import namedtuple
from itertools import product

import numpy as np
from reader import read_file
# from solver.greedy_2s import Greedy2s
# from solver.greedy import Greedy
from bind.tsp_alg import bind_data


# from solver.local import Local2Opt
# from drawer.graph import Plotter

def deviation(current, optimal):
    return 100 * (current - optimal) / optimal


PARAMS = ["problem", "n", "p", "a", "b", "ph_min", "ph_max", "iters", "ants", "result", "std", "time"]
PROBLEMS = [
    # "a280",
    "berlin52",
    # "bier127",
    # "eil51",
    # "eil76"
]

Config = namedtuple("Config", ', '.join(PARAMS[2:-3]))

if __name__ == "__main__":
    # problem = sys.argv[1]

    P = [0.2, 0.5, 0.9]
    a = [2, 7, 10]
    b = [2, 7, 10]
    ph_min = [1, 3]
    ph_max = [4, 10]
    iters = [-30]
    ants = [10, 100]

    configs = [Config(*p) for p in product(P,a,b,ph_min, ph_max, iters, ants)]


    # print header
    results = ('\t'.join(PARAMS)) + '\n'

    for problem in PROBLEMS:
        distances, vertices, optimal = read_file(problem + ".in")
        # np.set_printoptions(precision=3)
        D_flat = distances.flatten()
        D_flat[D_flat == np.inf] = 10000000

        for config in configs:
            start = time.time()
            res = bind_data(
                D_flat,
                len(distances),
                *config
            )
            duration = time.time() - start
            results += ('\t'.join(
                [problem, str(len(distances))] + [str(i) for i in config] + [str(res), f"{deviation(res, optimal):.2f}",
                                                                             f"{duration:.2f}"]
            )) + '\n'

    print(results)

    # start = time.time()
    # ls_alg = Local2Opt(distances, vertices)
    # ls_score, ls_path = ls_alg.solve(greedy_path)
    # ls_deviation = deviation(ls_score, optimal)
    # duration = time.time() - start
    # print(f"Duration: {duration:.2f}")

    # ls_alg.visualize(ls_score, ls_deviation)
