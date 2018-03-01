"""
Description
"""

import operator
import random

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush"]


class Alg:

    def __init__(self, data, iteration, child_number, population_number, chance_mutation):

        self.data = data
        self.iteration = iteration
        self.child_number = child_number
        self.population_number = population_number
        self.chance_mutation = chance_mutation
        self.population = self.init_population()
        self.result = None

    def init_population(self):
        raise NotImplementedError

    def fitness(self, person):
        raise NotImplementedError

    def validate_person(self, person) -> bool:
        raise NotImplementedError

    def filter_population_by_validation(self, population):

        return [[person, score] for person, score in population if self.validate_person(person)]

    def compute_population(self, population):

        for index, (person, score) in enumerate(population):
            if not score:
                population[index][1] = self.fitness(person)

        return sorted(population, key=operator.itemgetter(1), reverse=True)

    def filter_population_by_score(self, population):

        return population[:self.population_number]

    def populate(self) -> list:
        raise NotImplementedError

    def crossover(self, individual1, individual2):
        raise NotImplementedError

    def mutate_person(self, person):

        raise NotImplementedError

    def mutate_population(self, population):

        for index, (person, score) in enumerate(population):

            if random.random() * 100 < self.chance_mutation:
                population[index][0] = self.mutate_person(person)
                population[index][1] = None

        return population

    def run(self):

        self.init_population()
        self.population = self.filter_population_by_validation(self.population)
        self.population = self.compute_population(self.population)
        self.result = self.population[0]
        for _ in range(self.iteration):

            new_population = self.populate()
            new_population = self.mutate_population(new_population)
            new_population = self.filter_population_by_validation(new_population)
            new_population = self.compute_population(new_population)
            new_population = self.filter_population_by_score(new_population)

            self.population = new_population

            if self.result[1] < new_population[0][1]:
                self.result = new_population[0]
