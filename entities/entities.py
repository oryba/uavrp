"""
Prototypes of involved objects
"""
from recordclass import recordclass
from collections import namedtuple
from geopy.distance import vincenty
import operator
from functools import lru_cache

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]

# Ride container with calculated time delta and profit
AvailableOption = namedtuple('AvailOption', ['vehicle',
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
        if self.free and other.free:
            return 0
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
    def __init__(self, position: Point):
        self.position = position
        super().__init__(*position, free=True)

    @staticmethod
    def fabric(depots):
        for depot in depots:
            yield Depot(Point(*depot))

    def __repr__(self):
        return 'Depot at {}:{}'.format(*self.position)


class TargetState(Point):
    def __init__(self, target):
        self.position = target.position
        self.visited = False
        super().__init__(*target.position)

    def __repr__(self):
        return '{} Target at {}:{}'.format(
            'Visited' if self.visited else '', *self.position)


class Target(Point):
    def __init__(self, position: Point):
        self.position = position
        super().__init__(*position)

    @staticmethod
    def fabric(targets):
        for target in targets:
            yield Target(Point(*target))

    def create_state(self):
        return TargetState(self)


class Obstacle(Point):
    def __init__(self, position: Point, radius: float):
        self.position = position
        self.radius = radius
        super().__init__(*position)

    @staticmethod
    def fabric(obstacles):
        for obstacle in obstacles:
            yield Obstacle(Point(*obstacle[:2]), obstacle[2])

    def __repr__(self):
        return 'Obstacle at {}:{}'.format(*self.position)


class VehicleState:
    def __init__(self, vehicle, position: Point, depots: [Depot]):
        self.vehicle = vehicle
        self.position = position
        self.reserve = vehicle.dist
        self.points = []
        self.depots = depots

    # @lru_cache()
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
        if getattr(destination, 'visited', None):
            return False
        distance, _ = self._get_way(self.position, destination)
        way_back = min([destination - d for d in self.depots])
        if distance + way_back <= self.reserve:
            return True
        else:
            return False

    def move(self, option: AvailableOption):
        #if not self.check_flight(destinations[-1]):
        #    return False
        distance, way = option.distance, option.milestones
        self.reserve -= distance
        self.position = way[-1]
        self.points.extend(way)
        way[-1].visited = True
        return distance

    def distance_to_list(self, destinations: [Point], through_null_point=False):
        options = [AvailableOption(
                self, *self._get_way(self.position, d))
                for d in destinations if self.check_flight(d)]
        if through_null_point:
            # TODO: check flight!
            options += [AvailableOption(
                self, *self._get_way_through_depot(self.position, d))
                for d in destinations if self.check_flight(d)]
        return options


    def __repr__(self):
        return 'Vehicle at {}:{}'.format(*self.position)


class Vehicle:
    def __init__(self, dist, speed):
        self.speed = speed
        self.dist = dist

    @staticmethod
    def fabric(vehicles):
        for vehicle in vehicles:
            yield Vehicle(*(vehicle))

    def create_state(self, depots: [Depot]):
        return VehicleState(self, Point(0, 0, free=True), depots)

    def __repr__(self):
        return 'Vehicle'


Edge = recordclass('Edge', ['start', 'end', 'weight'])

ACOParams = namedtuple('ACO', ['q', 'p', 'a', 'b'])


class Pheromone:
    def __init__(self, points, p, q, start=0.4):
        """
        :param points: depots and targets
        :param p: pheromone decrease level
        :param q: constant order of the optimum
        """
        self.points = points + [Point(0, 0, free=True)]
        self.p = p
        self.q = q
        self.adj = {q: {p: start for p in self.points} for q in self.points}

    def __getitem__(self, item):
        return self.adj[item]

    def update(self, vehicles_scores):
        """
        :param vehicles_scores: tuple (solution, vehicle)
        """
        # evaporation
        for val in self.adj.values():
            for p in val:
                val[p] = (1 - self.p) * val[p]

        # update
        for score, v in vehicles_scores:
            if not v.points:
                continue
            for s, d in zip(v.points, v.points[1:]):
                self.adj[s][d] += self.q / score
