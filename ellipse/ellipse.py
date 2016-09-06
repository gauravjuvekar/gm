#!/usr/bin/env python3
"""
Plots an ellipse using midpoint algorithm (integer arithmetic only)
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

def ellipse(radius_x, radius_y):
    rad_xsq = radius_x**2
    rad_ysq = radius_y**2
    x, y = 0, radius_y
    diff_x, diff_y = 0, 2 * y * rad_xsq
    diff = rad_ysq - (rad_xsq * radius_y) + (rad_xsq / 4)

    yield Point(x, y)

    while diff_x < diff_y:
        x += 1
        diff_x += 2 * rad_ysq
        if diff < 0:
            diff += rad_ysq + diff_x
        else:
            y -= 1
            diff_y -= 2 * rad_xsq
            diff += rad_ysq + diff_x - diff_y
        yield Point(x, y)
        yield Point(x, -y)
        yield Point(-x, y)
        yield Point(-x, -y)

    diff = (rad_ysq * (x + 0.5) * (x + 0.5) + rad_xsq * (y - 1) * (y - 1) -
            rad_xsq * rad_ysq)
    while y > 0:
        y -= 1
        diff_y -= 2 * rad_xsq
        if diff > 0:
            diff += rad_xsq - diff_y
        else:
            x += 1
            diff_x += 2 * rad_ysq
            diff += rad_xsq - diff_y + diff_x
        yield Point(x, y)
        yield Point(x, -y)
        yield Point(-x, y)
        yield Point(-x, -y)

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
    parser.add_argument("RADIUS_X",
                        type=int,
                        help="X axis radius of the ellipse")
    parser.add_argument("RADIUS_Y",
                        type=int,
                        help="Y axis radius of the ellipse")
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
                  for point in ellipse(args.RADIUS_X, args.RADIUS_Y)):
        plot(point)
        time.sleep(0.005)
        pygame.display.update()

    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass
