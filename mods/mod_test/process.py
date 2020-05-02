import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u


def main_process(thresold=0.7, type=0):
    o.goto_scene("kun_28")
    u.random_sleep(1, 0.2)
    o.goto_scene("ting_yuan")
    u.random_sleep(1, 0.2)
    o.goto_scene("lei_qi_lin")
