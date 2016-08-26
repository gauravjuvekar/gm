#!/usr/bin/env python3
import pygame
import argparse
import math
import time

parser = argparse.ArgumentParser()
parser.add_argument("CENTER_X", type=int)
parser.add_argument("CENTER_Y", type=int)
parser.add_argument("RADIUS", type=int)
parser.add_argument("--window-size", "-w", type=int, default=500)
args = parser.parse_args()

pygame.display.init()
screen = pygame.display.set_mode((args.window_size, args.window_size))
surface = pygame.display.get_surface()

WHITE = (255, 255, 255)

sign = lambda x: int(math.copysign(1, x))

def plot(x, y):
    surface.set_at((x, y), WHITE)

def irange(start, end, abs_delta):
    diff = end - start
    return range(start, end + sign(diff), sign(diff) * abs_delta)

def tranlsate_plot_8(x, y, shift_x, shift_y):
    plot(shift_x + x, shift_y + y)
    plot(shift_x - x, shift_y + y)
    plot(shift_x + x, shift_y - y)
    plot(shift_x - x, shift_y - y)
    plot(shift_x + y, shift_y + x)
    plot(shift_x - y, shift_y + x)
    plot(shift_x + y, shift_y - x)
    plot(shift_x - y, shift_y - x)

def circle(center, radius):
    x, y = radius, 0
    diff = -radius
    prev_x, prev_y = x, y
    for y in irange(0, int(round(radius / math.sqrt(2))), 1):
        tranlsate_plot_8(x, y, *center)
        if diff > 0:
            x -= 1
            diff += 2 * prev_y - 2 * prev_x + 3
        else:
            diff+= 2 * prev_y + 1
        prev_x, prev_y = x, y

circle((args.CENTER_X, args.CENTER_Y), args.RADIUS)

pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
