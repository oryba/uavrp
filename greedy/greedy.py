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
                score += final_ride.profit
        return score

    def _get_available_options(self, vehicle: Vehicle):
        available = []
        for ride in [r for r in self.rides if r.available]:
            street_dif = ride.start - vehicle.position
            step_dif = ride.start_time - vehicle.step
            dif = max(street_dif, step_dif)
            street_length = ride.end - ride.start
            # bonus
            bonus = (vehicle.step + dif <= ride.start_time) * self.header.bonus
            # vehicle can't serve this ride
            if vehicle.step + dif + street_length > self.header.steps\
                    or vehicle.step + dif + street_length > ride.end_time:
                continue
            available.append(
                AvailableRide(ride, dif, street_length + bonus)
            )
        return available

    def _combine(self, dif, profit, difs, profits):
        min_dif = min(difs)
        min_profit = min(profits)
        try:
            return (dif - min_dif)/(max(difs) - min_dif) + \
               (profit - min_profit)/(max(profits) - min_profit)
        except:
            return dif, -profit

    def _simple_decision(self, dif, profit):
        return dif, -profit

    def _select_option(self, options: [AvailableRide], vehicle: Vehicle):
        if not options:
            return False
        profits = [op.profit for op in options]
        difs = [op.dif for op in options]
        min_profits = min(profits)
        max_profits = max(profits)
        min_difs = min(difs)
        max_difs = max(difs)
        selected = sorted(options, key=lambda o: (o.dif - min_difs)/(max_difs - min_difs) + \
               (o.profit - min_profits)/(max_profits - min_profits) if (max_difs - min_difs) > 0 and (max_profits - min_profits) > 0 else (o.dif, -o.profit))[0]
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


