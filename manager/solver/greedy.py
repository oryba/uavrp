import numpy as np
from .base import AlgBase


class Greedy(AlgBase):
    def solve(self):
        current_id = 0
        D = np.copy(self.D)
        path = [0]
        while True:
            # disallow ways to the current vertex
            D[:, current_id].fill(np.inf)

            # choose a closest vertex
            next_id = np.argmin(
                D[current_id]
            )

            # check if there is any way to proceed
            if np.isinf(D[current_id][next_id]):
                path.append(0)
                break

            # store it in the path
            path.append(next_id)
            current_id = next_id

            # update the solution history
            self.progress.append(path[:])

        return self.score(path), path
