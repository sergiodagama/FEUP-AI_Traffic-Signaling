import random
from Simulation import Simulation


class HillClimbing:

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
        return self.swapIntersections(currSol)

    def run(self,simulation : Simulation):
        currSol = list(simulation.output_state())
        simulation.run()
        currScore = simulation.score 
        it = 0

        while it < 1000:
            '''
            rn apenas testamos um neighbour e continuamos, porém tenho que dar refactor nisso
            a lógica da coisa é criar TODOS os neighbours possiveis e depois escolher o 1º que verificar um maior score
            (se steepest ascent, o nome dá hint, escolher o MELHOR neighbour)
    
            '''
            neighbour = self.generateNeighbour(currSol)
            it += 1
            simulation.intersections = neighbour
            simulation.run()
            neighbourScore = simulation.score
            if neighbourScore > currScore:
                currSol = list(simulation.output_state())
                currScore = neighbourScore
                for x in currSol:
                    print(x)
                print("Current Best Solution with a ", currScore, " score")
                it = 0
        return (currSol, currScore)

sim = Simulation("docs/city_plans/city_plan_1.txt","random")
hill_climbing = HillClimbing()
hill_climbing.run(sim)