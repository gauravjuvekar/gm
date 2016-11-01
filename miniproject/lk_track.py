#!/usr/bin/env python
import numpy as np
import cv2
from time import clock

lk_params = dict(winSize  = (15, 15),
                 maxLevel = 32,
                 criteria = (cv2.TERM_CRITERIA_EPS |
                             cv2.TERM_CRITERIA_COUNT,
                             10, 0.03))
spread_grow_distance = 6


class App(object):
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.unadded_tracks = []
        self.cam = cv2.VideoCapture(video_src)
        self.frame_idx = 0

        def add_points_cb(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONUP:
                param.append((float(x), float(y)))

        cv2.namedWindow("win_main")
        cv2.setMouseCallback(
            "win_main", add_points_cb, param=self.unadded_tracks)

    def run(self):
        while True:
            ret, frame = self.cam.read()
            frame = cv2.flip(frame, 1)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame_gray.copy()

            if len(self.tracks):
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32(
                        [tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(
                        img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(
                        img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks,
                                                 p1.reshape(-1, 2), good):
                    if not good_flag:
                        self.unadded_tracks.append((x + spread_grow_distance,
                                                    y + spread_grow_distance))
                        continue
                    tr.append((x, y))
                    # if len(tr) > self.track_len:
                        # del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 0, 255), 4)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks],
                                    False, (0, 0, 255))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                # p = cv2.goodFeaturesToTrack(
                        # frame_gray, mask=mask, **feature_params)
                p = np.array(self.unadded_tracks)
                del self.unadded_tracks[:]
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow("win_main", vis)

            ch = 0xff & cv2.waitKey(1)
            if ch == ord('q'):
                break

def main():
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0

    App(video_src).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
