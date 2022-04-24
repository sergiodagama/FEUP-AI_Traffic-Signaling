import queue


class TrafficLight:
    def __init__(self, street, time):
        self.cars_queue = queue.Queue()
        self.time = time
        self.street = street
        self.current_time = time

    def __str__(self):
        return str(self.street.street_name) + " " + str(self.time)

    def replicate(self):
        return TrafficLight(self.street, self.time)

    def add_car(self, car):
        self.cars_queue.put(car)

    def remove_car(self):
        try:
            return self.cars_queue.get(False)
        except queue.Empty as e:
            return None

    def set_time(self, time):
        self.time = time

    def update_time(self):
        self.current_time = self.time
