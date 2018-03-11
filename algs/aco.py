import itertools
import random

from algs.base import Alg
from entities import *


__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


class ACO(Alg):
    """ACO algorithm, stores all parameters and states while solving"""
    def __init__(self, data: Data, params: ACOParams):
        super().__init__(data)
        self.data = data
        self.params = params
        self.pheromone = Pheromone(self.targets + self.depots,
                                   params.p, params.q)
        self.base_vehicles = data.vehicles
        self.n = data.header.depots + data.header.targets
        random.seed('seed')

    def get_score(self, vehicles=None):
        """Calculate a score of current state

        :return integer score"""
        score = 0
        for vehicle in vehicles or self.vehicles:
            if vehicle.points:
                points = [p for p in vehicle.points]
                score += sum([p - n for p, n in zip(points, points[1:])])
                score += min(
                    [d.distance
                     for d in vehicle.distance_to_list(vehicle.depots)]
                )

        return score

    @staticmethod
    def _get_random():
        return random.uniform(0, 1)

    def _edge_probabilities(self, s, options):
        # tuple (destination, value)
        numerators = []
        for d in options:
            numerators.append((d, (self.pheromone[s][d.milestones[-1]] ** self.params.a) *
                      ((1 / d.distance) ** self.params.b)))
        denominator = sum([n[1] for n in numerators])
        # tuple (destination, probability)
        return [(n[0], n[1]/denominator) for n in numerators]

    def _get_available_options(self, vehicle: VehicleState):
        """Select options available for the vehicle

        :param vehicle: current vehicle with its state
        :return AvailableOptions list"""
        options = vehicle.distance_to_list(self.targets, through_null_point=True)
        return self._edge_probabilities(vehicle.position, options)

    @staticmethod
    def _select_option(vehicle: VehicleState, options):
        """
        Choose the best option for the vehicle on the iteration. Modifies
        a ride availability, a vehicle position, step and rides

        :param options: AvailableRides list for a current vehicle
        :param vehicle: a vehicle to operate with
        :return False if no options selected, True if a ride assigned to 
        the vehicle
        """
        c_sum = 0
        rand = ACO._get_random()
        # destination, probability
        for d, pb in options:
            if c_sum < rand < c_sum + pb:
                vehicle.move(d)
                return True
            c_sum += pb
        return False

    def _reset(self):
        self.targets = [t.create_state() for t in self.data.targets]
        self.vehicles = [v.create_state(self.data.depots)
                         for v in self.data.vehicles]

    def _iteration(self):
        """Do one iteration for each vehicle

        :return False if no new assignments, else True"""
        vehicle = self.vehicles[0]
        result = False
        while True:
            options = self._get_available_options(vehicle)
            if not options:
                break
            result = self._select_option(vehicle, options)
        self.pheromone.update([(self.get_score([vehicle]), vehicle)])
        return result

    def run(self):
        """Run iterations till no improvements left"""
        i = 0
        best = float('inf')
        for i in range(1000):
            self._iteration()
            i += 1
            score = self.get_score()
            if score < best:
                best = score
                self.display()
                print("Iteration {} => score {}".format(i, score))
            self._reset()
        print("After {} iterations score is {}".format(i, best))
