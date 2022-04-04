import Trafficlight

class Intersection:
    def __init__(self, id, traffic_lights):
        # self.streets = []
        self.id = id
        self.traffic_lights = traffic_lights

    def __init__(self, id):
        # self.streets = []
        self.id = id
        self.traffic_lights = []

    def insert_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)

    def has_street(self,street):
        next((True for x in self.traffic_lights if x.street == street), False)