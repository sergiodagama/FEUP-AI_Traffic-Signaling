import Parser
import Intersection
import random


# attributes are "duration", "n_intersections", "n_streets", "n_cars", "bonus"
class Simulation:
    def __init__(self, input_path, intersection_path=0):
        self.attributes, self.streets, self.cars = Parser.parse_input_file(input_path)
        self.current_time = 0
        self.intersections = self.calculate_intersections(intersection_path)

    def convert_state(self, state):
        # TODO: converts a state into data to be used in the simulation

    def run(self):
        for i in range(0, self.attributes["duration"]):
            for car in self.cars:
                # TODO
            for intersection in self.intersections:
                # TODO

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
            for street in car.path:
                id = street.end_intersection
                if not next((x for x in intersections if x.id == id), False):
                    new_intersection = Intersection(id)
                    new_intersection.insert_traffic_light(street, random(0, self.attributes["duration"]))
                    intersections.append(new_intersection)

    def create_state(self, path):
        switch()

    def create_intersections(state):


    def score_evaluation(self):
        car_traverse_time =  self.attributes["duration"] - self.current_time

        if self.current_time <= self.attributes["duration"]:
            score = self.attributes["bonus"] + car_traverse_time
        else:
            score = 0

        return score








