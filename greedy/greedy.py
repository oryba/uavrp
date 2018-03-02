"""
Greedy algorithm for vehicle assignment problem
"""
from entities import Vehicle, Header, Point, Ride, AvailableRide

__version__ = "0.1"
__author__ = "oryba"
__credits__ = ["oryba"]


class Greedy():
    """Greedy algorithm, stores all parameters and states while solving"""
    def __init__(self, header: Header, rides: [Ride]):
        self.header = header
        self.rides = rides
        self.vehicles = self._generate_vehicles()

    def _generate_vehicles(self):
        """Initial vehicles list generation"""
        vehicles = []
        for idx in range(self.header.vehicles):
            vehicles.append(
                Vehicle(idx, Point(0, 0), 0, [])
            )
        return vehicles

    def get_score(self):
        """Calculate a score of current state

        :return integer score"""
        score = 0
        for vehicle in self.vehicles:
            for final_ride in vehicle.rides:
                score += final_ride.profit
        return score

    def _get_available_options(self, vehicle: Vehicle):
        """Select options available for the vehicle

        :param vehicle: current vehicle with its state
        :return AvailableOptions list"""
        available = []
        for ride in [r for r in self.rides if r.available]:
            street_delta = ride.start - vehicle.position
            step_delta = ride.start_time - vehicle.step
            # time before the vehicle can start the ride
            delta = max(street_delta, step_delta)
            street_length = ride.end - ride.start
            # bonus
            bonus = (vehicle.step + delta <= ride.start_time)\
                    * self.header.bonus
            # vehicle can't serve this ride
            if vehicle.step + delta + street_length > self.header.steps\
                    or vehicle.step + delta + street_length > ride.end_time:
                continue
            available.append(
                AvailableRide(ride, delta, street_length + bonus)
            )
        return available

    @staticmethod
    def _combine(delta, profit, deltas, profits):
        """An experiment with time and profit combination

        :param delta: time before the vehicle can start the ride
        :param profit: ride estimated profit with bonus
        :param delta: all options deltas list
        :param profits: all options profits list
        :return tuple to sort options"""
        min_delta = min(deltas)
        min_profit = min(profits)
        try:
            return (delta - min_delta)/(max(deltas) - min_delta) + \
               (profit - min_profit)/(max(profits) - min_profit)
        except ZeroDivisionError:
            return delta, -profit

    @staticmethod
    def _simple_decision(delta, profit):
        """Order by time delta before the start first, then by profit

        :param delta: time before the vehicle can start the ride
        :param profit: ride estimated profit with bonus
        :return tuple to sort options"""
        return delta, -profit

    @staticmethod
    def _select_option(options: [AvailableRide], vehicle: Vehicle):
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
                          key=lambda o: Greedy._simple_decision(
                              o.delta, o.profit
                          ))[0]
        selected.ride.available = False
        vehicle.rides.append(selected)
        vehicle.position = selected.ride.end
        vehicle.step += selected.delta + selected.profit
        return True

    def _iteration(self):
        """Do one iteration for each vehicle

        :return False if no new assignments, else True"""
        improve = False
        for vehicle in self.vehicles:
            options = self._get_available_options(vehicle)
            current_improve = Greedy._select_option(options, vehicle)
            improve = improve or current_improve
        return improve

    def run(self):
        """Run iterations till no improvements left"""
        i = 0
        while self._iteration():
            i += 1
            print("Iteration {} => score {}".format(i, self.get_score()))
        print("After {} iterations score is {}".format(i, self.get_score()))

    def output(self, output_file):
        """Save the solution to output file"""
        rows = []
        for vehicle in self.vehicles:
            rides = [str(final_ride.ride.idx) for final_ride in vehicle.rides]
            rows.append(
                "{} {}\n".format(
                    len(rides),
                    " ".join(rides)
                )
            )
        with open(output_file, "w") as f:
            f.writelines(rows)


