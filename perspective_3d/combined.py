#!/usr/bin/env python3
"""
Shows a rotating cube in parallel and perspective projections
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
    Return signum(`number`)
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
    Return an inclusive 'range()' generator in steps of `abs_delta`
    """
    diff = end - start
    return range(start, end + sign(diff), sign(diff) * abs_delta)


def translate(points, shift_x, shift_y, shift_z):
    """
    Translate either a single 'Point()' or an iterable of 'Point()'s
    Return:
        iterable of translated 'Point()'s
    """
    if isinstance(points, Point):
        iter_points = iter((points,))
    else:
        iter_points = iter(points)
    for point in iter_points:
        yield Point(point.x + shift_x, point.y + shift_y, point.z + shift_z)


def scale(points, scale_x, scale_y, scale_z):
    """
    Scale either a single 'Point()' or an iterable of 'Point()'s
    Return:
        iterable of scaled 'Point()'s
    """
    if isinstance(points, Point):
        iter_points = iter((points,))
    else:
        iter_points = iter(points)
    for point in iter_points:
        yield Point(point.x * scale_x, point.y * scale_y, point.z * scale_z)


def rotate(points, angle, axis):
    """
    Rotates either a single 'Point()' or an iterable of 'Point()'s about `axis`
    by `angle` (in radians).
    Return:
        iterable of rotated 'Point()'s
    """
    if isinstance(points, Point):
        iter_points = iter((points,))
    else:
        iter_points = iter(points)
    l = axis.x
    m = axis.y
    n = axis.z
    matrix = [[l * l * (1 - math.cos(angle)) + 1 * math.cos(angle),
               m * l * (1 - math.cos(angle)) - n * math.sin(angle),
               n * l * (1 - math.cos(angle)) + m * math.sin(angle)],
              [l * m * (1 - math.cos(angle)) + n * math.sin(angle),
               m * m * (1 - math.cos(angle)) + 1 * math.cos(angle),
               n * m * (1 - math.cos(angle)) - l * math.sin(angle)],
              [l * n * (1 - math.cos(angle)) - m * math.sin(angle),
               m * n * (1 - math.cos(angle)) + l * math.sin(angle),
               n * n * (1 - math.cos(angle)) + 1 * math.cos(angle)]]
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
    """
    Convenience wrapper to rotate faces defined as an iterable of 'Point()'s
    about `axis` by `angle` radians.
    Returns:
        iterable of iterables of rotated face 'Point()'s
    """
    return (rotate(face, angle, axis) for face in faces)


def intify(points):
    """
    Round `points` (which can be a single 'Point()' or an iterable of
    'Point()'s) coordinates to integers.
    Return:
        iterable of 'Point()'s
    """
    if isinstance(points, Point):
        iter_points = iter((points,))
    else:
        iter_points = iter(points)
    for point in iter_points:
        yield Point(int(round(point.x)),
                    int(round(point.y)),
                    int(round(point.z)))


def animate(poly_shape, vector, rotation_range):
    """
    Animate `poly_shape` (iterable of faces which are themselves iterables of
    'Point()'s) by rotating it about `vector` in 1 degree steps from 0 to
    `rotation_range` degrees.
    Return:
        iterable of each rotated shape
    """
    for angle in rotation_range:
        faces = [[point for point in face] for face in
                 rotate_faces(poly_shape, math.radians(angle), vector)]
        yield list(faces)


def perspective_project(point, cam, screen_z):
    """
    Returns the perspective projection of `point` onto a screen parallel to the
    XY plane with Z coordinate `screen_z`, and center of projection as `cam`.
    Return:
        'Point()' on the screen
    """
    x = cam.x + ((screen_z - cam.z) * (cam.x - point.x) / (point.z - cam.z))
    y = cam.y + ((screen_z - cam.z) * (cam.y - point.y) / (point.z - cam.z))
    return Point(x, y, screen_z)


def parallel_project(point, screen_z=0):
    """
    Returns the parallel projection of `point` onto a screen parallel to the
    XY plane.
    Return:
        'Point()' on the screen
    """
    return Point(point.x, point.y, screen_z)


def flatten(point):
    """
    Convert a 3D 'Point()' `point` into a tuple of screen coordinates
    """
    point = list(intify(point))[0]
    return (point.x, point.y)


def main(args):
    cam = Point(args.cam_x, args.cam_y, args.cam_z)
    vector = UnitVector(args.VECTOR_X, args.VECTOR_Y, args.VECTOR_Z)

    # Define a cube as a list of faces with each face being a list of 'Point()'s
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
    # Shift it so that cube is centered at the origin
    cube = [list(translate(
        face,
        -CUBE_SIDE // 2,
        -CUBE_SIDE // 2,
        -CUBE_SIDE // 2)) for face in cube]

    # Init display
    pygame.display.init()
    screen = pygame.display.set_mode((args.window_size, args.window_size))
    surface = pygame.display.get_surface()

    # Get incrementally rotated cubes
    for cube in animate(cube, vector, range(args.angle + 1)):
        # Shift it at the center of the screen, and make its Z coordinates
        # negative.
        cube = [list(translate(face,
                               args.window_size // 2,
                               args.window_size // 2,
                               -CUBE_SIDE * 1.5)) for face in cube]
        perspectives = [[perspective_project(point, cam, args.screen_z)
                         for point in face]
                        for face in cube]
        parallels = [[parallel_project(point) for point in face]
                     for face in cube]

        # Shift projections to appear side by side
        perspectives = [list(translate(face, +CUBE_SIDE * 1, 0, 0))
                        for face in perspectives]
        parallels = [list(translate(face, -CUBE_SIDE * 1, 0, 0))
                     for face in parallels]

        # Convert to tuples as pygame.draw takes only 2d tuples
        parallels = [[flatten(point) for point in face] for face in parallels]
        perspectives = [[flatten(point) for point in face]
                        for face in perspectives]
        for polygon in perspectives:
            pygame.draw.polygon(surface, (255, 255, 255), polygon, 1)
        for polygon in parallels:
            pygame.draw.polygon(surface, (255, 0, 255), polygon, 1)

        pygame.display.update()
        time.sleep(0.01)
        surface.fill((0,0,0))

    # Wait till window quit
    while pygame.event.wait().type != pygame.QUIT:
        pass


if __name__ == '__main__':
    # Get command line arguments
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
    parser.add_argument("--cam_x",
                        type=int,
                        help="X coordinate of camera",
                        default=500)
    parser.add_argument("--cam_y",
                        type=int,
                        help="Y coordinate of camera",
                        default=500)
    parser.add_argument("--cam_z",
                        type=int,
                        help="Z coordinate of camera",
                        default=500)
    parser.add_argument("--screen-z",
                        type=int,
                        help="Z coordinate of screen",
                        default=0)
    parser.add_argument("--angle",
                        type=int,
                        help="Angle to rotate in degrees",
                        default=360)
    parser.add_argument("--window-size", "-w",
                        type=int,
                        default=1000,
                        help="Window size in pixels (equal width an height)")
    args = parser.parse_args()
    main(args)
