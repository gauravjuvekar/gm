#!/usr/bin/env python3
import cv2
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)

hue_range = ((80,20,20), (95, 255, 255))
history = deque(maxlen=64)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    blurred = cv2.blur(frame, (10, 10))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    obj_mask = cv2.inRange(hsv, *hue_range)
    obj_mask = cv2.erode(obj_mask, None, iterations=2)
    obj_mask = cv2.dilate(obj_mask, None, iterations=2)

    cv2.imshow("mask", obj_mask)
    cv2.imshow("hsv", hsv)

    contours = cv2.findContours(
            obj_mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    radius = 0
    if len(contours):
        largest = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest)
        print(x, y, radius)
        moments = cv2.moments(largest)
        center = (int(moments["m10"] / moments["m00"]),
                  int(moments["m01"] / moments["m00"]))
        print(center)
    if radius > 5:
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        history.append(center)
    prev = None
    for pt in history:
        if pt is None or prev is None:
            continue
        cv2.line(frame, prev, pt, (0, 0, 255), 5)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

