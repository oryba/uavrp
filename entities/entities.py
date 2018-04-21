"""
Prototypes of involved objects
"""
from recordclass import recordclass
from collections import namedtuple
from geopy.distance import vincenty
import operator
from functools import lru_cache
import numpy as np

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]

# Ride container with calculated time delta and profit
AvailableOption = recordclass('AvailOption', ['vehicle',
                                             'distance', 'milestones'])

# Problem data with headers and rides set
Data = recordclass('Data', ['header', 'depots', 'targets',
                            'obstacles', 'vehicles'])

# Problem properties
Header = namedtuple('Header', ['depots', 'targets', 'obstacles', 'vehicles'])


# Map point
class Point:
    def __init__(self, x, y, free=False):
        self.x = x
        self.y = y
        # if tha point is free, we can travel to any target for
        # min(target - any depot) distance
        self.free = free

    @lru_cache(None)
    def __sub__(self, other):
        if self.free:
            if isinstance(other, Depot):
                return 0
            else:
                return float('inf')
        if other.free:
            return float('inf')
        # return abs(self.x - other.x) + abs(self.y - other.y)
        return vincenty((self.x, self.y), (other.x, other.y)).km

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        raise IndexError()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + hash(self.y)


class Depot(Point):
    def __init__(self, position: Point, name=''):
        self.position = position
        self.name = name
        super().__init__(*position)

    @staticmethod
    def fabric(depots):
        for depot in depots:
            y, x, name = depot.strip().split()
            yield Depot(Point(float(x),float(y)), name=name)

    def __repr__(self):
        return 'Depot at {}:{}'.format(*self.position)


class TargetState(Point):
    def __init__(self, target):
        self.position = target.position
        self.visited = False
        self.name = target.name
        super().__init__(*target.position)

    def __repr__(self):
        return '{} Target at {}:{}'.format(
            'Visited' if self.visited else '', *self.position)


class Target(Point):
    def __init__(self, position: Point, name=''):
        self.position = position
        self.name = name
        super().__init__(*position)
        self.id = 0

    @staticmethod
    def fabric(targets):
        for target in targets:
            y, x, name = target.strip().split()
            yield Target(Point(float(x),float(y)), name=name)

    def create_state(self):
        return TargetState(self)

    def __repr__(self):
        return str(self.id)


class Obstacle(Point):
    def __init__(self, position: Point, radius: float, name=''):
        self.position = position
        self.radius = radius
        self.name = name
        super().__init__(*position)

    @staticmethod
    def fabric(obstacles):
        for obstacle in obstacles:
            y, x, radius, name = obstacle.strip().split()
            yield Obstacle(Point(float(x),float(y)), radius, name=name)

    def __repr__(self):
        return 'Obstacle at {}:{}'.format(*self.position)


class VehicleState:
    def __init__(self, vehicle, position: Point, depots: [Depot]):
        self.vehicle = vehicle
        self.position = position
        self.reserve = vehicle.dist
        self.name = vehicle.name
        self.points = []
        self.depots = depots
        self.np = 0
        self.idx = None

    def get_copy(self):
        v = VehicleState(self.vehicle, self.position, self.depots)
        v.points = self.points[:]
        v.reserve = self.reserve
        return v

    @lru_cache()
    def _get_way(self, source: Point, destination: Point):
        milestones = []
        if source.free:
            depot_index, distance = min(
                enumerate([destination - d for d in self.depots]),
                key=operator.itemgetter(1)
            )
            milestones.append(self.depots[depot_index])
        else:
            distance = source - destination
        milestones.append(destination)
        return distance, milestones

    def _get_way_through_depot(self, source: Point, destination: Point):
        if source.free:
            return self._get_way(source, destination)
        in_depot_index, in_distance = min(
            enumerate([source - d for d in self.depots]),
            key=operator.itemgetter(1)
        )
        out_depot_index, out_distance = min(
            enumerate([destination - d for d in self.depots]),
            key=operator.itemgetter(1)
        )
        return (in_distance + out_distance,
                [self.depots[in_depot_index],
                 self.depots[out_depot_index],
                 destination])

    def check_flight(self, destination: Point):
        if getattr(destination, 'visited', None) and not isinstance(destination, Depot):
            return False
        distance, _ = self._get_way(self.position, destination)
        way_back = min([destination - d for d in self.depots])
        if distance + way_back <= self.reserve:
            return True
        else:
            return False

    def move(self, option: AvailableOption, skip_marking=False):
        #if not self.check_flight(destinations[-1]):
        #    return False
        distance, way = option.distance, option.milestones
        self.reserve -= distance
        self.position = way[-1]
        self.points.extend(way)
        if not skip_marking:
            for w in way:
                w.visited = True
        if isinstance(way[-1], Depot):
            self.reserve = self.vehicle.dist
        return distance

    def move_to_depot(self):
        if isinstance(self.position, Depot):
            return False
        in_depot_index, in_distance = min(
            enumerate([self.position - d for d in self.depots]),
            key=operator.itemgetter(1)
        )
        # recharge
        self.reserve = self.vehicle.dist
        depot = self.depots[in_depot_index]
        self.position = depot
        self.points.append(depot)

    def distance_to_list(self, destinations: [Point]) -> [AvailableOption]:
        options = [AvailableOption(
                self, *self._get_way(self.position, d))
                for d in destinations if self.check_flight(d) and d != self.position]
        # if through_null_point:
        #     # TODO: check flight!
        #     options += [AvailableOption(
        #         self, *self._get_way_through_depot(self.position, d))
        #         for d in destinations if self.check_flight(d)]
        return options

    def __repr__(self):
        return 'Vehicle {} at {}:{}'.format(self.vehicle.name, *self.position)


