from turtle import Screen, Turtle
import turtle
from Car import Car
from Street import Street

class Animation:
    def __init__(self, coords):
        self.nodes,self.streets = coords
        self.screen = Screen()
        self.screen.setworldcoordinates(-20,-20,1020,1020)
        self.screen.bgcolor("#D0D0D0")
        self.screen.tracer(0, 0)
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.turtle.color("#0000FF")
        self.turtle.hideturtle()
        self.turtle.shape('turtle')
    
    def draw_map(self):
        rootwindow = self.screen.getcanvas().winfo_toplevel()
        rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
        rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
        for street in self.streets:
            node_from = self.nodes[street[0]]
            node_to = self.nodes[street[1]]
            x = node_to[0]-node_from[0]
            y = node_to[1]-node_from[1]
            x -= x/2
            y -= y/2
            self.turtle.up()
            self.turtle.setpos(node_from[0],node_from[1])
            self.turtle.down()
            self.turtle.seth(self.turtle.towards(node_to[0],node_to[1]))
            self.turtle.setpos(node_from[0]+x,node_from[1]+y)
            self.turtle.left(150)
            self.turtle.forward(15)
            self.turtle.left(120)
            self.turtle.forward(15)
            self.turtle.left(120)
            self.turtle.forward(15)
            self.turtle.setpos(node_to[0],node_to[1])

        for node in self.nodes:
            self.turtle.up()
            self.turtle.setpos(node[0],node[1])
            self.turtle.dot(7,"#F00000")
    
    def update(self):
        self.screen.update()

    def draw_car(self, car):
        street = car.current_road()
        begin = street.start_intersection
        end = street.end_intersection
        dirX = (self.nodes[begin][0] - self.nodes[end][0])/street.time_cost
        dirY = (self.nodes[begin][1] - self.nodes[end][1])/street.time_cost
        posX = self.nodes[end][0] + (dirX * car.remaining_cost)
        posY = self.nodes[end][1] + (dirY * car.remaining_cost)
        self.turtle.up()
        self.turtle.setpos(posX, posY)
        self.turtle.seth(self.turtle.towards(self.nodes[end][0],self.nodes[end][1]))
        turtle.colormode(255)
        self.turtle.color(car.color[0],car.color[1],car.color[2])
        self.turtle.stamp()

    def clear_cars(self):
        self.turtle.clearstamps()

