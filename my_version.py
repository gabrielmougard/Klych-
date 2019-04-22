import turtle


myPen = turtle.Turtle()
# myPen.ht()
myPen.speed(4000000)
myPen.pencolor('blue')
size = 50

# first points
base_points = [[-size, +size],
               [+size, +size],
               [+size, -size],
               [-size, -size]]


def make_square_from_center(center: tuple, size: int):
    h = size / 2
    return (
        (center[0]-h, center[1]+h),
        (center[0]+h, center[1]+h),
        (center[0]+h, center[1]-h),
        (center[0]-h, center[1]-h)
    )


polygon_type = make_square_from_center

# rule prototype :
# center, size

rules = (
    lambda center, size: (center[0] + size, center[1]),
    lambda center, size: (center[0], center[1] + size),
    lambda center, size: (center[0] - size, center[1]),
    lambda center, size: (center[0], center[1] - size),
    lambda center, size: (center[0] + size, center[1] + size),
    lambda center, size: (center[0] - size, center[1] - size),
    lambda center, size: (center[0] + size, center[1] - size),
    lambda center, size: (center[0] - size, center[1] + size),
)


def make_polygon(center: tuple, size: int, rule):
    return rule(center, size)


def draw_polygon(vertexes:list):
    myPen.up()
    myPen.goto(vertexes[0][0], vertexes[0][1])
    myPen.down()
    for vertex in vertexes:
        myPen.goto(vertex[0], vertex[1])
    myPen.goto(vertexes[0][0], vertexes[0][1])


def current_size(points: int):
    return abs(points[0][0] - points[1][0])


def give_center(points: list):
    return ((points[0][0] + points[2][0]) / 2,
            (points[0][1] + points[2][1]) / 2)


def _next_centers(points: list):
    center = give_center(points)
    size = current_size(points)
    for rule in rules:
        yield rule(center, size)


def _next_points(points: list):
    next_size = _next_size(points)
    for center in _next_centers(points):
        yield make_polygon(center, next_size, polygon_type)


def _next_size(points: list):
    return current_size(points) / 3


def next_frame(square: list, depth: int):
    if depth > 0:
        for square in _next_points(square):
            draw_polygon(square)
            next_frame(square, depth - 1)


def fractal(points: list, depth: int):
    # init base square
    draw_polygon(points)
    # gives the first 4 squares for now
    first_squares = _next_points(points)
    for square in first_squares:
        draw_polygon(square)
        next_frame(square, depth)

fractal(base_points, 3)
turtle.done()