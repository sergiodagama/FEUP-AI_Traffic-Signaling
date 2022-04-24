import random
import math
import matplotlib.pyplot as plt


""" Different types of temperature schedules """


class MultMonotonicCooling:
    def get_temperature(self, t0: float, alpha: float, i: int) -> float:
        """Override"""
        pass


class AddMonotonicCooling:
    def get_temperature(self, t0: float, tn: float, i: int, n: int) -> float:
        """Override"""
        pass


""" Multiplicative Monotonic Cooling """


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


""" Additive Monotonic Cooling """


class LinearAdd(AddMonotonicCooling):
    def get_temperature(self, t0, tn, i, n):
        return tn + (t0 - tn) * ((n - i) / n)


class QuadAdd(AddMonotonicCooling):
    def get_temperature(self, t0, tn, i, n):
        return tn + (t0 - tn) * (((n - i) / n) ** 2)


""" Non-Monotonic Adaptive Cooling """


class NonMonotonicAdaptCooling:
    def get_temperature(self, current_score, best_score, t):
        return (1 + (current_score - best_score) / current_score) * t


""" Simulated Annealing optimization algorithm """


class SimulatedAnnealing:
    def __init__(self, simulation):
        self.simulation = simulation

    def temp_schedule(self, t_schedule_type, t0, i, tn, n, is_non_mono, current_score, best_score):
        alpha = 0.85
        t = 0

        if t_schedule_type == 1:
            t = ExponentialMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 2:
            t = LogarithmicMult.get_temperature(self, t0, 2, i)
        elif t_schedule_type == 3:
            t = LinearMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 4:
            t = QuadraticMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 5:
            t = LinearAdd.get_temperature(self, t0, tn, i, n)
        elif t_schedule_type == 6:
            t = QuadAdd.get_temperature(self, t0, tn, i, n)
        else:
            print("ERROR IN TEMP SCHEDULE")

        if is_non_mono:
            return NonMonotonicAdaptCooling.get_temperature(self, current_score, best_score, t)

        return t

    def random_neighbour(self, inter_prob, light_prob):
        for inter in self.simulation.intersections:
            if random.random() > inter_prob:
                for light in inter.traffic_lights:
                    if random.random() > light_prob:
                        light.time = random.randint(1, self.simulation.duration)

    def accept_with_prob(self, values_diff, t):
        try:
            if t != 0:
                return random.random() < math.exp(values_diff / t)
            else:
                return False
        except OverflowError:
            return False

    def value(self, state):
        self.simulation.set_state(state)
        self.simulation.run()
        return self.simulation.score

    def run(self, n_iterations, t0, schedule_type, tn, is_non_mono):
        best = self.simulation.output_state_copy()
        best_score = self.value(best)

        t_values = []
        i_values = []
        s_values = []

        for i in range(n_iterations):
            current_state = self.simulation.output_state_copy()
            current_score = self.value(current_state)

            t = self.temp_schedule(schedule_type, t0, i, tn, n_iterations, is_non_mono, current_score, best_score)

            t_values.append(t)
            i_values.append(i)

            s_values.append(current_score)

            self.random_neighbour(0.1, 0.1)
            next_state = self.simulation.output_state_copy()

            if self.value(best) < self.value(current_state):
                best = self.simulation.output_state_copy()
                best_score = self.value(current_state)

            values_diff = self.value(next_state) - self.value(current_state)

            print("iteration: [" + str(i) + "]" + " best score: " + str(best_score) + " temperature: " + str(t) + " acceptance prob: " + str(self.accept_with_prob(values_diff, t)), end="\n")
            # print("\ncurr state: ", self.simulation.print_state(current_state), end="\n")
            # print("\nnext state: ", self.simulation.print_state(next_state), end="\n")

            if values_diff >= 0:
                current_state = next_state
            else:
                if self.accept_with_prob(values_diff, t):
                    current_state = next_state

            self.simulation.set_state(current_state)

        plt.plot(i_values, s_values, color='green', linewidth=2,
                     marker='o', markerfacecolor='blue', markersize=4)
        plt.ylabel('Score')
        plt.xlabel('Iteration')
        plt.show()

        plt.plot(i_values, t_values)
        plt.ylabel('Cooling Schedule')
        plt.show()

        return best, best_score
