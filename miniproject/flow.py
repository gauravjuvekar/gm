#!/usr/bin/env python3

'''
example to show optical flow

USAGE: opt_flow.py [<video_source>]

Keys:
 1 - toggle HSV flow visualization
 2 - toggle glitch

Keys:
    ESC    - exit
'''

# Python 2/3 compatibility
import numpy as np
import cv2

from collections import deque

from itertools import islice


def window(seq, n=2):
    """
    Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
    return res


def filter_reduce_flow(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    return [fx.mean(), fy.mean()]


if __name__ == '__main__':
    import sys
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 0

    cam = cv2.VideoCapture(fn)
    ret, prev = cam.read()
    prev = cv2.flip(prev, 1)
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()

    threshold = 0.8
    history = deque(maxlen=10)

    while True:
        ret, img = cam.read()
        win_x, win_y = img.shape[:2]
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
                prevgray,
                gray,
                None,
                0.5,
                3,
                15,
                3,
                5,
                1.2,
                0)
        prevgray = gray

        aggregate = filter_reduce_flow(flow)
        x, y = aggregate
        if abs(x) < threshold and abs(y) < threshold:
            direction = None
        else:
            direction = np.arctan2(y, x)
            r = 100
            lx = r * np.cos(direction)
            lx = int(lx)
            ly = r * np.sin(direction)
            ly = int(ly)
            cv2.line(
                    img,
                    (win_x//2, win_y//2),
                    (win_x//2 + lx, win_y//2 + ly),
                    (0, 255, 255))
            direction = int((np.degrees(direction) + 360 + 90) % 360)
            # dir_step = [0, 45, 135, 225, 315, 360]
            # dir_geo = ["N", "E", "S", "W", "N"]
            dir_step = [0, 180, 360]
            dir_geo = ["R", "L", "R"]
            for i, (l, h) in enumerate(window(dir_step, 2)):
                if l<= direction < h:
                    direction = dir_geo[i]
                    break

        history.append(direction)
        print(direction)
        cv2.imshow("img", img)


        # cv2.imshow('flow', draw_flow(gray, flow))
        if show_hsv:
            cv2.imshow('flow HSV', draw_hsv(flow))
        if show_glitch:
            cur_glitch = warp_flow(cur_glitch, flow)
            cv2.imshow('glitch', cur_glitch)

        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break
        if ch == ord('1'):
            show_hsv = not show_hsv
            print('HSV flow visualization is', ['off', 'on'][show_hsv])
        if ch == ord('2'):
            show_glitch = not show_glitch
            if show_glitch:
                cur_glitch = img.copy()
            print('glitch is', ['off', 'on'][show_glitch])
    cv2.destroyAllWindows()
