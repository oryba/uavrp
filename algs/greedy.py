import itertools

from algs.base import Alg
from entities import *


__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


class Greedy(Alg):
    """Greedy algorithm, stores all parameters and states while solving"""
    def __init__(self, data: Data):
        super().__init__(data)

    def get_score(self):
        """Calculate a score of current state

        :return integer score"""
        score = 0
        for vehicle in self.vehicles:
            if vehicle.points:
                points = [p for p in vehicle.points]
                score += sum([p - n for p, n in zip(points, points[1:])])
                score += min(
                    [d.distance for d in vehicle.distance_to_list(vehicle.depots)]
                )

        return score

    def _get_available_options(self, vehicle: VehicleState):
        """Select options available for the vehicle

        :param vehicle: current vehicle with its state
        :return AvailableOptions list"""
        return vehicle.distance_to_list([target for target in self.targets
                                  if not target.visited]) or []

    @staticmethod
    def _select_option(options: [AvailableOption]):
        """
        Choose the best option for the vehicle on the iteration. Modifies
        a ride availability, a vehicle position, step and rides

        :param options: AvailableRides list for a current vehicle
        :param vehicle: a vehicle to operate with
        :return False if no options selected, True if a ride assigned to 
        the vehicle
        """
        if not options:
            return False
        selected = sorted(options,
                          key=lambda o: o.distance)[0]
        return selected.vehicle.move(selected)

    def _iteration(self):
        """Do one iteration for each vehicle

        :return False if no new assignments, else True"""
        improve = False
        options = list(itertools.chain.from_iterable(
            [self._get_available_options(v) for v in self.vehicles]
        ))
        if not options:
            return False
        self._select_option(options)
        return True

    def run(self):
        """Run iterations till no improvements left"""
        i = 0
        while self._iteration():
            i += 1
            print("Iteration {} => score {}".format(i, self.get_score()))
        print("After {} iterations score is {}".format(i, self.get_score()))
