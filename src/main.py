duration = 0  # simulation duration (D)
n_intersections = 0  # number of intersections (I)
n_streets = 0  # number of streets (S)
n_cars = 0  # number of cars
bonus = 0  # bonus points for each car that reaches destination

streets = []  # parsed streets
cars = []  # parsed cars

class Street:
    def __init__(self, start_intersection, end_intersection, street_name, time_cost):
        self.start_intersection = start_intersection
        self.end_intersection = end_intersection
        self.street_name = street_name
        self.time_cost = time_cost


class Car:
    def __init__(self, path_length, path):
        self.path_length = path_length
        self.path = path


# parses the first line
# of the input file
def parse_first_line(line):
    splitted = line.split()

    duration = splitted[0]
    n_intersections = splitted[1]
    n_streets = splitted[2]
    n_cars = splitted[3]
    bonus = splitted[4]

# parses one line of the input file
# relative to the streets
def parse_street_line(line):
    splitted = line.split()

    street = Street()

    street.append(splitted)

# parses one line of the input file
# relative to the cars paths
def parse_car_line(line):
    split_list = line.split()
    num = split_list.pop(0)
    cars.append(Car(num,split_list))


# parses all the input file
def parse_input_file(path):
    file = open (path, 'r')
    lines = file.readline()
    parse_first_line(lines.pop(0))
    for i in range(0,n_streets):
        parse_street_line(lines.pop(i))
    for line in lines:
        parse_car_line(line)

