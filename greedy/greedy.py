from recordclass import recordclass
from entities import Vehicle, Header, Point, Ride


AvailableRide = recordclass('AvailRide', ['ride', 'dif', 'profit'])


class Greedy():
    def __init__(self, header: Header, rides: [Ride]):
        self.header = header
        self.rides = rides
        self.vehicles = self._generate_vehicles()

    def _generate_vehicles(self):
        vehicles = []
        for idx in range(self.header.vehicles):
            vehicles.append(
                Vehicle(idx, Point(0, 0), 0, [])
            )
        return vehicles

    def score_wo_bonus(self):
        score = 0
        for vehicle in self.vehicles:
            for final_ride in vehicle.rides:
                score += final_ride.ride.end - final_ride.ride.start
        return score

    def _get_available_options(self, vehicle: Vehicle):
        available = []
        for ride in [r for r in self.rides if r.available]:
            street_dif = ride.start - vehicle.position
            step_dif = ride.start_time - vehicle.step
            dif = max(street_dif, step_dif)
            street_length = ride.end - ride.start
            # vehicle can't serve this ride
            if vehicle.step + dif + street_length > self.header.steps\
                    or vehicle.step + dif + street_length > ride.end_time:
                continue
            available.append(
                AvailableRide(ride, dif, street_length)
            )
        return available

    def _select_option(self, options: [AvailableRide], vehicle: Vehicle):
        if not options:
            return False
        selected = sorted(options, key=lambda o: (o.dif, -o.profit))[0]
        selected.ride.available = False
        vehicle.rides.append(selected)
        vehicle.position = selected.ride.end
        vehicle.step += selected.dif + selected.profit
        return True

    def _iteration(self):
        improve = False
        for vehicle in self.vehicles:
            options = self._get_available_options(vehicle)
            current_improve = self._select_option(options, vehicle)
            improve = improve or current_improve
        return improve

    def run(self):
        i = 0
        while self._iteration():
            i += 1
            print("Iteration {} => score {}".format(i, self.score_wo_bonus()))
        print("After {} iters score is {}".format(i, self.score_wo_bonus()))

    def output(self, output_file):
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


