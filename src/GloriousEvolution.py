import random
from functools import total_ordering
from Simulation import Simulation

class GloriousEvolution:
    def __init__(self, city_plan, population_size = 10, number_of_generations = 10) :
        random.seed()
        self.city_plan = city_plan
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.current_gen = self.generation_initializer()

    def generation_initializer(self):
        gen = []
        for _ in range(self.population_size):
            gen.append(Simulation(self.city_plan, "random"))
        return gen
    

    # run simulations for current generation and get reproductove probabilities
    def run_current(self):
        total_score = 0     # combined score of all individuals of this gen
        probability = 0
        #calculate each simulation's score
        for simulation in self.current_gen:
            simulation.run()
            total_score += simulation.score
        #assess each simulation reproductive probability, each object as the lowest value in probability interval that will choose it 
        for i in range(self.population_size):
            simulation = self.current_gen[i]
            if i == self.population_size-1:
                simulation.reproductive_probability = 1
                print("probability: " + str(simulation.reproductive_probability)+ ", score: " + str(simulation.score))
                break
            probability += simulation.score / total_score
            simulation.reproductive_probability = probability
            print("probability: " + str(simulation.reproductive_probability)+ ", score: " + str(simulation.score))

    def reproduction(self):
        # generate lists of parents for each individual in new gen in 2 different lists
        parent1 = []
        parent2 = []
        for index in range(self.population_size):
            p1 = random.random()
            for sim in self.current_gen:
                if p1 < sim.reproductive_probability:
                    parent1.append(sim)
            p2 = random.random()
            for i in range(self.population_size):
                sim = self.current_gen[i]
                if p2 < sim.reproductive_probability and sim != parent1[index]:
                    parent2.append(sim)




            # new_sim = Simulation
            # new_gen.append(new_sim)
