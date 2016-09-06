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
Point = namedtuple('Point', ['x', 'y'])

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

def translate(points, shift_x, shift_y):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(point.x + shift_x, point.y + shift_y)

def scale(points, scale_x, scale_y):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(point.x * scale_x, point.y * scale_y)

def rotate(points, angle):
    try:
        iter_points = iter(points)
    except TypeError:
        iter_points = iter((points,))
    for point in iter_points:
        yield Point(math.cos(angle) * point.x - math.sin(angle) * point.y,
                    math.sin(angle) * point.x + math.cos(angle) * point.y)

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
    # parser.add_argument("X_START",
                        # type=int,
                        # help="X coordinate of starting point")
    # parser.add_argument("Y_START",
                        # type=int,
                        # help="Y coordinate of starting point")
    # parser.add_argument("X_END",
                        # type=int,
                        # help="X coordinate of ending point")
    # parser.add_argument("Y_END",
                        # type=int,
                        # help="Y coordinate of ending point")
    parser.add_argument("--window-size", "-w",
                        type=int,
                        default=1000,
                        help="Window size in pixels (equal width an height)")
    args = parser.parse_args()

    # Init display
    pygame.display.init()
    screen = pygame.display.set_mode((args.window_size, args.window_size))
    surface = pygame.display.get_surface()

    points = [Point(*_) for _ in ((100,100), (200,200), (100,300))]

    pygame.draw.polygon(surface, (255, 255, 255), points, 1)
    pygame.draw.polygon(surface, (255, 0, 0),
                        list(scale(points, 3.2, 1.2)), 1)
    pygame.draw.polygon(surface, (0, 255, 0),
                        list(translate(points, -50, 100)), 1)
    pygame.draw.polygon(surface, (0, 0, 255),
                        list(rotate(points, math.radians(10))), 1)

    pygame.display.update()

    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass
