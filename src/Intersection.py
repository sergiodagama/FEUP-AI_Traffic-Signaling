import Trafficlight

class Intersection:

    def __init__(self, id):
        # self.streets = []
        self.id = id
        self.traffic_lights = []
        self.current_light = 0
        self.num_of_lights = 0
    
    def __str__(self):
        output = ""
        output += str(self.id)
        output += ("\n")
        for i in self.traffic_lights:
            output += str(i)
            output += ("\n")
        return output

    def insert_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)
        self.num_of_lights += 1

    def has_street(self,street):
        return next((True for x in self.traffic_lights if x.street == street), False)

    def run(self):
        while self.traffic_lights[self.current_light].current_time == 0:
            self.current_light +=1
            self.current_light %= self.num_of_lights
            self.traffic_lights[self.current_light].update_time()
        self.traffic_lights[self.current_light].current_time -= 1
        return self.traffic_lights[self.current_light].remove_car()

    def draw(self):
        print("Intersection ID: " + str(self.id), end="")
        print("Current traffic light: " + str(self.traffic_lights[self.current_light].street.street_name))