import random
from Simulation import Simulation
from Parser import parse_input_file

class HillClimbing:

    def __init__(self, sim : Simulation):
        self.simulation = sim

    '''
    change a random traffic light duration
    '''
    def changeTrafficlightDuration(self, trafficLights : list):
        new_trafficLights = []
        for i in trafficLights:
            new_trafficLights.append(i)
        id1 = random.randrange(len(trafficLights))
        random_digit = random.randint(1, self.simulation.duration)
        new_trafficLights[id1].set_time(random_digit)

        return new_trafficLights

    def swapIntersections(self, intersections : list):
        new_intersections = []
        for i in intersections:
            new_intersections.append(i)
        id1 = random.randrange(len(intersections))
        id2 = random.randrange(len(intersections))

        while id1 == id2:
            id2 = random.randrange(len(intersections))

        new_intersections[id1] , new_intersections[id2] = new_intersections[id2] , new_intersections[id1]
        return new_intersections
    
    def generateNeighbour(self,currSol : list):
        newSol = []
        for i in currSol:
            newSol.append(i)
        random_digit = random.randint(0,1)
        id1 = random.randrange(len(currSol)) # escolhemos uma interseção para alterar
        if(random_digit == 0):
            newSol[id1].set_traffic_lights(self.changeTrafficlightDuration(currSol[id1].get_traffic_lights()))
        else:
            while len(currSol[id1].get_traffic_lights()) < 2:
                id1 = random.randrange(len(currSol))
            newSol[id1].set_traffic_lights(self.swapIntersections(currSol[id1].get_traffic_lights()))
        
        return newSol



    def run(self):
        currSol = self.simulation.output_state()
        self.simulation.run()
        currScore = self.simulation.score
        print("Initial Solution with a score of ", currScore)
        for x in currSol:
            print(x)
        print("Let the simulation begin")
        it = 0

        while it < 100:
            '''
            rn apenas testamos um neighbour e continuamos, porém tenho que dar refactor nisso
            a lógica da coisa é criar TODOS os neighbours possiveis e depois escolher o 1º que verificar um maior score
            (se steepest ascent, o nome dá hint, escolher o MELHOR neighbour)
    
            '''
            neighbour = self.generateNeighbour(currSol)
            it += 1
            self.simulation.set_state(neighbour)
            self.simulation.run()
            neighbourScore = self.simulation.score
            if neighbourScore > currScore:
                currSol = self.simulation.output_state()
                currScore = neighbourScore
                it = 0
                print("Found a better solution with a score of ", currScore)
            else:
                print(neighbourScore)
        return (currSol, currScore)
city_plan_data = parse_input_file("docs/city_plans/city_plan_1.txt")
sim = Simulation(city_plan_data,"random")
hill_climbing = HillClimbing(sim)
(bestSol, bestScore) = hill_climbing.run()
print("End of simulation")
print(" ")
print("With a score of ", bestScore)
