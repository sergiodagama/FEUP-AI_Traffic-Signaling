class Car:
    def __init__(self, path_length, path):
        self.path_length = path_length
        self.path = path
        self.current_street = 0
        self.remaining_cost = 0


    def enter_next_street(self):
        self.current_street += 1
        self.remaining_cost = self.path[self.current_street].time_cost

    def current_street(self):
        return self.path[self.current_street]

    def drive(self):
        if self.remaining_cost > 0:
            self.remaining_cost -= 1
            return 0
        elif self.current_street +1 == self.path_length:
            return 2
        return 1