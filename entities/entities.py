"""
Prototypes of involved objects
"""
from recordclass import recordclass

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]

# Ride container with calculated time delta and profit
AvailableRide = recordclass('AvailRide', ['ride', 'delta', 'profit'])

# Problem properties
Header = recordclass('Header', ['rows', 'cols', 'vehicles', 'rides',
                                  'bonus', 'steps'])
# Ride with its properties
Ride = recordclass('Ride', ['idx', 'start', 'end', 'start_time', 'end_time',
                            'available'])

# Problem data with headers and rides set
Data = recordclass('Data', ['header', 'rides'])

# Map point base class
BasePoint = recordclass('Point', ['x', 'y'])


# Map point
class Point(BasePoint):
    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


# Vehicle with its properties
Vehicle = recordclass('Vehicle', ['idx', 'position', 'step', 'rides'])
