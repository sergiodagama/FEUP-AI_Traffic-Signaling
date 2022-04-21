import random
from Simulation import Simulation

class GloriousEvolution:
    def __init__(self, city_plan, radiation_dosage = 0.05, population_size = 10, number_of_generations = 10) :
        random.seed()
        self.city_plan = city_plan
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.radiation_dosage = radiation_dosage
        self.current_gen = self.generation_initializer()

    def generation_initializer(self):
        gen = []
        for _ in range(self.population_size):
            gen.append(Simulation(self.city_plan, "random"))
        return gen
    
    def run(self):
        for _ in range(self.number_of_generations):
            self.run_current_gen() 
            self.reproduce()

    # run simulations for current generation and get reproductove probabilities
    def run_current_gen(self):
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
                # print("probability: " + str(simulation.reproductive_probability)+ ", score: " + str(simulation.score))
                break
            probability += simulation.score / total_score
            simulation.reproductive_probability = probability
            # print("probability: " + str(simulation.reproductive_probability)+ ", score: " + str(simulation.score))

    def reproduce(self):
        random.seed()
        # generate lists of parents for each individual in new gen in 2 different lists
        parent = [[],[]]
        for _ in range(self.population_size):
            get_parent1 = True
            get_parent2 = True
            rand1 = random.random()
            rand2 = random.random()
            # print("randoms (" + str(rand1) + ", " + str(rand2) + ")")
            for sim in self.current_gen:
                if rand1 <= sim.reproductive_probability and get_parent1:
                    get_parent1 = False
                    parent[0].append(sim.output_state_copy())
                if rand2 <= sim.reproductive_probability and get_parent2:
                    get_parent2 = False
                    parent[1].append(sim.output_state_copy())
        # print(len(parent),len(parent[0]),len(parent[1]))
        for i in range(self.population_size):
            new_state = [x.replicate() for x in parent[0][i]]
            for j in range(len(new_state)):
                if (new_state[j].num_of_lights < 2 and random.randint(0,1) > 0.5):
                    continue
                for r in random.sample(range(0,new_state[j].num_of_lights),(new_state[j].num_of_lights+1) // 2):
                    genetic_code = next((x for x in parent[1][i][j].traffic_lights if x.street.street_name == new_state[j].traffic_lights[r].street.street_name),None)
                    if genetic_code is None:
                        continue
                    new_state[j].traffic_lights[r] = genetic_code.replicate()
            self.current_gen[i].set_state(new_state)
        # self.radiation()

    def radiation(self):
        for sim in self.current_gen:
            for intersection in sim.intersections:
                for light in intersection.traffic_lights:
                    if random.random() < self.radiation_dosage:
                        if light.time == 0: light.time+=1
                        elif light.time == sim.duration: light.time -= 1
                        else: light.time += random.sample([-1,1],1)[0]

    def run(self):
        best_score = -1
        best_sim = None
        self.run_current_gen()
        for sim in self.current_gen:
            if sim.score > best_score:
                best_score = sim.score
                best_sim = sim
        print("best round score: "+ str(best_score))
        print(best_sim)
        for _ in range(self.number_of_generations):
            best_score = -1
            best_sim = None
            self.reproduce()
            self.run_current_gen()
            for sim in self.current_gen:
                if sim.score > best_score:
                    best_score = sim.score
                    best_sim = sim
            print("best round score: "+ str(best_score))
        print(best_sim)

        