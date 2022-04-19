import random
import math


class SimulatedAnnealing:
    def __init__(self, simulation):
        self.simulation = simulation

    def temp_schedule(self, t):
        pass

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

    def run(self, n_iterations, init_state, t0):
        t = t0
        current_state = init_state

        for i in range(n_iterations):
            t = self.temp_schedule(t)

            next_state = self.random_neighbour(0.5, 0.5)

            values_diff = self.value(current_state) - self.value(current_state)

            if values_diff > 0 or self.accept_with_prob(values_diff, t):
                current_state = next_state
