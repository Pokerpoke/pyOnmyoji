#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import time
import os
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u


def main_process():
    img_dir = os.path.join(__file__, "..", "img")
    o.goto_scene("hao_you")
    time.sleep(1)
    o.click_if_exists(os.path.join(img_dir, "hao_you.png"))
    time.sleep(1)

    p_src = u.position_relative(0.3, 0.7)
    p_des = u.position_relative(0.3, 0.5)

    while (True):

        time_up = None

        p = o.exists(os.path.join(
            img_dir, "you_qing_dian_fen_hong.png"), threshold=0.98)
        if p is not None:
            u.random_sleep(1, 0.2)
            u.random_click(p, 10)
            u.random_sleep(2, 0.2)
            u.random_click(p, 10)

            time_up = u.wait_until(os.path.join(img_dir, "ci_shu_shang_xian.png"),
                                   timeout=1, interval=0.1, notify=False, raise_except=False)
        else:
            u.slide(p_src, p_des)

        if time_up is not None:
            logging.info("友情点次数上限")
            break

    logging.info("友情点领取完成")
