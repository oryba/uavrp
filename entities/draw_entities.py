import matplotlib.pyplot as plt
import mplleaflet
from entities import Depot, Obstacle, TargetState, Point, Edge


class Graph:
    def __init__(self):
        self.targets = []
        self.depots = []
        self.obstacles = []
        self.temps = []
        self.edges = []
        self._cached_points = []

    def add_points(self, points):
        for point in points:
            self._add_point(point)
        self._update_cached_points()

    def _add_point(self, point: Point):
        if isinstance(point, Depot):
            self.depots.append(point)
        elif isinstance(point, Obstacle):
            self.obstacles.append(point)
        elif isinstance(point, TargetState):
            self.targets.append(point)
        else:
            raise ValueError("Undefined type {}".format(type(point)))

    def _update_cached_points(self):
        self._cached_points = self.targets + self.depots + self.temps

    def get_available_points(self) -> [Point]:
        return self._cached_points

    def add_edge(self, edge: Edge):
        if edge.start not in self.get_available_points():
            raise ValueError("Edge starts from non-existent point")
        if edge.end not in self.get_available_points():
            raise ValueError("Edge ends with non-existent point")
        self.edges.append(edge)


class Plotter():
    def __init__(self, graph: Graph):
        self.graph = graph

    def plot_points(self):
        depots = [[p.x, p.y] for p in self.graph.depots]
        plt.plot(*zip(*depots), marker='o', color='b', ls='')
        targets = [[p.x, p.y] for p in self.graph.targets]
        plt.plot(*zip(*targets), marker='o', color='g', ls='')
        obstacles = [[p.x, p.y] for p in self.graph.obstacles]
        plt.plot(*zip(*obstacles), marker='o', color='r', ls='')

    def plot_edges(self):
        for e in self.graph.edges:
            plt.plot([e.start.x, e.end.x], [e.start.y, e.end.y], color='c',
                     linewidth=3.0)

    def show(self):
        mplleaflet.show()


if __name__ == '__main__':
    points = [
        Depot(x=1, y=1),
        Depot(x=1, y=3),
        Depot(x=1, y=5),
        TargetState(x=5, y=0),
        Obstacle(x=3, y=2, radius=1),
        Obstacle(x=3, y=4, radius=0.5)
    ]

    edges = [
        Edge(points[0], points[4], 0),
        Edge(points[4], points[6], 0),
        Edge(points[1], points[6], 0)
    ]

    g = Graph()

    g.add_points(points)

    [g.add_edge(edge) for edge in edges]

    p = Plotter(g)
    p.plot_points()
    p.plot_edges()
    p.show()
