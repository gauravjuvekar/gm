#!/usr/bin/env python3
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(1):
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    # print("*"*80)
    # print(len(corners))
    # print(corners)
    corners = np.int0(corners)
    print(corners.ndim, corners.strides)
    print(corners.shape)
    corn2 = np.array([[[1, 2]], [[3, 34]]])
    print(corn2.ndim, corn2.strides)
    print(corn2.shape)
    break
    for i in corners:
        x, y = i.ravel()
        cv2.circle(frame, (x, y), 3, 255, 4)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
    elif key == ord('r'):
        del armature_rects[:]

cv2.destroyAllWindows()
cap.release()
