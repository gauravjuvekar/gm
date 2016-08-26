#!/usr/bin/env python3
"""
Plots a line using Bresenham's algorithm (integer arithmetic only)
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

def bresanham_quad0(start, end):
    """
    Returns a generator that gives the line pixel coordinates using Bresenham's
    algorithm, suitable only for the first quadrant and for lines with
    slopes < 1
    """
    INCREMENT = 1
    ydiff = end.y - start.y
    assert(ydiff >= 0)
    ydiff_2  = 2 * ydiff
    xdiff = end.x - start.x
    assert(xdiff >= 0)
    xdiff_2 = 2 * xdiff
    # Plot start point
    yield start
    error_parameter = ydiff_2 - xdiff
    y = start.y
    assert(xdiff >= ydiff)
    for x in irange(start.x, end.x):
        if error_parameter > 0:
            y += 1
            error_parameter -= xdiff_2
        yield Point(x, y)
        error_parameter += ydiff_2

def bresanham(start, end):
    """
    Applies proper input and output transformations to convert the line into
    first quadrant with slope < 1
    The compass directions are given in comments
    +--------+--------+
    |\       |       /|
    | \  NNW | NNE  / |
    |  \     |     /  |
    |   \    |    /   |
    |    \   |   /    |
    |     \  |  /     |
    | WNW  \ | / ENE  |
    |       \|/       |
    +--------X--------+
    |       /|\       |
    | WSW  / | \ ESE  |
    |     /  |  \     |
    |    /   |   \    |
    |   /    |    \   |
    |  / SSW | SSE \  |
    | /      |      \ |
    |/       |       \|
    +--------+--------+
    """
    end = Point(end.x - start.x, end.y - start.y)
    xdiff = end.x
    ydiff = end.y
    if xdiff >= 0 and ydiff >= 0:
        # SE
        if xdiff >= ydiff:
            # ESE
            transform_in = lambda point: point
            transform_out = transform_in
        else:
            # SSE
            transform_in = lambda point: Point(point.y, point.x)
            transform_out = transform_in
    elif xdiff >= 0 and ydiff < 0:
        # NE
        if xdiff >= -ydiff:
            # ENE
            transform_in = lambda point: Point(point.x, -point.y)
            transform_out = transform_in
        else:
            # NNE
            transform_in = lambda point: Point(-point.y, point.x)
            transform_out = lambda point: Point(point.y, -point.x)
    elif xdiff < 0 and ydiff >= 0:
        # SW
        if -xdiff >= ydiff:
            # WSW
            transform_in = lambda point: Point(-point.x, point.y)
            transform_out = transform_in
        else:
            # SSW
            transform_in = lambda point: Point(point.y, -point.x)
            transform_out = lambda point: Point(-point.y, point.x)
    else:
        # NW
        if -xdiff >= -ydiff:
            # WNW
            transform_in = lambda point: Point(-point.x, -point.y)
            transform_out = transform_in
        else:
            # NNW
            transform_in = lambda point: Point(-point.y, -point.x)
            transform_out = transform_in
    transform_final = lambda point: Point(transform_out(point).x + start.x,
                                          transform_out(point).y + start.y)
    return (transform_final(point) for point in
            bresanham_quad0(Point(0, 0), transform_in(end)))

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
    for point in bresanham(Point(args.X_START, args.Y_START),
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
