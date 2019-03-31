from .base import AlgBase


class Local2Opt(AlgBase):
    def _2opt_next(self, best, current_path):
        n = len(self.D)
        for i in range(1, n - 1):
            for j in range(i + 2, n + 1):
                new_path = current_path[:]
                new_path[i:j] = current_path[j - 1:i - 1:-1]
                if self.score(new_path) < best:
                    # update the solution history
                    self.progress.append(new_path)

                    return self._2opt_next(self.score(new_path), new_path)
        return best, current_path

    def solve(self, initial):
        # update the solution history
        self.progress.append(initial)

        best_score, best_path = self._2opt_next(
            self.score(initial),
            initial
        )
        return best_score, best_path
