from Parser import parse_input_file, coord_parser
from Simulation import Simulation
from SimulatedAnnealing import SimulatedAnnealing
from GloriousEvolution import GloriousEvolution
from HillClimbing import HillClimbing


def get_input():
    inputted = input("-> ")
    if inputted.isdigit():
        return int(inputted)
    else:
        return -1


def get_city_string(city):
    if city == 1:
        return "docs/city_plans/city_plan_1"
    if city == 2:
        return "docs/city_plans/small_map"
    if city == 3:
        return "docs/city_plans/big"
    if city == 4:
        path = input("File Name: ")
        path = path.split()[0].split('.')[0]
        try:
            f = open("docs/city_plans/"+path+".txt",'r')
            f.close()
            return "docs/city_plans/"+path
        except FileNotFoundError:
            print("Could not find file '"+path+"' on city_plans directory")
            return -1
    else:
        return -1


def cli():
    print("\nTraffic Signaling Optimization Problem CLI")

    while True:
        print("Choose the city plan: ")
        print("0: Exit")
        print("1: Basic City")
        print("2: Small City")
        print("3: Big City")
        print("4: Custom (enter a file name)")

        city = get_input()

        if city == 0:
            break
        city_string = get_city_string(city)
        if city_string == -1:
            print("You have chosen an invalid city!\nPlease try again")
            continue

        city_plan_data = parse_input_file(city_string+".txt")
        try:
            city_plan_coords = coord_parser(city_string+".coords")
        except FileNotFoundError:
            city_plan_coords = None
            print("This map does not support animation")

        simulation = Simulation(city_plan_data, "random")

        while True:
            print("Choose the optimization algorithm: ")
            print("0: Go Back")
            print("1: Hill Climbing")
            print("2: Simulated Annealing")
            print("3: Genetic Algorithm")
            algo = get_input()

            if algo == 0:
                break
            elif algo == 1:
                # hill climbing
                hill_climbing = HillClimbing()
                (bestSol, bestScore) = hill_climbing.run(simulation)
                simulation.reset()
                print("End of simulation\n")
                print("With a score of ", bestScore)

            elif algo == 2:
                number_of_coolings = 6

                # simulated annealing
                while True:
                    tn = 1

                    print("Choose the temperature cooling schedule: ")
                    print("0: Go Back")
                    print("1: Exponential multiplicative cooling")
                    print("2: Logarithmic multiplicative cooling")
                    print("3: Linear multiplicative cooling")
                    print("4: Quadratic multiplicative cooling")
                    print("5: Linear additive cooling")
                    print("6: Quadratic additive cooling")
                    cooling = get_input()

                    if cooling == 0:
                        break

                    print("Choose the initial temperature: ")
                    t0 = get_input()

                    print("Choose the number of the algorithm iterations: ")
                    iterations = get_input()

                    if cooling > 4:
                        print("Choose the final temperature: ")
                        tn = get_input()

                    if 0 > cooling > number_of_coolings or iterations <= 0 or t0 <= 0 or tn < 0:
                        print("You have chosen invalid options!\nPlease try again")
                        continue

                    print("Do you want to apply Non-Monotonic Adaptive Cooling to the previous schedule (y/n): ")
                    apply_non_mono = input() in "yY"

                    sim_annealing = SimulatedAnnealing(simulation)
                    best_state, best_score = sim_annealing.run(iterations, t0, cooling, tn, apply_non_mono)

                    print("Best State: ", end="")
                    simulation.print_state(best_state)
                    print("\nBest State Score: ", best_score)
                    break

            elif algo == 3:
                # genetic algorithm
                while True:
                    print("Choose the population size: ")
                    population_size = get_input()

                    print("Choose the number of generations: ")
                    number_of_generations = get_input()

                    print("Choose the radiation dosage: ")
                    radiation_dosage = get_input()

                    if 0 > radiation_dosage > 1 or population_size <= 0 or number_of_generations <= 0:
                        continue

                    ev = GloriousEvolution(city_plan_data, radiation_dosage, population_size, number_of_generations)
                    best = ev.run()
                    if city_plan_coords is None:
                        break
                    ans = ""
                    while True:
                        print("Do you wish to watch the animation for the best schedule found? (y/n)")
                        ans = input()
                        if(ans in "ynYN"):
                            break
                        print("Invalid Input")
                    if ans in "yY":
                        sim = Simulation(city_plan_data, "array", best)
                        sim.run_animated(city_plan_coords)
                            
                    break
            else:
                print("You have chosen an invalid algorithm!\nPlease try again")
                continue
