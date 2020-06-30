import sys
import os
import time
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o
import logging
import queue


def img(img_name):
    img_dir = os.path.join(__file__, "..", "img")
    return os.path.join(img_dir, img_name+".png")


def scroller():
    return u.exists(img("scroller"), thresold=0.7)


def in_range(p1, p2, r=20):
    if abs(p1.x-p2.x) < r and abs(p1.y-p2.y) < r:
        return True
    else:
        return False


def main_process(times=1, time_used=35):

    o.goto_scene("jie_jie_ka_he_cheng")

    scroller_end = u.exists(img("scroller_end"), thresold=0.98)
    scroller_start = u.exists(img("scroller_start"), thresold=0.98)

    # u.slide(scroller(), scroller_end, duration=1)
    # time.sleep(1)
    # u.slide(scroller(), scroller_start, duration=1)

    slide_start = u.position_relative(0.3, 0.7)
    slide_end = u.position_relative(0.3, 0.3)

    u.slide(slide_start, slide_end)

    # p1 = u.exists(img("tai_yin_1"))
    # if p1 is not None:
    #     print(p1)
    #     # u.random_click(p1, 10)
    # u.random_sleep(1, 0.2)

    # while(True):
    #     p2 = u.exists(img("tai_yin_1"))
    #     if (p2 is not None) and (not in_range(p1, p2)):
    #         print(p1)
    #         # u.random_click(p2, 10)
    #         break
    #     u.random_sleep(1, 0.2)

    # i = 0

    # while (True):
    #     if i < 3:
