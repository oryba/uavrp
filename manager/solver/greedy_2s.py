from collections import namedtuple
import numpy as np
from .base import AlgBase

Option = namedtuple('Option', 'i,k,j,len')


class Greedy2s(AlgBase):
    def solve(self):
        current_id = 0
        D = np.copy(self.D)
        path = [0]
        while True:
            # disallow ways to the current vertex
            D[:, current_id].fill(np.inf)

            # choose a closest vertex
            options = []
            for k in range(len(D)):
                if np.isinf(D[current_id][k]):
                    continue
                for j in range(len(D)):
                    if np.isinf(D[k][j]):
                        continue
                    options.append(
                        Option(
                            current_id, k, j,
                            D[current_id][k] + D[k][j]
                        )
                    )

            # check if there is any way to proceed
            if not options:
                # check for 1-step options
                next_id = np.argmin(
                    D[current_id]
                )
                if not np.isinf(D[current_id][next_id]):
                    path.append(next_id)

                path.append(0)
                break

            option = min(options, key=lambda opt: opt.len)
            # store it in the path
            path.append(option.k)
            path.append(option.j)
            current_id = option.j

            D[:, option.k].fill(np.inf)

            # update the solution history
            self.progress.append(path[:])

        return self.score(path), path
