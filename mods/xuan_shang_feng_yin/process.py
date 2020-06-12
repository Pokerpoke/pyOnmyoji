import logging
import sys
import os
import time
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o
import mods.bonus.process as bonus


def img_path(img_name):
    path = os.path.join(__file__, "..", "img", img_name+".png")
    return path


def main_process(times=1, time_used=7, target="lei_qi_lin"):
    o.goto_scene("ting_yuan")

    p = u.exists(img_path("feng"))
    if p is not None:
        u.random_click(p)
