"""
Greedy algorithm for vehicle assignment problem
"""
from entities import *
from .local import local_2opt, get_score as local_score

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
        self.ls_number = 0

    def get_score(self, vehicles=None):
        """Calculate a score of current state

        :return integer score"""
        raise NotImplementedError()

    def run(self):
        """Run iterations till no improvements left"""
        raise NotImplementedError()

    def _local(self, vehicles: [VehicleState], light=False):
        self.ls_number += 1
        for v in vehicles:
            if v.points:
                # TODO improve 2opt
                # we can optimize only chunks between depots
                depots_indices = [i for i, p in enumerate(v.points)
                                  if isinstance(p, Depot)]
                current_score = local_score(PointsList(v.points))
                # for each chunk
                for i, j in zip(depots_indices, depots_indices[1:]):
                    while True:
                        v.points[i:j+1], _ = local_2opt(PointsList(v.points[i:j+1]))
                        score = local_score(PointsList(v.points))
                        if score < current_score:
                            current_score = score
                        else:
                            break
        return vehicles

    def output(self):
        """Save the solution to output file"""
        rows = []
        for vehicle in self.vehicles:
            if len(vehicle.points) > 2:
                print("БПЛ {}:".format(vehicle.name))
                print(" > вилітає з аеропорту {}".format(vehicle.points[0].name))
                fragment = vehicle.get_copy()
                fragment.points = [vehicle.points[0]]
                for p in vehicle.points[1:-1]:
                    if isinstance(p, TargetState):
                        fragment.points.append(p)
                        print(" > знімає ціль {}".format(p.name))
                    elif isinstance(p, Depot):
                        print(" > замінює блоки живлення в аеропорту {}".format(p.name))
                        fragment.points.append(p)
                        print(self.get_score([fragment]))
                        fragment.points = [p]
                print(" > здійснює посадку в аеропорту {}".format(vehicle.points[-1].name))
                fragment.points.append(vehicle.points[-1])
                print(self.get_score([fragment]))

        # with open(output_file, "w") as f:
        #     f.writelines(rows)

    def display(self, vehicles=None):
        g = Graph()

        g.add_points(self.targets + self.obstacles + self.depots)

        for v in (vehicles or self.vehicles):
            if not v.points:
                continue
            for p, n in zip(v.points, v.points[1:]):
                g.add_edge(Edge(p, n, v.vehicle.color))

        p = Plotter(g)
        p.plot_points()
        p.plot_edges()
        p.show()

