from time import sleep
from drawer.graph import Plotter


class AlgBase:
    def __init__(self, distance, vertices):
        self.D = distance
        self.V = vertices
        self.progress = []

    def solve(self, *args, **kwargs):
        raise NotImplementedError

    def score(self, solution):
        return sum(self.D[i][j] for i, j in zip(solution, solution[1:]))

    def visualize(self, score, deviation):
        for path in self.progress:
            gp = Plotter(
                self.V,
                title=f"Greedy algorithm, {score} ({deviation:.2f}%)"
            )
            gp.plot_points()
            gp.plot_edges(path)
            gp.show()
            sleep(0.01)
