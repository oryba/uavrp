"""
Greedy algorithm for vehicle assignment problem
"""
from entities import *

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


class Alg():
    """Greedy algorithm, stores all parameters and states while solving"""
    def __init__(self, data: Data):
        self.header = data.header
        self.depots = data.depots
        self.targets = [t.create_state() for t in data.targets]
        self.obstacles = data.obstacles
        self.vehicles = [v.create_state(data.depots) for v in data.vehicles]

    def get_score(self):
        """Calculate a score of current state

        :return integer score"""
        raise NotImplementedError()

    def run(self):
        """Run iterations till no improvements left"""
        raise NotImplementedError()

    def output(self, output_file):
        """Save the solution to output file"""
        rows = []
        for vehicle in self.vehicles:
            rides = [str(final_ride.ride.idx) for final_ride in vehicle.rides]
            rows.append(
                "{} {}\n".format(
                    len(rides),
                    " ".join(rides)
                )
            )
        with open(output_file, "w") as f:
            f.writelines(rows)

    def display(self):
        g = Graph()

        g.add_points(self.targets + self.obstacles + self.depots)

        for v in self.vehicles:
            if not v.points:
                continue
            for p, n in zip(v.points, v.points[1:]):
                g.add_edge(Edge(p, n, 0))
            g.add_edge(Edge(
                v.points[-1],
                min([d for d in v.distance_to_list(v.depots)],
                    key=lambda d: d.distance).milestones[-1],
                0
            ))


        p = Plotter(g)
        p.plot_points()
        p.plot_edges()
        p.show()

