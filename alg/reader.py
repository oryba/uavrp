"""
Description
"""

from attrdict import AttrDict
from entities import Data, get_data

__version__ = "0.1"
__author__ = "oyarush"
__credits__ = ["oyarush"]


class Reader:

    params = []

    def __init__(self, input_file):

        self.input_file = input_file
        self.data = AttrDict()

    def get(self):
        for param in self.params:
            if param not in self.data:
                raise ValueError
        return self.data

    def process(self):
        raise NotImplementedError


class PizzaReader(Reader):
    params = ['R', 'C', 'L', 'H', 'M', 'T']

    def process(self):

        with open(self.input_file, 'r') as f:
            self.data['R'], self.data['C'], self.data['L'], self.data['H'] = f.readline().split()
            matrix = f.readlines()

        M = []
        T = []
        for row in matrix:
            row_list = row.split('')
            M.append([1 if item == 'M' else 0 for item in row_list])
            T.append([1 if item == 'T' else 0 for item in row_list])

        self.data['M'] = M
        self.data['T'] = T


class KnapsackReader(Reader):
    params = ['W', 'pack']

    def process(self):

        with open(self.input_file, 'r') as f:
            header = [int(i) for i in f.readline().split()]
            body = [[int(i) for i in row.split()] for row in f.readlines()]
            self.data = get_data(header, body)

    def get(self):
        return self.data