#!/usr/bin/env python3
"""
Plots a circle using Bresenham's algorithm (integer arithmetic only)
"""
import pygame
import argparse
import math
from collections import namedtuple
import time

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

def circle(radius):
    """
    Returns a generator that gives the points of a circle of radius `radius`
    centered at the origin.
    """
    x, y = 0, radius
    diff = 3 - 2 * radius
    while x <= y:
        yield Point(x, y)
        yield Point(x, -y)
        yield Point(-x, y)
        yield Point(-x, -y)
        yield Point(y, x)
        yield Point(y, -x)
        yield Point(-y, x)
        yield Point(-y, -x)
        diff += 4 * x + 6
        if diff > 0:
            diff += -(4 *  y) + 4
            y -= 1
        x += 1

def translate(shift_x, shift_y, point):
    return Point(shift_x + point.x, shift_y + point.y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("CENTER_X",
                        type=int,
                        help="X coordinate of center")
    parser.add_argument("CENTER_Y",
                        type=int,
                        help="Y coordinate of center")
    parser.add_argument("RADIUS",
                        type=int,
                        help="Radius of the circle")
    parser.add_argument("--window-size", "-w",
                        type=int,
                        default=500,
                        help="Window size in pixels (equal width an height)")
    args = parser.parse_args()

    # Init display
    pygame.display.init()
    screen = pygame.display.set_mode((args.window_size, args.window_size))
    surface = pygame.display.get_surface()

    # Plot generated points
    for point in (translate(args.CENTER_X, args.CENTER_Y, point)
                  for point in circle(args.RADIUS)):
        plot(point)
        time.sleep(0.005)
        pygame.display.update()

    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass
