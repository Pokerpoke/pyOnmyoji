def main_process(times=1, time_used=7):
    import sys
    import os
    import time
    import onmyoji.utils as u
    import onmyoji.onmyoji_funcs as o
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    u.click_if_exists(os.path.join(img_dir, "jia_cheng.png"),
                      thresold=0.7, click_random=2)
    u.random_sleep(2, 0.2)

    u.click_if_exists(os.path.join(img_dir, "jing_yan_50.png"),
                      thresold=0.98, click_offset=(240, 0))
    u.random_sleep(0.5, 0.2)

    u.click_if_exists(os.path.join(img_dir, "jing_yan_100.png"),
                      thresold=0.98, click_offset=(240, 0))
    u.random_sleep(0.5, 0.2)

    u.click_if_exists(os.path.join(img_dir, "jin_bi_100.png"),
                      thresold=0.98, click_offset=(240, 0))
    u.random_sleep(0.5, 0.2)

    u.click_if_exists(os.path.join(img_dir, "jia_cheng.png"),
                      thresold=0.7, click_random=2)
    u.random_sleep(1, 0.2)

    logging.info("Trig bonus finished")
