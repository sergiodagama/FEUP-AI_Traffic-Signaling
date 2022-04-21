from Parser import parse_input_file
from Simulation import Simulation
from SimulatedAnnealing import SimulatedAnnealing


def get_input():
    inputted = input("-> ")
    if inputted.isdigit():
        return int(inputted)
    else:
        return -1


def get_city_string(city):
    if city == 1:
        return "docs/city_plans/city_plan_1.txt"
    if city == 2:
        return "docs/city_plans/big.txt"
    else:
        return -1


def cli():
    print("\nTraffic Signaling Optimization Problem CLI")

    while True:
        print("Choose the city plan: ")
        print("0: Exit")
        print("1: Basic City")
        print("2: Big City")

        city = get_input()

        if city == 0:
            break
        city_string = get_city_string(city)
        if city_string == -1:
            print("You have chosen an invalid city!\nPlease try again")
            continue

        city_plan_data = parse_input_file(city_string)
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
                # run hill climbing
                pass
            elif algo == 2:
                # simulated annealing
                while True:
                    print("Choose the temperature cooling schedule: ")
                    print("0: Go Back")
                    print("1: Exponential multiplicative cooling")
                    print("2: Logarithmic multiplicative cooling")
                    print("3: Linear multiplicative cooling")
                    print("4: Quadratic multiplicative cooling")

                    cooling = get_input()

                    if cooling == 0:
                        break

                    print("Choose the initial temperature: ")

                    t0 = get_input()

                    print("Choose the number of the algorithm iterations: ")

                    iterations = get_input()

                    if cooling < 0 | iterations < 0 | t0 < 0:
                        print("You have chosen invalid options!\nPlease try again")
                        continue

                    sim_annealing = SimulatedAnnealing(simulation, cooling)
                    sim_annealing.run(iterations, t0, cooling)
                    break

            elif algo == 3:
                # genetic algorithm
                pass
            else:
                print("You have chosen an invalid algorithm!\nPlease try again")
                continue
