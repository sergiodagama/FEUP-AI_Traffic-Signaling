class Car:
    def __init__(self, path_length, path):
        self.path_length = path_length
        self.path = path
        self.current_street = 0
        self.remaining_cost = 0


    def enter_next_street(self):
        self.current_street += 1
        if self.current_street == self.path_length:
            return True
        self.remaining_cost = self.path_length[self.current_street].time_cost
