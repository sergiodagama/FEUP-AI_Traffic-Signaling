import sys 
# from copy import deepcopy
from Parser import parse_input_file
from Simulation import Simulation
from GloriousEvolution import GloriousEvolution


def main():

    city_plan_data = parse_input_file("docs/city_plans/city_plan_1.txt")
    # city_plan_data = parse_input_file("docs/city_plans/b_by_the_ocean.txt")
    # sim = Simulation(city_plan_data,"path", "docs/schedules/b_by_the_ocean.txt")
    # sim = Simulation(city_plan_data, "random")




    # new_state = sim.output_state()
    # new_state[0],new_state[1] = new_state[1],new_state[0]
    # new_state[0].traffic_lights[0].time = 1
    # sim.set_state(new_state)
    # sim.reset()

    # sim.run()
    # print("sim2 score: " + str(sim.score))
    # sim.output_state_file("docs/schedules/result2.txt", 'w')


    # new_state = sim.output_state()
    # # new_state[0],new_state[1] = new_state[1],new_state[0]
    # new_state[0].traffic_lights[0].time = 1
    # sim.set_state(new_state)
    # sim.reset()

    # sim.run()
    # print("sim2 score: " + str(sim.score))
    # sim.output_state_file("docs/schedules/result2.txt", 'w')



    ev = GloriousEvolution(city_plan_data,0.2,10,100)
    ev.run()






if __name__ == '__main__':
    sys.exit(main())
