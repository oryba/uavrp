"""
Input processor
"""

from entities import Point, Header, Data, Depot, Target, Vehicle, Obstacle

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush", "oryba"]


class Reader:

    def __init__(self, input_file):

        self.input_file = input_file
        self.data = None

    def _get_data(self, header, body):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError


class FlightsReader(Reader):
    def process(self):
        with open(self.input_file, 'r') as f:
            header = Header(*[int(i) for i in f.readline().split()])
            depots = list(Depot.fabric(
                [reversed([float(i) for i in next(f).split()])
                      for x in range(header.depots)]
            ))
            targets = list(Target.fabric(
                [reversed([float(i) for i in next(f).split()])
                       for x in range(header.targets)]
            ))
            obstacles = list(Obstacle.fabric(
                [reversed([float(i) for i in next(f).split()])
                      for x in range(header.obstacles)]
            ))
            vehicles = list(Vehicle.fabric(
                [[float(i) for i in next(f).split()]
                      for x in range(header.vehicles)]
            ))
            return Data(header, depots, targets, obstacles, vehicles)
