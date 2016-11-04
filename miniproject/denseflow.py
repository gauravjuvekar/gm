#!/usr/bin/env python3

import cv2
import numpy as np
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
frame1 = cv2.flip(frame1, 1)
frame_prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while(1):
    ret, frame2 = cap.read()
    frame2 = cv2.flip(frame2, 1)
    frame_next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(
            frame_prev,
            frame_next,
            None,
            0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2', rgb)
    cv2.imshow("raw_frame", frame_next)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',rgb)
    frame_prev = frame_next

cap.release()
cv2.destroyAllWindows()
