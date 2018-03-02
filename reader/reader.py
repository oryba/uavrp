"""
Input processor
"""

from entities import Point, Ride, Header, Data

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


class VehicleAssignmentReader(Reader):
    def process(self):
        with open(self.input_file, 'r') as f:
            header = [int(i) for i in f.readline().split()]
            body = [[int(i) for i in row.split()] for row in f.readlines()]
            return self._get_data(header, body)

    def _get_data(self, head, body):
        def _parse_ride(r, idx) -> Ride:
            start = Point(r[0], r[1])
            end = Point(r[2], r[3])
            start_time, end_time = r[4], r[5]
            return Ride(idx, start, end, start_time, end_time, True)

        header = Header(*head)
        rides = [_parse_ride(ride, idx) for idx, ride in enumerate(body)]
        return Data(header, rides)
