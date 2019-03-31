import os
import numpy as np

from path import BASE_PATH


def read_file(name: str) -> (np.array, list):
    vertices = []
    with open(os.path.join(BASE_PATH, "input", name)) as f:
        optimal = float(f.readline())
        for point in f.readlines():
            idx, x, y = point.split()
            vertices.append((float(x), float(y)))

    distances = []
    for i, source in enumerate(vertices):
        distances.append(
            [((source[0] - destination[0]) ** 2 + (source[1] - destination[1]) ** 2) ** 0.5
             for j, destination in enumerate(vertices)]
        )

    distances = np.array(distances)
    distances[distances == 0] = np.inf
    return distances, vertices, optimal
