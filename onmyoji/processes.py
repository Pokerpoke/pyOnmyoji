# -*- coding:utf-8 -*-

import cv2
import time
import os
import json
import getopt
import sys
import random
from datetime import datetime
from .window_funcs import *

background = False

def base_process(mod,times=1):
    handle = find_window("阴阳师-网易游戏")
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(handle)
    pos_window = get_window_pos(handle)

    # opts, args = getopt.getopt(sys.argv[1:], "t:")
    # times = 1
    # for option, value in opts:
    #     if option == "-t":
    #         times = value
    #         print("Going to run for " + times + " times.")
    #     elif option == "-c":
    #         file_path = value
    #         print("Going to use " + file_path + " as configure file.")
    #     else:
    #         assert False, "unhandled option"

    workspace_path = os.getcwd()
    mod_name = mod
    mod_path = os.path.join(workspace_path, "mods", mod_name)
    strategy_file = os.path.join(mod_path, "strategy.json")

    j = None
    with open(strategy_file) as f:
        j = json.load(f)

    print("Start ", mod_name)

    for i in range(int(times)):
        print("Times: " + str(i + 1))
        for state in j["process"]:
            print("Current state: ", state["state"])


            if "img" in state:
                state_img = os.path.join(mod_path, "img", state['img'])
                template = cv2.imread(state_img)

                timeout = 10
                if "timeout" in state:
                    timeout = state["timeout"]
                p = wait_until(template,timeout=timeout)
                if p == None:
                    print("template not found")
                    return
            elif "position" in state:
                p = Point(state["position"]["x"],
                          state["position"]["y"])
            elif "position_relative" in state:
                p = Point(int(pos_window.x +
                              pos_window.width * state["position_relative"]["x"]),
                          int(pos_window.y +
                              pos_window.height * state["position_relative"]["y"]))

            if "offset_x" in state:
                p.x = p.x + state["offset_x"]

            if "offset_y" in state:
                p.y = p.y + state["offset_y"]

            if state["operation"] == "click":
                if "random" in state and state["random"] != 0:
                    p = p + \
                        Point(random.randint(-state["random"], state["random"]),
                              random.randint(-state["random"], state["random"]))

                if "wait_before" in state:
                    print("Sleep for ", state["wait_before"], " seconds")
                    time.sleep(state["wait_before"])

                click(p,background=background)

            elif state["operation"] == "keep_clicking":
                begin_time = datetime.now()
                while(True):
                    if "random" in state and state["random"] != 0:
                        p = p + \
                            Point(random.randint(-state["random"], state["random"]),
                                  random.randint(-state["random"], state["random"]))

                    if "wait_before" in state:
                        print("Sleep for ", state["wait_before"], " seconds")
                        time.sleep(state["wait_before"])

                    click(p,background=background)

                    if "random_interval" in state:
                        time.sleep(state["interval"] +
                                   random.uniform(-state["random_interval"], state["random_interval"]))
                    else:
                        time.sleep(state["interval"])

                    end_time = datetime.now()
                    if (end_time - begin_time).seconds >= state["timeout"]:
                        break

            if "wait_after" in state:
                print("sleep for ", state["wait_after"], " seconds")
                time.sleep(state["wait_after"])

    print("finished")