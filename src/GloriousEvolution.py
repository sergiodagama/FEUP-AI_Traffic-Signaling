from copy import deepcopy
import random
import time
import sys
from Simulation import Simulation


class GloriousEvolution:
    def __init__(self, city_plan, radiation_dosage=0.05, population_size=10, number_of_generations=10):
        random.seed()
        self.city_plan = city_plan
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.radiation_dosage = radiation_dosage
        self.current_gen = self.generation_initializer()
        self.best_simulation = None

    def generation_initializer(self):
        gen = []
        for _ in range(self.population_size):
            gen.append(Simulation(self.city_plan, "random"))
        return gen

    def run(self):
        for _ in range(self.number_of_generations):
            self.run_current_gen()
            self.reproduce()

    # run simulations for current generation and get reproductive probabilities
    def run_current_gen(self):
        total_score = 0  # combined score of all individuals of this gen
        probability = 0
        # calculate each simulation's score
        for simulation in self.current_gen:
            simulation.run()
            total_score += simulation.score
        # assess each simulation reproductive probability, each object as the lowest value in probability interval that will choose it
        if total_score == 0:
            raise Exception("No solution found, please check if the city_map is possible")
        for i in range(self.population_size):
            simulation = self.current_gen[i]
            if i == self.population_size - 1:
                simulation.reproductive_probability = 1
                break
            probability += simulation.score / total_score
            simulation.reproductive_probability = probability

    def reproduce(self):
        random.seed()
        # generate lists of parents for each individual in new gen in 2 different lists
        parent = [[], []]
        for _ in range(self.population_size):
            get_parent1 = True
            get_parent2 = True
            rand1 = random.random()
            rand2 = random.random()
            for sim in self.current_gen:
                if rand1 <= sim.reproductive_probability and get_parent1:
                    get_parent1 = False
                    parent[0].append(sim.output_state_copy())
                if rand2 <= sim.reproductive_probability and get_parent2:
                    get_parent2 = False
                    parent[1].append(sim.output_state_copy())
        for i in range(self.population_size):
            new_state = [x.replicate() for x in parent[0][i]]
            for j in range(len(new_state)):
                if new_state[j].num_of_lights < 2 and random.randint(0, 1) > 0.5:
                    continue
                for r in random.sample(range(0, new_state[j].num_of_lights), (new_state[j].num_of_lights + 1) // 2):
                    genetic_code = next((x for x in parent[1][i][j].traffic_lights if
                                         x.street.street_name == new_state[j].traffic_lights[r].street.street_name),
                                        None)
                    if genetic_code is None:
                        continue
                    new_state[j].traffic_lights[r] = genetic_code.replicate()
            self.current_gen[i].set_state(new_state)
        self.radiation()

    def radiation(self):
        for sim in self.current_gen:
            for intersection in sim.intersections:
                if random.random() < self.radiation_dosage:
                    intersection.swap_random()
                for light in intersection.traffic_lights:
                    if random.random() < self.radiation_dosage:
                        if light.time == 0:
                            light.time += 1
                        elif light.time == sim.duration:
                            light.time -= 1
                        else:
                            light.time += random.sample([-1, 1], 1)[0]

    def run(self):
        start_time = time.time()
        best_score = -1
        best_gen_score = -1
        self.run_current_gen()
        for sim in self.current_gen:
            if sim.score > best_gen_score:
                best_gen_score = deepcopy(sim.score)
                if best_gen_score > best_score:
                    best_score = deepcopy(best_gen_score)
                    self.best_simulation = sim.output_state_copy()
        loading_bar_size = 50
        load = loading_bar_size//self.number_of_generations
        print("best overall score: " + str(best_score)+", best round score: "+ str(best_gen_score)+"\ttime left: "+str((time.time()-start_time)*(self.number_of_generations-1))+ 
                "\n["+ str(1) + " out of " + str(self.number_of_generations)+ "] generations complete"+
                "\nLoading[{}{}]".format('#'*load,' '*(loading_bar_size-load)))
        for i in range(1,self.number_of_generations):
            self.reproduce()
            best_gen_score = -1
            self.run_current_gen()
            for sim in self.current_gen:
                if sim.score > best_gen_score:
                    best_gen_score = deepcopy(sim.score)
                    if best_gen_score > best_score:
                        best_score = deepcopy(sim.score)
                        self.best_simulation = sim.output_state_copy()
            sys.stdout.write("\x1b[1A\x1b[2K")
            sys.stdout.write("\x1b[1A\x1b[2K")
            sys.stdout.write("\x1b[1A\x1b[2K")
            load = ((i+1)*loading_bar_size)//self.number_of_generations
            print("best overall score: " + str(best_score)+", best round score: "+ str(best_gen_score)+"\ttime left: "+str((time.time()-start_time)*(self.number_of_generations-i))+ 
                "\n["+ str(i+1) + " out of " + str(self.number_of_generations)+ "] generations complete"+
                "\nLoading[{}{}]".format('#'*load,' '*(loading_bar_size-load)))
        sys.stdout.write("\x1b[1A\x1b[2K")
        sys.stdout.write("\x1b[1A\x1b[2K")
        print("[" + str(self.number_of_generations) + " out of " + str(
            self.number_of_generations) + "] generations complete\nLoading[{}]".format('#' * loading_bar_size))
        print("                                                                      ")
        print("Success! Best score on final generation was: " + str(best_score))
        sim = Simulation(self.city_plan, "array", self.best_simulation)
        sim.print_state(self.best_simulation)
        print("")
        return self.best_simulation
