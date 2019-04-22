import turtle
import copy


myPen = turtle.Turtle()
# myPen.ht()
myPen.speed(5)
myPen.pencolor('blue')

# first points
points = [[-175, +175],
          [-175, -175],
          [+175, -175],
          [+175, +175]]  

def draw_polygon(vertexes):
    myPen.up()
    myPen.goto(vertexes[0][0], vertexes[0][1])
    myPen.down()
    for vertex in vertexes :
        myPen.goto(vertex[0], vertex[1])
    myPen.goto(vertexes[0][0], vertexes[0][1])

def _init(points):
    draw_polygon(points)


def _next_points(points):
    return 1


def fractal(points, depth):
    _init(points)
    i = depth
    while i > 0 :
        points = _next_points(points)
        draw_polygon(points)






fractal(points, 2)
turtle.done()