class Vehicle:
    def __init__(self, dist, speed, color='c', name=''):
        self.speed = speed
        self.dist = dist
        self.color = color
        self.name = name

    @staticmethod
    def fabric(vehicles):
        colors = ['#aaaa00', '#aa00aa', '#00aa00']
        for i, vehicle in enumerate(vehicles):
            dist, speed, name = vehicle.strip().split()
            yield Vehicle(float(dist), float(speed), name=name, color=colors[i % len(colors)])

    def create_state(self, depots: [Depot]):
        return VehicleState(self, Point(0, 0, free=True), depots)

    def __repr__(self):
        return 'Vehicle {}'.format(self.name)


Edge = recordclass('Edge', ['start', 'end', 'color'])

ACOParams = namedtuple('ACO', ['q', 'p', 'a', 'b', 'iterations', 'two_steps'])


class Pheromone:
    def __init__(self, points, p, q, start=0.4, bounds=(0.4, 1.9)):
        """
        :param points: depots and targets
        :param p: pheromone decrease level
        :param q: constant order of the optimum
        """
        self.points = points + [Point(0, 0, free=True)]
        self.p = p
        self.q = q
        self.bounds = bounds
        self.adj = {q: {p: start for p in self.points} for q in self.points}

    def __getitem__(self, item):
        return self.adj[item]

    def evaporation(self):
        for val in self.adj.values():
            for p in val:
                val[p] = max(
                    (1 - self.p) * (val[p] - self.bounds[0]) + self.bounds[0],
                    self.bounds[0])

    def update(self, score, vehicles):
        """
        :param vehicles_scores: tuple (solution, vehicle)
        """
        self.evaporation()

        # update
        for v in vehicles:
            if not v.points:
                continue
            for s, d in zip(v.points, v.points[1:]):
                self.adj[s][d] = min(
                    self.adj[s][d] + self.q / score,
                    self.bounds[1]
                )
                # self.adj[d][s] = self.adj[s][d]


class NewPheromone:
    def __init__(self, points, p, q, start=0.2, bounds=(0.2, 0.9)):
        """
        :param points: depots and targets
        :param p: pheromone decrease level
        :param q: constant order of the optimum
        """
        self.p = p
        self.q = q
        self.bounds = bounds
        self.n = len(points)
        self.adj = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                self.adj[i][j] = start

    def __getitem__(self, item):
        return self.adj[item]

    def evaporation(self):
        for i in range(self.n):
            for j in range(self.n):
                self.adj[i][j] = max(
                    (1 - self.p) * self.adj[i][j],
                    self.bounds[0])

    def update(self, score, vehicles):
        """
        :param vehicles_scores: tuple (solution, vehicle)
        """
        self.evaporation()

        # update
        for v in vehicles:
            if not v:
                continue
            for s, d in zip(v.points, v.points[1:]):
                self.adj[s][d] = min(
                    self.adj[s][d] + self.q / score,
                    self.bounds[1]
                )
                # self.adj[d][s] = self.adj[s][d]


class PointsList(list):
    def __hash__(self):
        return hash((el for el in self))

    def copy(self):
        return PointsList(self)