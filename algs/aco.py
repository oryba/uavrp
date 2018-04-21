import itertools
import random
import numpy as np

from algs.base import Alg
from entities import *
from .local import local_2opt, get_score as local_score
from functools import lru_cache


__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


class ACO(Alg):
    """ACO algorithm, stores all parameters and states while solving"""
    def __init__(self, data: Data, params: ACOParams, rand_seed='seed'):
        super().__init__(data)
        self.data = data
        self.params = params

        self.base_vehicles = data.vehicles
        self.n = data.header.depots + data.header.targets

        self.last_productive_iteration = 0

        self.points = list(enumerate([Point(0, 0, free=True)] + self.depots + self.targets))
        self.n = len(self.points)
        self.tg_n = len(self.targets)
        self.index_depots = list(range(1, len(self.depots) + 1))
        self.index_targets = list(range(len(self.depots) + 1, self.n))
        self.C = np.zeros((self.n, self.n)) # distance matrix
        self.V = np.zeros((self.n, ), dtype=bool) # visited vector
        self.X = np.zeros((self.n, self.n, len(self.vehicles)), dtype=bool)
        self.ph = NewPheromone(self.points,
                                   params.p, params.q)

        self.points_transformer = dict(self.points)

        for i, v in enumerate(self.vehicles):
            v.idx = i
            v.points = []

        for i, p in self.points:
            for j, q in self.points:
                if i != j:
                    if (i == 0 or i in self.index_depots) and j in self.index_depots:
                            self.C[i][j] = float('inf')
                    else:
                        self.C[i][j] = p - q
                else:
                    self.C[i][j] = float('inf')

        for j in range(self.n):
            if j in self.index_targets:
                self.C[0][j] = self._get_closest_depot(j)[1]

        self.max_length = 0
        for i in range(self.n):
            for j in range(self.n):
                v = self.C[i][j]
                if not np.isinf(v) and v > self.max_length:
                    self.max_length = v
        self.max_length *= 1.1

        random.seed(rand_seed)

    @lru_cache(None)
    def _get_path_score(self, points):
        return sum([self.C[a][b] for a, b in zip(points, points[1:])])

    def get_score(self, vehicles=None):
        """Calculate a score of current state

        :return integer score"""
        score = 0
        for vehicle in (vehicles or self.vehicles):
            if vehicle.points:
                points = [p for p in vehicle.points]
                score += self._get_path_score(PointsList(points))

        return score

    @staticmethod
    def _get_random():
        return random.uniform(0, 1)

    def _edge_probabilities(self, options, two_steps_options=None):
        # tuple (option, value)
        numerators, two_steps_numerators = [], []
        for d in options:
            numerators.append((d, (max(self.pheromone[d.vehicle.position][d.milestones[-1]], 0.01) ** self.params.a) *
                      ((1 / d.distance) ** self.params.b)))
        if two_steps_options:
            for d in two_steps_options:
                two_steps_numerators.append((d, (
                    # pheromone part
                    (self.pheromone[d.vehicle.position][d.milestones[-2]] * self.pheromone[d.milestones[-2]][d.milestones[-1]]
                    ) ** self.params.a) *
                    # heuristic info part
                    (((1 / (d.vehicle.position - d.milestones[-2])) + (1 / (d.milestones[-2] - d.milestones[-1]))
                    ) ** self.params.b)
                    )
                )
        single = 0 if two_steps_options else 1
        two = 1
        denominator = sum([n[1] for n in numerators])
        two_steps_denominator = sum([n[1] for n in two_steps_numerators])
        # tuple (destination, probability)
        single_res = [(n[0], n[1] * single / denominator) for n in numerators]
        two_res = [(n[0], n[1] * two / two_steps_denominator) for n in two_steps_numerators]
        return single_res + two_res

    @lru_cache(None)
    def _get_closest_depot(self, i):
        return min([(d, self.C[i][d]) for d in self.index_depots],
            key=lambda d: d[1])

    def _check_flight(self, reserve, i, j, allow_depots=False):
        if allow_depots and j in self.index_depots:
            wayback = 0
        else:
            wayback = self._get_closest_depot(j)[1]
        if reserve < wayback + self.C[i][j]:
            return False
        else:
            return True

    @staticmethod
    @lru_cache(None)
    def _calc_p(tau, dist, a, b):
        return (tau ** a) * (
            (1 / dist) ** b)

    def _get_ways(self, vehicles, skip=[]):
        options = []
        numerators = []
        additional_options = []
        way_ids = []
        for v in vehicles:
            i = v.np
            for j in range(self.n):
                if (j in self.index_targets and self.V[j]) or self.C[i][j] == float('inf') or not self._check_flight(v.reserve, i, j):
                    continue
                if self.params.two_steps:
                    for k in range(self.n):
                        if (k in self.index_targets and self.V[k]) or \
                            self.C[j][k] == float('inf') or k == j \
                            or not self._check_flight(v.reserve - self.C[i][j], j, k, allow_depots=True):
                            continue
                        # numerators.append(
                        #     ((self.ph[i][j] * self.ph[j][k]) ** self.params.a) * (
                        #     (1 / (1 + self.C[i][j]) + 1 / (1 + self.C[j][k])) ** self.params.b)
                        # )
                        numerators.append(
                            (
                                ACO._calc_p(self.ph[i][j], self.C[i][j], self.params.a, self.params.b)
                            ) * (
                                ACO._calc_p(self.ph[j][k], self.C[j][k],
                                            self.params.a, self.params.b)
                            )
                        )
                        way_ids.append((v, [j, k]))
                # else:
                numerators.append(
                    ACO._calc_p(self.ph[i][j], self.C[i][j], self.params.a,
                                self.params.b)
                )
                way_ids.append((v, [j]))  # vehicle and next vertices
        if not numerators:
            return None
        numerators = [(n if not np.isinf(n) else 1) for n in numerators]
        denominator = sum(numerators)
        return [(([j[0], j[1]]), n / denominator) for n, j in zip(numerators, way_ids)]


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
                        temp_options = temp_v.distance_to_list(self.targets + self.depots)
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

    def _select_option(self, options):
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
        for ps, pb in options:
            if c_sum < rand < c_sum + pb:
                source = ps[0].np
                for destination in ps[1]:
                    # self.X[ps[0].np][ps[1]][ps[0].idx] = True
                    if destination in self.index_depots:
                        ps[0].reserve = ps[0].vehicle.dist
                    else:
                        ps[0].reserve -= self.C[source][destination]
                    if source == 0:
                        ps[0].points.append(
                            self._get_closest_depot(destination)[0]
                        )
                    ps[0].np = destination
                    ps[0].points.append(destination)
                    self.V[destination] = True
                    source = destination
                return True
            c_sum += pb
        return False

    def _move_to_depot(self, vehicle: VehicleState):
        i = vehicle.np
        if i in self.index_depots:
            return True
        closest_depot, distance = self._get_closest_depot(i)
        vehicle.reserve = vehicle.vehicle.dist
        self.X[i][closest_depot][vehicle.idx] = True
        vehicle.points.append(closest_depot)
        vehicle.np = closest_depot

    def _reset(self):
        for v in self.vehicles:
            v.points = []
            v.reserve = v.vehicle.dist
            v.np = 0
        self.V = np.zeros((self.n, ), dtype=bool)

    def _make_2opt(self, seq: PointsList, i, j):
        new_seq = seq.copy()
        new_seq[i:j] = seq[j - 1:i - 1:-1]
        return new_seq

    def _2_opt(self, points):
        n = len(points)
        if n < 4:
            return points, self._get_path_score(PointsList(points))
        neighbours = [points]
        for i in range(1, n - 1):
            for j in range(i + 2, n):
                neighbours.append(self._make_2opt(points, i, j))
        return min(
            map(lambda n: (n, self._get_path_score(PointsList(n))), neighbours),
            key=lambda pairs: pairs[1])

    def _local(self, vehicles: [VehicleState], light=False):
        self.ls_number += 1
        for v in vehicles:
            if v.points:
                # TODO improve 2opt
                # we can optimize only chunks between depots
                depots_indices = [i for i, p in enumerate(v.points)
                                  if p in self.index_depots]
                current_score = self.get_score([v])
                # for each chunk
                for i, j in zip(depots_indices, depots_indices[1:]):
                    while True:
                        v.points[i:j+1], _ = self._2_opt(PointsList(v.points[i:j+1]))
                        score = self.get_score([v])
                        if score < current_score:
                            current_score = score
                        else:
                            break
        return vehicles

    def _iteration(self):
        """Do one iteration for each vehicle

        :return False if no new assignments, else True"""
        result = False
        while True:
            options = self._get_ways(self.vehicles)
            if not options:
                for v in self.vehicles:
                    self._move_to_depot(v)
                options = self._get_ways(self.vehicles)
                # even with repeatable flights
                if not options:
                    break
            result = self._select_option(options)
        if len([1 for t in self.index_targets if not self.V[t]]) > 0:
            return False
        if self._get_random() > 0.95:
            self._local(self.vehicles)
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
            if i == 100:
                ll =0
            score = self.get_score()
            if score < best:
                self._local(self.vehicles, light=False)
                best = self.get_score()
                best_solution = [v.get_copy() for v in self.vehicles]
                if self.ph.q > best:
                    self.ph.q = best
                # self.display()
                self.last_productive_iteration = i
                if not silent:
                    print("Iteration {} => score {}".format(i, best))
            self.ph.update(self.get_score(self.vehicles), self.vehicles)
            if self.ph.q > best:
                self.ph.q = best
            self._reset()
        # self.display(best_solution)
        self.vehicles = best_solution
        if not silent:
            print("After {} iterations score is {}".format(i, best))
        return best

    def display(self, vehicles=None):
        g = Graph()

        g.add_points(self.targets + self.obstacles + self.depots)

        for v in (vehicles or self.vehicles):
            if not v.points:
                continue
            for p, n in zip(v.points, v.points[1:]):
                g.add_edge(Edge(
                    self.points_transformer[p],
                    self.points_transformer[n],
                    v.vehicle.color))

        p = Plotter(g)
        p.plot_points()
        p.plot_edges()
        p.show()
