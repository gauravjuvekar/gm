#!/usr/bin/env python3
"""
Plots a line using DDA algorithm (integer arithmetic only)
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


def dda(start, end):
    """
    Returns a generator that gives the line pixel coordinates using DDA
    algorithm
    """
    ydiff = end.y - start.y
    xdiff = end.x - start.x

    if xdiff == 0:
        for y in irange(start.y, end.y):
            yield Point(start.x, y)
    else:
        slope = ydiff / xdiff
        if abs(slope) <= 1:
            y = start.y
            for x in irange(start.x, end.x):
                yield Point(x, int(round(y)))
                y += slope * sign(end.y - start.y)
        else:
            x = start.x
            for y in irange(start.y, end.y):
                yield Point(int(round(x)), y)
                x += (1 / slope) * sign(end.x - start.x)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("X_START",
                        type=int,
                        help="X coordinate of starting point")
    parser.add_argument("Y_START",
                        type=int,
                        help="Y coordinate of starting point")
    parser.add_argument("X_END",
                        type=int,
                        help="X coordinate of ending point")
    parser.add_argument("Y_END",
                        type=int,
                        help="Y coordinate of ending point")
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
    for point in dda(Point(args.X_START, args.Y_START),
                     Point(args.X_END, args.Y_END)):
        plot(point)
        time.sleep(0.005)
        pygame.display.update()

    # Wait till window quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
