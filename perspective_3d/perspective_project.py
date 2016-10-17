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
               m*n*(1-math.cos(angle)) + l*math.sin(angle),
               n*n*(1-math.cos(angle)) + 1*math.cos(angle)]]
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

def rotate_faces(faces, angle, axis):
    return (rotate(face, angle, axis) for face in faces)


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
    parser.add_argument("CAM_X",
                        type=int,
                        help="X coordinate of camera")
    parser.add_argument("CAM_Y",
                        type=int,
                        help="Y coordinate of camera")
    parser.add_argument("CAM_Z",
                        type=int,
                        help="Z coordinate of camera")
    parser.add_argument("--screen-z",
                        type=int,
                        help="Z coordinate of screen",
                        default=0)
    parser.add_argument("ANGLE",
                        type=int,
                        help="Angle to rotate in degrees")
    parser.add_argument("--window-size", "-w",
                        type=int,
                        default=500,
                        help="Window size in pixels (equal width an height)")
    args = parser.parse_args()
    cam = Point(args.CAM_X, args.CAM_Y, args.CAM_Z)

    # Init display
    pygame.display.init()
    screen = pygame.display.set_mode((args.window_size, args.window_size))
    surface = pygame.display.get_surface()

    cube = []
    CUBE_SIDE = 200
    face = [Point(*_) for _ in (
        (0, 0, 0),
        (0, CUBE_SIDE, 0),
        (0, CUBE_SIDE, CUBE_SIDE),
        (0, 0, CUBE_SIDE))]
    cube.append(face)
    cube.append(list(translate(face, CUBE_SIDE, 0, 0)))

    face = [Point(*_) for _ in (
        (0, 0, 0),
        (CUBE_SIDE, 0, 0),
        (CUBE_SIDE, CUBE_SIDE, 0),
        (0, CUBE_SIDE, 0))]
    cube.append(face)
    cube.append(list(translate(face, 0, 0, CUBE_SIDE)))

    face = [Point(*_) for _ in (
        (0, 0, 0),
        (0, 0, CUBE_SIDE),
        (CUBE_SIDE, 0, CUBE_SIDE),
        (0, 0, CUBE_SIDE))]
    cube.append(face)
    cube.append(list(translate(face, 0, CUBE_SIDE, 0)))
    cube = [list(translate(
        face,
        -CUBE_SIDE // 2,
        -CUBE_SIDE // 2,
        -CUBE_SIDE // 2)) for face in cube]

    def animate(cube, vector, rotation_range):
        for angle in rotation_range:
            faces = [[point for point in face] for face in rotate_faces(cube, math.radians(angle), vector)]
            yield list(faces)

    def perspective_project(point, cam, screen_z):
        x = cam.x + ((screen_z - cam.z) / (cam.z - point.z)) * (cam.x - point.x)
        y = cam.y + ((screen_z - cam.z) / (cam.z - point.z)) * (cam.y - point.y)
        x = int(round(x))
        y = int(round(y))
        return (x, y)

    vector = UnitVector(args.VECTOR_X, args.VECTOR_Y, args.VECTOR_Z)
    for cube in animate(cube, vector, range(361)):
        cube = [list(translate(
            face,
            args.window_size // 2, args.window_size // 2,
            -CUBE_SIDE // 2)) for face in cube]
        projections = [[perspective_project(point, cam, args.screen_z)
                        for point in face]
                       for face in cube]
        for polygon in projections:
            pygame.draw.polygon(surface, (255, 255, 255), polygon, 1)
        pygame.display.update()
        time.sleep(0.02)
        surface.fill((0,0,0))

    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass
