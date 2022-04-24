import random
from Simulation import Simulation
import matplotlib.pyplot as plt

class HillClimbing:
    '''
    Class storing a simulation and solving it using hill climbing and some variations
    '''

    def __init__(self, sim: Simulation):
        self.simulation = sim

    def changeTrafficlightDuration(self, trafficLights: list):
        '''
        Chooses a random Trafficlight and gives it a random duration between 1 and the max simulation time
        '''
        new_trafficLights = []
        for i in trafficLights:
            new_trafficLights.append(i)
        id1 = random.randrange(len(trafficLights))
        random_digit = random.randint(1, self.simulation.duration)
        new_trafficLights[id1].set_time(random_digit)

        return new_trafficLights

    def swapTrafficlight(self, trafficLights: list):
        '''
        Chooses between two Trafficlights and swaps their order in the cycle
        '''
        
        new_trafficLights = []
        for i in trafficLights:
            new_trafficLights.append(i)
        id1 = random.randrange(len(trafficLights))
        id2 = random.randrange(len(trafficLights))

        while id1 == id2:
            id2 = random.randrange(len(trafficLights))

        new_trafficLights[id1], new_trafficLights[id2] = new_trafficLights[id2], new_trafficLights[id1]
        return new_trafficLights
    
    def generateNeighbour(self, currSol: list, index: int):
        '''
        Generates one neighbour currosponding to the 'index'th operation
        '''
        newSol = []
        for i in currSol:
            newSol.append(i)

        id1 = random.randrange(len(currSol))

        if index == 0:  # randomly generate traffic light duration
            newSol[id1].set_traffic_lights(self.changeTrafficlightDuration(currSol[id1].get_traffic_lights()))

        elif index == 1:  # randomly swaps two traffic lights in the cycle
            while len(currSol[id1].get_traffic_lights()) < 2:
                id1 = random.randrange(len(currSol))
            newSol[id1].set_traffic_lights(self.swapTrafficlight(currSol[id1].get_traffic_lights()))
        
        return newSol

    def neighbours(self, currSol: list):
        '''
        Generates all possible solutions for a solution
        '''
        neighboursList = []
        nFunctions = 2
        for i in range(nFunctions):
            neighboursList.append(self.generateNeighbour(currSol,i))
        return neighboursList

    def run_steepest_ascent(self,iterations):
        '''
        Hill-climbing steepest ascent optimization technique
        '''

        currSol = self.simulation.output_state()
        self.simulation.run()
        currScore = self.simulation.score
        print("Initial Solution with a score of", currScore)
        print("Let the simulation begin")
        it = 0
        evaluation = []
        while it < iterations:
            evaluation.append(currScore)
            it += 1
            neighboursList = self.neighbours(currSol)
            for neighbour in neighboursList:
                self.simulation.set_state(neighbour)
                self.simulation.run()
                neighbourScore = self.simulation.score
                if neighbourScore > currScore:
                    currSol = self.simulation.output_state()
                    currScore = neighbourScore
                    it = 0
                print("Current best solution : ", currScore ," ", round(100 * (it / iterations),2)," %", end='\r')
        '''generating a plot'''
        plt.xlabel('Iteration')
        plt.ylabel('Evaluation')
        print(len(evaluation))
        plt.plot(range(len(evaluation)),evaluation)
        plt.show()
        return (currSol, currScore)

    def run(self, iterations):
        '''
        Hill-climbing optimization technique
        '''

        currSol = self.simulation.output_state()
        self.simulation.run()
        currScore = self.simulation.score
        print("Initial Solution with a score of", currScore)
        print("Let the simulation begin")
        it = 0
        evaluation = []
        while it < iterations:
            evaluation.append(currScore)
            neighbour = self.generateNeighbour(currSol,random.randint(0,1))
            it += 1
            self.simulation.set_state(neighbour)
            self.simulation.run()
            neighbourScore = self.simulation.score
            if neighbourScore > currScore:
                currSol = self.simulation.output_state()
                currScore = neighbourScore
                it = 0
            print("Current best solution : ", currScore ," ", round(100 * (it / iterations),2)," %", end='\r')
        '''generating a plot'''
        plt.xlabel('Iteration')
        plt.ylabel('Evaluation')
        plt.plot(range(len(evaluation)),evaluation)
        plt.show()
        return (currSol, currScore)
