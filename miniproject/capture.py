#!/usr/bin/env python3
import numpy as np
import cv2

def draw_bounding_rect(img, rects, color=(0, 255, 0), thickness=1):
    for x, y, w, h in rects:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness)


cap = cv2.VideoCapture(0)

armature_rects = []

sel_rect_last_down = None
def init_click_cb(event, x, y, flags, param):
    global armature_points
    global sel_rect_last_down
    if event == cv2.EVENT_LBUTTONDOWN:
        sel_rect_last_down = (x, y)
    if event == cv2.EVENT_LBUTTONUP:
        x2, y2 = sel_rect_last_down
        top_left = (min(x, x2), min(y, y2))
        bottom_right = (max(x, x2), max(y, y2))
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        if width > 0 and height > 0:
            armature_rects.append((*top_left, width, height))

cv2.namedWindow("win_main")
cv2.setMouseCallback("win_main", init_click_cb)

def get_new_bounding(frame, track):
    x, y, w, h = track
    roi = frame[x:x+h, y:y+w]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", hsv)
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi,
                       np.array((0.0, 60.0, 32.0)),
                       np.array((180.0, 255,0, 255.0)))
    print("mask", mask)
    roi_histogram = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    print("hist", mask)
    cv2.normalize(roi_histogram, roi_histogram, 0, 255, cv2.NORM_MINMAX)
    term_condition = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                      10, 1)
    dst = cv2.calcBackProject([hsv], [0], roi_histogram, [0, 180], 1)
    ret, track = cv2.meanShift(dst, track, term_condition)
    return ret, track


while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    for i, track in enumerate(armature_rects):
        ret, new_track = get_new_bounding(frame, track)
        print(new_track)
        armature_rects[i] = new_track
        # pts = cv2.boxPoints(ret)
        # pts = np.int0(pts)
        # img2 = cv2.polylines(frame, [pts], True, 255, 2)
        # cv2.imshow("img2", img2)

    draw_bounding_rect(frame, armature_rects, thickness=2)

    cv2.imshow("win_main", frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
    elif key == ord('r'):
        del armature_rects[:]
cap.release()
cv2.destroyAllWindows()
