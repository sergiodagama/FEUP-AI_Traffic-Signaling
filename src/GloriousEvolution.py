from Simulation import Simulation

class GloriousEvolution:
    def __init__(self, city_plan_path, population_size = 10, number_of_generations = 10) :
        self.city_plan = city_plan_path
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.current_gen = self.generation_initializer()

    def generation_initializer(self):
        gen = []
        for _ in range(self.population_size):
            gen.append(Simulation(self.city_plan, "random"))
        return gen
    
    def run(self):
        for simulation in self.current_gen:
            simulation.run()