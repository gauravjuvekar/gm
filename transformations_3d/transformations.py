#!/usr/bin/env python3
"""
Plots a line using Bresenham's algorithm (integer arithmetic only)
"""
import pygame
import argparse
import math
from collections import namedtuple
import time
import math

# A simple point class
Point = namedtuple('Point', ['x', 'y', 'z'])
Vector = namedtuple('Vector', ['x', 'y', 'z'])

class UnitVector(object):
    def __init__(self, x, y, z):
        det = math.sqrt(x**2 + y**2 + z**2)
        self.x = x / det
        self.y = y / det
        self.z = z / det

def sign(number):
    """
    Returns signum(`number`)
        -1 if `number` < 0,
        +1 if `number` > 0,
        0 if `number` == 0)
    """
    return int(math.copysign(1, number))


def plot(point, color=(255, 255, 255)):
    """
    Plot a colored pixel at (`x`, `y`)
    `color` is specified as (R, G, B) with each value ranging till 255
    """
    surface.set_at((point.x, point.y), color)

def irange(start, end, abs_delta=1):
    """
    Returns an inclusive range() generator in steps of `abs_delta`
    """
    diff = end - start
    return range(start, end + sign(diff), sign(diff) * abs_delta)

def translate(points, shift_x, shift_y, shift_z):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(point.x + shift_x, point.y + shift_y, point.z + shift_z)

def scale(points, scale_x, scale_y, scale_z):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(point.x * scale_x, point.y * scale_y, point.z * scale_z)

def rotate(points, angle, axis):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    l = axis.x
    m = axis.y
    n = axis.z
    matrix = [[l*l*(1-math.cos(angle)) + 1*math.cos(angle),
               m*l*(1-math.cos(angle)) - n*math.sin(angle),
               n*l*(1-math.cos(angle)) + m*math.sin(angle)],
              [l*m*(1-math.cos(angle)) + n*math.sin(angle),
               m*m*(1-math.cos(angle)) + 1*math.cos(angle),
               n*m*(1-math.cos(angle)) - l*math.sin(angle)],
              [l*n*(1-math.cos(angle)) - m*math.sin(angle),
               m*n*(1-math.cos(angle)) + l*math.cos(angle),
               n*n*(1-math.cos(angle)) + 1*math.sin(angle)]]
    for point in iter_points:
        yield Point((matrix[0][0] * point.x +
                     matrix[0][1] * point.y +
                     matrix[0][2] * point.z),
                    (matrix[1][0] * point.x +
                     matrix[1][1] * point.y +
                     matrix[1][2] * point.z),
                    (matrix[2][0] * point.x +
                     matrix[2][1] * point.y +
                     matrix[2][2] * point.z))

def intify(points):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(int(round(point.x)), int(round(point.y)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("VECTOR_X",
                        type=int,
                        help="X dimension of axis of rotation")
    parser.add_argument("VECTOR_Y",
                        type=int,
                        help="Y dimension of axis of rotation")
    parser.add_argument("VECTOR_Z",
                        type=int,
                        help="Z dimension of axis of rotation")
    parser.add_argument("ANGLE",
                        type=int,
                        help="Angle to rotate in degrees")
    parser.add_argument("--window-size", "-w",
                        type=int,
                        default=500,
                        help="Window size in pixels (equal width an height)")
    args = parser.parse_args()

    # Init display
    pygame.display.init()
    screen = pygame.display.set_mode((args.window_size, args.window_size))
    surface = pygame.display.get_surface()

    def rt(angle, vector):
        faces = []
        face = [Point(*_) for _ in (
            (0, 0, 0), (0, 100, 0), (0, 100, 100), (0, 0, 100),)]
        faces.append(face)
        faces.append(list(translate(face, 100, 0, 0)))

        face = [Point(*_) for _ in (
            (0, 0, 0), (100, 0, 0), (100, 100, 0), (0, 100, 0),)]
        faces.append(face)
        faces.append(list(translate(face, 0, 0, 100)))

        face = [Point(*_) for _ in (
            (0, 0, 0), (0, 0, 100), (100, 0, 100), (0, 0, 100),)]
        faces.append(list(translate(face, 0, 100, 0)))
        faces = [list(translate(face, -50, -50, -50)) for face in faces]

        faces = [rotate(points,
                        math.radians(angle),
                        vector, )
                 for points in faces]
        faces = [list(translate(face, 200, 200, 0)) for face in faces]
        faces = [[(_.x, _.y) for _ in face] for face in faces]

        for face in faces:
            pygame.draw.polygon(surface, (255, 255, 255), face, 1)
        pygame.display.update()
    vector = UnitVector(args.VECTOR_X, args.VECTOR_Y, args.VECTOR_Z)
    for angle in range(360 + 1):
        rt(angle, vector)
        time.sleep(0.01)
        surface.fill((0,0,0))
    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass
