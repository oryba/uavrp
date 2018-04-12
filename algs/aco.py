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

        self.last_productive_iteration = 0

        random.seed('seed')

    def get_score(self, vehicles=None):
        """Calculate a score of current state

        :return integer score"""
        score = 0
        for vehicle in (vehicles or self.vehicles):
            if vehicle.points:
                points = [p for p in vehicle.points]
                score += sum([p - n for p, n in zip(points, points[1:])])

        return score

    @staticmethod
    def _get_random():
        return random.uniform(0, 1)

    def _edge_probabilities(self, options, two_steps_options=None):
        # tuple (option, value)
        numerators = []
        for d in options:
            numerators.append((d, (max(self.pheromone[d.vehicle.position][d.milestones[-1]], 0.01) ** self.params.a) *
                      ((1 / d.distance) ** self.params.b)))
        if two_steps_options:
            for d in two_steps_options:
                numerators.append((d, (
                    # pheromone part
                    (self.pheromone[d.vehicle.position][d.milestones[-2]] * self.pheromone[d.milestones[-2]][d.milestones[-1]]
                    ) ** self.params.a) *
                    # heuristic info part
                    ((1 / (d.vehicle.position - d.milestones[-2]) + 1 / (d.milestones[-2] - d.milestones[-1])
                    ) ** self.params.b)
                    )
                )
        denominator = sum([n[1] for n in numerators])
        # tuple (destination, probability)
        return [(n[0], n[1]/denominator) for n in numerators]

    def _get_available_options(self, vehicles: [VehicleState]):
        """Select options available for the vehicle

        :param vehicle: current vehicle with its state
        :return AvailableOptions list"""
        options = []
        two_steps_options = []
        for v in vehicles:
            v_options = v.distance_to_list(self.targets)
            if not v_options:
                v.move_to_depot()
            else:
                if self.params.two_steps:
                    for opt in v_options:
                        temp_v = v.get_copy()
                        temp_v.move(opt, skip_marking=True)
                        temp_options = temp_v.distance_to_list(self.targets)
                        if not temp_options:
                            continue
                        for t in temp_options:
                            t.vehicle = v
                            t.distance += opt.distance
                            t.milestones = opt.milestones + t.milestones
                        two_steps_options.extend(temp_options)
                        del temp_v
                options += v_options
        return self._edge_probabilities(options, two_steps_options)

    @staticmethod
    def _select_option(options):
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
        for opt, pb in options:
            if c_sum < rand < c_sum + pb:
                opt.vehicle.move(opt)
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
        result = False
        while True:
            options = self._get_available_options(self.vehicles)
            if not options:
                for v in self.vehicles:
                    v.move_to_depot()
                options = self._get_available_options(self.vehicles)
                # even with repeatable flights
                if not options:
                    break
            result = self._select_option(options)
        if len([t for t in self.targets if not t.visited]) > 0:
            return False
        if self._get_random() > 0.9:
            self._local(self.vehicles)
        self.pheromone.update(self.get_score(self.vehicles), self.vehicles)
        return result

    def run(self, silent=False):
        """Run iterations till no improvements left"""
        best = float('inf')
        best_solution = []
        for i in range(self.params.iterations):
            if not self._iteration():
                # self.pheromone.evaporation()
                self._reset()
                continue
            score = self.get_score()
            if score < best:
                self._local(self.vehicles, light=False)
                best = self.get_score()
                best_solution = [v.get_copy() for v in self.vehicles]
                if self.pheromone.q > best:
                    self.pheromone.q = best
                # self.display()
                self.last_productive_iteration = i
                if not silent:
                    print("Iteration {} => score {}".format(i, best))
            self._reset()
        self.display(best_solution)
        self.vehicles = best_solution
        if not silent:
            print("After {} iterations score is {}".format(i, best))
        return best
