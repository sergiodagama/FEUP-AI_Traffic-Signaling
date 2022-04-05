class Car:
    def __init__(self, path_length, path):
        self.path_length = path_length
        self.path = path
        self.current_street = 0
        self.remaining_cost = 1


    def enter_next_street(self):
        self.current_street += 1
        print("\tcurrent street value: "+ str(self.current_street) + " for " + str(self.path_length))
        self.remaining_cost = self.path[self.current_street].time_cost

    def current_road(self):
        return self.path[self.current_street]

    def drive(self):
        self.remaining_cost -= 1
        if self.remaining_cost <= 0:
            if self.current_street+1 == self.path_length:
                return 2
            elif self.remaining_cost == 0:
                return 1
        else:
            return 0

    def draw(self):
        for i in range(self.path_length):
            print(self.path[i].street_name,  end=" ")
        print("\nCurrently on :", end="")
        print(self.path[self.current_street].street_name)
        print("Remaining Cost: ", end="")
        print(self.remaining_cost)
        print("Path_length: ", end="")
        print(self.path_length)
        print("")