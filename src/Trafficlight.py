import queue
import copy


class TrafficLight:
    def __init__(self, street, time):
        self.my_queue = queue.Queue()
        self.time = time
        self.street = street
        self.current_time = time
        # self.green_light = False

    def __str__(self):
        return str(self.street.street_name) + " " + str(self.time)

    def replicate(self):
        return TrafficLight(self.street, self.time)
    def add_car(self, car):
        self.my_queue.put(car)

    def remove_car(self):
        try:
            return self.my_queue.get(False)
        except queue.Empty as e:
            return None


    # def swap_light(self):
    #     self.green_light = not self.green_light

    # def update(self):                   # this should probably be hadled by the Intersection for simplicity sake, and it's probably easier to debug
    #     if not self.green_light:
    #         return
    #     self.current_time -= 1

    #     # greenlight time is out now
    #     if self.current_time == 0:
    #         self.swap_light()
    #         self.current_time = self.time

    def update_time(self):
        self.current_time = self.time
