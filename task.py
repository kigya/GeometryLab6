import math
import random
from matplotlib import pyplot as plt
from celluloid import Camera
from Point import Point
from Vector import Vector


fig = plt.figure()
camera = Camera(fig)


def init_points():
    points = []
    xs = [random.randint(0, 10) for _ in range(15)]
    ys = [random.randint(0, 10) for _ in range(15)]
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points


def draw_point(point: Point):
    plt.scatter(point.x, point.y, color='black')


def draw_points(points: list):
    for i in range(len(points)):
        draw_point(points[i])


def init_vectors_of_moving(points: list):
    vectors = []
    xs = [random.randint(-1, 1) for _ in range(len(points))]
    ys = [random.randint(-1, 1) for _ in range(len(points))]
    for i in range(len(xs)):
        p = Point(xs[i], ys[i])
        while p.x == 0 and p.y == 0:
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
        vectors.append(p)
    return vectors


def det(a, b, c, d):
    return a * d - b * c


def get_point_position_to_line(p0: Point, p1: Point, p2: Point):
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return "left"
    elif d < 0:
        return "right"
    else:
        return "on the line"


def find_point_with_min_x(points: list):
    min_point = points[0]
    for i in range(1, len(points)):
        if min_point.x > points[i].x:
            min_point = points[i]
    return min_point


def find_point_with_max_x(points: list):
    max_point = points[0]
    for i in range(1, len(points)):
        if max_point.x < points[i].x:
            max_point = points[i]
    return max_point


def find_lefter_points(points: list, p1: Point, p2: Point):
    lefter_points = []
    for i in range(len(points)):
        if get_point_position_to_line(points[i], p1, p2) == "left":
            lefter_points.append(points[i])
    return lefter_points


def find_righter_points(points: list, p1: Point, p2: Point):
    righter_points = []
    for i in range(len(points)):
        if get_point_position_to_line(points[i], p1, p2) == "right":
            righter_points.append(points[i])
    return righter_points


def vector_product(p0: Point, p1: Point, p2: Point):
    return math.fabs(det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y))


def quick_hull(pL: Point, pR: Point, points: list, convex_hull_points: list):
    max_area_triangle = vector_product(pL, pR, points[0])
    s = points[0]
    for i in range(1, len(points)):
        # находим наиболее удаленную точку s
        if vector_product(pL, pR, points[i]) > max_area_triangle:
            max_area_triangle = vector_product(pL, pR, points[i])
            s = points[i]
            #print("s ", s.x, ":", s.y, " l ", pL.x, ":", pL.y, " r ", pR.x, ":", pR.y)
    # теперь для каждой из сторон pls и spr находим точки левее
    pls = find_lefter_points(points, pL, s)
    spr = find_lefter_points(points, s, pR)
    # и если множество точек левее pls не пусто то повторяем quick hull и тд
    if pls:
        quick_hull(pL, s, pls, convex_hull_points)
        convex_hull_points.append(s)
    else:
        convex_hull_points.append(s)
    # и если множество точек левее spr не пусто то повторяем quick hull и тд
    if spr:
        quick_hull(s, pR, spr, convex_hull_points)
        
    for point in convex_hull_points:
        print("x: ", point.x, " y: ", point.y)


def complete_convex_hull(points: list):
    pl = find_point_with_min_x(points)
    pr = find_point_with_max_x(points)
    convex_hull_points = []

    lefter_points = find_lefter_points(points, pl, pr)
    righter_points = find_righter_points(points, pl, pr)

    convex_hull_points.append(pl)
    quick_hull(pl, pr, lefter_points, convex_hull_points)
    convex_hull_points.append(pr)
    quick_hull(pr, pl, righter_points, convex_hull_points)

    convex_hull_points.append(convex_hull_points[0])
    return convex_hull_points


def draw_convex_hull(convex_hull_points: list, color: str):
    for i in range(len(convex_hull_points) - 1):
        plt.plot([convex_hull_points[i].x, convex_hull_points[i + 1].x],
                 [convex_hull_points[i].y, convex_hull_points[i + 1].y], color=color)


def perimeter(points: list):
    hull_perimeter = 0
    for i in range(len(points) - 1):
        hull_perimeter += Vector(points[i], points[i + 1]).get_length()
    hull_perimeter += Vector(points[len(points) - 1], points[0]).get_length()
    return hull_perimeter


def move(moving_points: list, vectors: list):
    for i in range(len(moving_points)):
        moving_points[i] = moving_points[i] + vectors[i]


def opposite_vectors_of_moving(vectors: list):
    for i in range(len(vectors)):
        vectors[i] = Point(-vectors[i].x, -vectors[i].y)
    return vectors


def init_motion(points: list):
    vectors = init_vectors_of_moving(points)
    PERIMETER_LIMIT = 100

    i = 0
    while i < 70:
        convex_hull_points = complete_convex_hull(points)

        draw_points(points)
        draw_convex_hull(convex_hull_points, "blue")
        camera.snap()

        if perimeter(convex_hull_points) >= PERIMETER_LIMIT:
            vectors = opposite_vectors_of_moving(vectors)

        # for i in range(len(points)):
        #     for j in range(len(convex_hull_points)):
        #         if points[i]==convex_hull_points[j] and perimeter(convex_hull_points) >= PERIMETER_LIMIT:
        #             points[i] = points[i] + opposite_vectors_of_moving(vectors)[i];
        #         else:
        #             points[i] = points[i] + vectors[i];
        move(points, vectors)
        i += 1


def init():
    points = init_points()
    init_motion(points)
    plt.grid(True)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()


init()
