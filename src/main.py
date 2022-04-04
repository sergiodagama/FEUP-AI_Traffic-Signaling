import sys 
from Simulation import Simulation


def main():
    sim = Simulation("docs/city_plans/city_plan_1","path", "docs/schedules/schedule1") 
    sim.run()
    print(sim.score)
    sim.output_state_file("docs/schedules/result", 'w')





if __name__ == '__main__':
    sys.exit(main())