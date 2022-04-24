import math
import sys
from PIL import Image
from random import randint, sample
from turtle import Turtle, Screen
import time


class Node:
    def __init__(self,id_, x, y):
        self.id = id_
        self.posX = x
        self.posY = y
        self.dist_to_neigh = 0
        self.starting_streets = []

    def sq_dist(self,other):
        return pow(self.posX-other.posX,2) + pow(self.posY-other.posY,2)

    def closest(self, list, amount):
        neighbors = []
        for n in list:
            if n is not self:
                n.dist_to_neigh = self.sq_dist(n)
                neighbors.append(n)
        neighbors.sort(key=lambda a: a.dist_to_neigh)
        return neighbors[0:amount]

class Street:
    static_name = 1
    def __init__(self, node_from, node_to, name, cost):
        self.node_from = node_from
        self.node_to = node_to
        self.name = name
        self.cost = cost
    
    def __str__(self) -> str:
        return self.name

class Car:
    def __init__(self, num, streets):
        self.number_of_streets = num
        self.streets = streets

#default:   sim_time=10, num_of_nodes=10, num_of_cars=10, min_dist_sq=100,
#           bonus=1000, max_street_cost=6, min_street_len=3, max_street_len=5, file_name=''):
def main(list_args):
    args = [10, 10, 10, 100, 1000, 6, 3, 5, ""]
    for i,c in enumerate(list_args):
        args[i] = c
    sim_time=int(args[0])
    num_of_nodes=int(args[1])
    num_of_cars=int(args[2])
    min_dist_sq=int(args[3])
    bonus=int(args[4])
    max_street_cost=int(args[5])
    min_street_len=int(args[6])
    max_street_len=int(args[7])
    file_name=args[8]
    
    nodes = []
    streets = []
    cars = []
    for i in range(0,num_of_nodes):
        acceptable = False
        node = None
        while(not acceptable):
            acceptable = True
            node = Node(i,randint(0,1000),randint(0,1000))
            for n in nodes:
                if n.sq_dist(node)<min_dist_sq:
                    acceptable = False
                    break
        nodes.append(node)
    print("Nodes Successfully Generated")
    
    for node in nodes:
        neighboors = node.closest(nodes,randint(2,4))
        for node2 in neighboors:
            street = Street(node2.id,node.id,str(Street.static_name)+"nt_Street", randint(1,max_street_cost))
            go = next((x for x in streets if (x.node_from == street.node_from and x.node_to == street.node_to)),None)
            if go is None:
                Street.static_name += 1
                streets.append(street)
    print("Streets Successfully Generated")
    

    for street in streets:
        node = next((x for x in nodes if x.id == street.node_from),None)
        if node is None: raise Exception("Error, no node compatible with that street")
        if street.name not in node.starting_streets:
            node.starting_streets.append(street.name)


    for index in range(0,num_of_cars):
        acceptable = False
        while(not acceptable):
            acceptable = True
            road_map = []
            current_street = sample(streets, 1)[0]
            road_map.append(current_street)
            for roads in range(1,randint(min_street_len,max_street_len)):
                # print(roads)
                node = next((x for x in nodes if x.id == current_street.node_to),None)
                # print(node.id)
                if node is None:
                    acceptable = False
                    break
                street = [x for x in streets if x.node_from == node.id]
                # print(street)
                if len(street) == 0:
                    acceptable = False
                    break
                current_street = sample(street,1)[0]
                road_map.append(current_street)
        cars.append(Car(len(road_map),road_map))
    print("Cars Successfully Generated")



    print("Generating Graph")
    sc=Screen()
    sc.setworldcoordinates(-20,-20,1020,1020)
    sc.bgcolor("#D0D0D0")
    sc.tracer(0, 0)
    t=Turtle()
    t.speed(0)
    t.color("#0000FF")
    t.hideturtle()
    for street in streets:
        node_from = next((x for x in nodes if x.id == street.node_from),None)
        node_to = next((x for x in nodes if x.id == street.node_to),None)
        x = node_to.posX-node_from.posX
        y = node_to.posY-node_from.posY
        x -= x/2
        y -= y/2
        t.up()
        t.setpos(node_from.posX,node_from.posY)
        t.down()
        t.seth(t.towards(node_to.posX,node_to.posY))
        t.setpos(node_from.posX+x,node_from.posY+y)
        t.left(150)
        t.forward(15)
        t.left(120)
        t.forward(15)
        t.left(120)
        t.forward(15)
        t.setpos(node_to.posX,node_to.posY)

    for node in nodes:
        t.up()
        t.setpos(node.posX,node.posY)
        t.dot(7,"#F00000")
    sc.update()

    input("Press Enter to continue")

    if file_name == "": exit(0)
    file_name = parse(file_name)
    print("Generating file: "+file_name+".txt")
    
    # create city_plan file
    file = open("city_plans/" + file_name + ".txt", 'x')
    file.write(str(sim_time)+" "+str(num_of_nodes)+" "+str(len(streets))+" "+str(num_of_cars)+" "+str(bonus)+"\n")
    for street in streets:
        file.write(str(street.node_from)+" "+str(street.node_to)+" "+str(street.name)+" "+str(street.cost)+"\n")
    for car in cars:
        file.write(str(car.number_of_streets))
        for street in car.streets:
            file.write(" "+ str(street))
        file.write("\n")
    file.close()

    # create city_plan.coords
    file = open("city_plans/" + file_name + ".coords", 'x')
    file.write(str(num_of_nodes) +" "+str(len(streets))+"\n")
    for node in nodes:
        file.write(str(node.posX)+" "+str(node.posY)+"\n")
    for street in streets:
        file.write(str(street.node_from)+" "+str(street.node_to)+"\n")
    file.close()


    # create .eps map
    sc.getcanvas().postscript(file="city_plans_map/" + file_name+".eps",colormode="color")
    time.sleep(1)

    # create .png map from .eps
    img = Image.open("city_plans_map/" + file_name+".eps") 
    img.save("city_plans_map/" + file_name+ ".png", 'png')



def parse(name):
    return name.split()[0].split(".")[0]


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
