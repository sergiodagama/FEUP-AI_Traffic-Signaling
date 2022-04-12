from copy import deepcopy
from Parser import parse_state_file
from Intersection import *
from Trafficlight import TrafficLight
import random


# attributes are "duration", "n_intersections", "n_streets", "n_cars", "bonus"
class Simulation:
    def __init__(self, city_plan_data,state_mode, intersection_path=0,debug=False):
        self.attributes = city_plan_data[0]
        self.streets = city_plan_data[1]
        self.cars = deepcopy(city_plan_data[2])
        self.duration = int(self.attributes["duration"])
        self.bonus = int(self.attributes["bonus"])
        self.score = 0
        self.reproductive_probability = 0 #value from 0 to 1, for use in GloriousEvolution
        self.debug = debug
        self.intersections = self.create_state(state_mode, self.streets, intersection_path)
        self.streets_to_lights = {}
        self.init_traffic_lights()

    def convert_state(self, state):
        # TODO: converts a state into data to be used in the simulation
        return 0

    def run(self):
        for time in range(0, self.duration+1):
            for car in self.cars:       # cars decrease remaining cost, if it reaches 0 they queue on TrafficLight
                car_position = car.drive()
                if(car_position == 1):     # car did not reach end of the road
                    light = self.streets_to_lights[car.current_road().street_name] # next((traffic_light for inter in self.intersections for traffic_light in inter.traffic_lights if traffic_light.street==car.current_road()),None)
                    light.add_car(car)
                    # print("\tAdding element to street: " + str(car.current_road().street_name))
                elif(car_position == 2):    #car reached end, add to score
                    self.score_evaluation(time)
                    # self.cars.remove(car)
            for intersection in self.intersections:     #first update which traffic light is on, then dequeue one form the green light
                car = intersection.run()
                # print("Running intersection: "+ str(intersection.id))
                if car is not None:
                    car.enter_next_street()
            self.draw()

    # pre: fill traffic lights with cars
    # pre: fill intersections with traffic lights

    # MAIN SIMULATION (done for each state given by convert_state)
    #
    # loop time:
    #   loop cars:
    #       if green light and in queue:
    #           if first in queue, go to next street
    #           if not first in queue, do nothing
    #          if in queue and red light, do nothing
    #       if red light and in queue:
    #           always do nothing
    #       if in street (not in queue):
    #           advance in the street
    #
    #       if at end of street:
    #           if car at end of path:
    #               calculate score
    #           if car not at end of path:
    #               add car to traffic light queue
    #
    #    loop traffic lights:
    #       if green:
    #           sub 1 unit time to current traffic light
    #       if the green traffic light time is 0:
    #           change this traffic light to red
    #           change next intersection traffic light to green
    #


    #
    #   create_state():
    #       switch for different types of heuristics
    #       returns a new state
    #
    #   create_intersections(state):
    #       create traffic lights and intersections based on the state given
    #


    #
    #   loop n_simulations:
    #       state = create_state()
    #
    #       create_intersections(state)
    #
    #       run()

    def create_random_state(self):
        intersections = []
        for car in self.cars:
            for i in range(car.path_length-1):
                street = car.path[i]
                id = street.end_intersection
                old_intersection = next((x for x in intersections if x.id == id), None)
                if old_intersection is None:
                    new_intersection = Intersection(id)
                    new_intersection.insert_traffic_light(TrafficLight(street, random.randint(1, self.duration)))
                    intersections.append(new_intersection)
                elif not old_intersection.has_street(street):
                    old_intersection.insert_traffic_light(TrafficLight(street, random.randint(1, self.duration)))
        return intersections


    def create_state_from_path(self,path, streets):
        return parse_state_file(path, streets)


    def create_state(self, mode, streets, path=0):
        if mode == "random":
            return self.create_random_state()
        if mode == "path":
            return self.create_state_from_path(path,streets)
        if mode == "array":
            return path

    def output_state_file(self, output_file_path, mode):
        file = open(output_file_path, mode)
        file.write(str(len(self.intersections)))
        file.write("\n")
        for intersection in self.intersections:
            file.write(str(intersection.id))
            file.write("\n")
            file.write(str(len(intersection.traffic_lights)))
            file.write("\n")
            for traffic_light in intersection.traffic_lights:
                file.write(traffic_light.street.street_name + " " + str(traffic_light.time))
                file.write("\n")
        file.close()

    def output_state(self):
        return self.intersections


    def score_evaluation(self, time):
        self.score += self.bonus + self.duration - time



    def draw(self):
        if(self.debug):
            for car in self.cars:
                car.draw()
            for inter in self.intersections:
                inter.draw()
            print("Press to Continue")
            input()

    def init_traffic_lights(self):
        for intersection in self.intersections:
            for light in intersection.traffic_lights:
                self.streets_to_lights[light.street.street_name] = light

    def reset(self):
        self.score = 0
        self.reproductive_probability = 0
        
        self.init_traffic_lights()
        for inter in self.intersections:
            inter.reset()
        for car in self.cars:
            car.reset()
        
    def set_state(self,state):
        self.intersections = state