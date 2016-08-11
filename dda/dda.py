#!/usr/bin/env python3
import pygame
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("X_START", type=int)
parser.add_argument("Y_START", type=int)
parser.add_argument("X_END", type=int)
parser.add_argument("Y_END", type=int)
parser.add_argument("--window-size", "-w", type=int, default=500)
args = parser.parse_args()

pygame.display.init()
screen = pygame.display.set_mode((args.window_size, args.window_size))
surface = pygame.display.get_surface()

WHITE = (255, 255, 255)

sign = lambda x: int(math.copysign(1, x))

def irange(start, end, abs_delta):
    diff = end - start
    return range(start, end + sign(diff), sign(diff) * abs_delta)

def plot(x, y):
    surface.set_at((x, y), WHITE)

def dda(start, end):
    INCREMENT = 1
    ydiff = (end[1] - start[1])
    xdiff = (end[0] - start[0])

    if xdiff == 0:
        for y in irange(start[1], end[1], INCREMENT):
            plot(start[0], y)
    else:
        slope = ydiff / xdiff
        if abs(slope) <= 1:
            y = start[1]
            for x in irange(start[0], end[0], INCREMENT):
                plot(x, int(round(y)))
                y += slope * sign(end[1] - start[1])
        else:
            x = start[0]
            for y in irange(start[1], end[1], INCREMENT):
                plot(int(round(x)), y)
                x += (1 / slope) * sign(end[0] - start[0])

dda((args.X_START, args.Y_START), (args.X_END, args.Y_END))

pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
