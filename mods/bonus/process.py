import sys
import os
import time
import logging
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o


def main_process(bonus=["jin_bi_100",
                        "jing_yan_50",
                        "jing_yan_100"],
                 on=True):

    img_dir = os.path.join(__file__, "..", "img")

    u.click_if_exists(os.path.join(img_dir, "jia_cheng.png"),
                      threshold=0.7, click_random=2)
    u.random_sleep(1, 0.2)

    if type(bonus) == str:
        bonus = [bonus]

    for b in bonus:
        u.click_if_exists(os.path.join(img_dir, b+".png"),
                          threshold=0.98, click_offset=(240, 0))
        u.random_sleep(0.5, 0.2)

    u.click_if_exists(os.path.join(img_dir, "jia_cheng.png"),
                      threshold=0.7, click_random=2)
    u.random_sleep(1, 0.2)

    logging.info("加成转换完成")


def bonus_on():
    """
    @TODO 动态的，不太好判断，再说
    """
    img_dir = os.path.join(__file__, "..", "img")

    if u.exists(os.path.join(img_dir, "bonus_trigger.png")):
        return False
