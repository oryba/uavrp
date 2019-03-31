import sys
import time
import numpy as np
from reader import read_file
from solver.greedy_2s import Greedy2s
from solver.greedy import Greedy
from bind.aco import greedy
from solver.local import Local2Opt
from drawer.graph import Plotter


def deviation(current, optimal):
    return 100 * (current - optimal) / optimal


if __name__ == "__main__":
    distances, vertices, optimal = read_file(sys.argv[1])
    np.set_printoptions(precision=3)
    # D_flat = distances.flatten()
    # D_flat[D_flat == np.inf] = 10000000
    # res = greedy(D_flat, len(D_flat))


    greedy_alg = Greedy(distances, vertices)
    greedy_score, greedy_path = greedy_alg.solve()
    greedy_deviation = deviation(greedy_score, optimal)

    greedy_alg.visualize(greedy_score, greedy_deviation)

    # start = time.time()
    # ls_alg = Local2Opt(distances, vertices)
    # ls_score, ls_path = ls_alg.solve(greedy_path)
    # ls_deviation = deviation(ls_score, optimal)
    # duration = time.time() - start
    # print(f"Duration: {duration:.2f}")

    # ls_alg.visualize(ls_score, ls_deviation)
