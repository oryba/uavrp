from recordclass import recordclass


individual_record = recordclass('Individual', ['code', 'fitness'])


class Individual(individual_record):
    def __hash__(self):
        return hash((hash(el) for el in self.code))


Header = recordclass('Header', ['rows', 'cols', 'vehicles', 'rides',
                                  'bonus', 'steps'])

Ride = recordclass('Ride', ['idx', 'start', 'end', 'start_time', 'end_time',
                            'available'])

Data = recordclass('Data', ['header', 'rides'])

BasePoint = recordclass('Point', ['x', 'y'])


class Point(BasePoint):
    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


Vehicle = recordclass('Vehicle', ['idx', 'position', 'step', 'rides'])


def get_data(head, body):
    def _parse_ride(r, idx) -> Ride:
        start = Point(r[0], r[1])
        end = Point(r[2], r[3])
        start_time, end_time = r[4], r[5]
        return Ride(idx, start, end, start_time, end_time, True)

    header = Header(*head)
    rides = [_parse_ride(ride, idx) for idx, ride in enumerate(body)]
    return Data(header, rides)


