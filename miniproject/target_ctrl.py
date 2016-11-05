#!/usr/bin/env python3

import subprocess

class WinManager(object):
    def __init__(self):
        output = subprocess.check_output(["wmctrl", "-d"])
        output = output.split(b'\n')
        output = [x.decode().split() for x in output]
        workspace_ids = []
        self.current = None
        for ws in output:
            if len(ws):
                this = int(ws[0])
                if ws[1] == '*':
                    self.current = this
                workspace_ids.append(this)
        self.n_wspaces = len(workspace_ids)

    def switch(self, wspace_num):
        if not wspace_num < self.n_wspaces:
            raise ValueError("no such workspace")

        self.current = wspace_num
        subprocess.check_call(["wmctrl", "-s", str(wspace_num)])

    def switch_next(self):
        self.switch((self.current + 1) % self.n_wspaces)

    def switch_prev(self):
        self.switch((self.current - 1) % self.n_wspaces)


if __name__ == "__main__":
    wm = WinManager()

