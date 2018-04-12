import itertools
import random
from functools import lru_cache

from entities import *


__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


@lru_cache(None)
def get_score(seq: PointsList):
    n_range = range(len(seq))
    return sum(seq[i] - seq[j] for i, j in zip(n_range, n_range[1:]))


@lru_cache(None)
def make_2opt(seq: PointsList, i, j):
    new_seq = seq.copy()
    new_seq[i:j] = seq[j-1:i-1:-1]
    return new_seq


def local_2opt(points):
    n = len(points)
    if n < 4:
        return points, get_score(points)
    neighbours = [points]
    for i in range(1, n-1):
        for j in range(i + 2, n):
            neighbours.append(make_2opt(points, i, j))
    return min(
        map(lambda n: (n, get_score(n)), neighbours),
        key=lambda pairs: pairs[1])


if __name__ == '__main__':
    targets = list(Target.fabric([[50.478404, 30.506887],
    [50.498841, 30.523816],
    [50.508222, 30.630811],
    [50.460862, 30.649951],
    [50.379307, 30.573624],
    [50.334877, 30.571261],
    [50.363888, 30.577941],
    [50.415803, 30.612011],
    [50.410850, 30.576544],
    [50.382149, 30.664148],
    [50.374409, 30.615389],
    [50.376951, 30.949898],
    [50.303762, 30.852284],
    [50.393498, 30.795309],
    [50.350858, 30.953390]]))
    for i, t in enumerate(targets):
        t.id = i

    initial = PointsList(targets)
    print(get_score(initial))
    print(local_2opt(initial))