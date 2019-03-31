import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, points, title=""):
        self.points = points
        self.title = title
        self.edges = []
        self.plot = None

    def plot_points(self):
        self.plot = plt.plot(*zip(*self.points), marker='o', markersize=5, color='b', ls='')

    def plot_edges(self, path: list):
        for start, end in zip(path, path[1:]):
            self.edges.append(
                plt.plot(
                    [self.points[start][0], self.points[end][0]],
                    [self.points[start][1], self.points[end][1]],
                    color='r',
                    linewidth=2.0)[0]
            )

    def clear_edges(self):
        for edge in self.edges:
            edge.remove()

    def show(self):
        plt.title(self.title)
        plt.show()
