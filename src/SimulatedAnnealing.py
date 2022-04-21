import random
import math


""" Different types of temperature schedules """


class MultMonotonicCooling:
    def get_temperature(self, t0: float, alpha: float, i: int) -> float:
        """Override"""
        pass


class AddMonotonicCooling:
    def get_temperature(self, t0: float, file_name: str) -> str:
        """Override"""
        pass


class NonMonotonicAdaptCooling:
    def get_temperature(self, t0: float, file_name: str) -> str:
        """Override"""
        pass


class ExponentialMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 * (alpha ** i)


class LogarithmicMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * math.log(1 + i, 10))


class LinearMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * i)


class QuadraticMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * (i ** 2))


""" Simulated Annealing optimization algorithm """


class SimulatedAnnealing:
    def __init__(self, simulation, t_schedule_type):
        self.simulation = simulation
        self.t_schedule_type = t_schedule_type

    def temp_schedule(self, t_schedule_type, t0, i):
        alpha = 0.85

        if t_schedule_type == 1:
            return ExponentialMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 2:
            return LogarithmicMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 3:
            return LinearMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 4:
            return QuadraticMult.get_temperature(self, t0, alpha, i)
        else:
            print("ERROR IN TEMP SCHEDULE")

    def random_neighbour(self, inter_prob, light_prob):
        for inter in self.simulation.intersections:
            if random.random() > inter_prob:
                for light in inter.traffic_lights:
                    if random.random() > light_prob:
                        light.time = random.randint(1, self.simulation.duration)

    def accept_with_prob(self, values_diff, t):
        return random.random() > math.e ** (values_diff / t)

    def value(self, state):
        self.simulation.set_state(state)
        self.simulation.run()
        return self.simulation.score

    def run(self, n_iterations, t0, schedule_type):
        current_state = self.simulation.output_state_copy()

        for i in range(n_iterations):
            t = self.temp_schedule(schedule_type, t0, i)

            self.random_neighbour(0.5, 0.5)
            next_state = self.simulation.output_state_copy()
            values_diff = self.value(current_state) - self.value(next_state)

            if values_diff > 0 or self.accept_with_prob(values_diff, t):
                current_state = next_state
            else:
                self.simulation.set_state(current_state)
