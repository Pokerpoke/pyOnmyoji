import sys
import os
import time
import logging
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o


def main_process(times=1, time_used=7):

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("Will run for: "+str(times)+" times")

    o.goto_scene("yu_ling")

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")

        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(os.path.join(img_dir, "tiao_zhan.png"))
        u.random_sleep(1, 0.2)
        u.random_click(p, 20)

        u.random_sleep(time_used+3, 0.3)

        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                         timeout=time_used, interval=0.2)
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"), timeout=30)
        u.random_sleep(3, 0.3)
        u.random_click(p, 20)

        u.random_sleep(3, 0.3)

    logging.info("Finished.")
