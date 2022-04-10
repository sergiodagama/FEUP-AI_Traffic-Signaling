import sys 
from Simulation import Simulation
from GloriousEvolution import GloriousEvolution


def main():
    # sim = Simulation("docs/city_plans/city_plan_1.txt","path", "docs/schedules/schedule1.txt") 
    # sim = Simulation("docs/city_plans/city_plan_1.txt","random") 
    # sim.run()
    # sim.output_state_file("docs/schedules/result.txt", 'w')
    # print("The Simulation score is: " + str(sim.score))

    ev = GloriousEvolution("docs/city_plans/city_plan_1.txt", 100)
    ev.run_current()






if __name__ == '__main__':
    sys.exit(main())