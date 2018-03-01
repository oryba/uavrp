"""
Description
"""

from random import randint

import numpy as np

from alg.alg import Alg

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush", "oryba"]


class Knapsnack(Alg):
    def init_population(self):
        first = [0 for _ in range(len(self.data.pack))]
        second = [0 for _ in range(len(self.data.pack))]
        first[0] = 1
        second[1] = 1
        self.population = [
            [first, self.fitness(first)],
            [second, self.fitness(second)]
        ]

    def fitness(self, person):

        return np.sum(self.data.pack[i][1] for i, item in enumerate(person) if item)

    def validate_person(self, person) -> bool:

        return np.sum(self.data.pack[i][1] for i, item in enumerate(person) if item) < self.data.W

    def populate(self) -> list:

        new_population = []
        for i in range(len(self.population) - 1):
            for j in range(i, len(self.population)):
                new_population.append([
                    self.crossover(
                        self.population[i][0],
                        self.population[j][0]
                    ),
                    None
                ])
        return new_population + self.population

    def crossover(self, individual1, individual2):

        return individual1[:3] + individual2[3:]

    def mutate_person(self, person):

        index = randint(0, len(person) - 1)
        person[index] = 0 if person[index] else 1
        return person
