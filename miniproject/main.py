#!/usr/bin/env python3
import numpy as np
import cv2

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
hand_cascade = cv2.CascadeClassifier('hand2.xml')

def detect(img, cascade):
    rects = cascade.detectMultiScale(
            img,
            scaleFactor=2,
            minNeighbors=1,
            minSize=(10, 10),
            flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt
    print(__doc__)

    cam = cv2.VideoCapture(0)

    while True:
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        rects = detect(gray, hand_cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))

        cv2.imshow('facedetect', vis)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
