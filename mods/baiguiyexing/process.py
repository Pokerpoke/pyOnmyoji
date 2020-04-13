def main_process(times=1):
    import sys
    import os
    import time
    from datetime import datetime
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")
        # invite friend
        logging.info("Search for yao_qing_hao_you.png.")
        p = u.wait_until(os.path.join(img_dir, "yao_qing_hao_you.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        # choose friend
        logging.info("Search for xuan_ze_hao_you.png.")
        p = u.wait_until(os.path.join(img_dir, "xuan_ze_hao_you.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        # get in
        logging.info("Search for jin_ru.png.")
        p = u.wait_until(os.path.join(img_dir, "jin_ru.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        # choose monster king
        logging.info("Search for xuan_ze_gui_wang.png.")
        p = u.wait_until(os.path.join(img_dir, "xuan_ze_gui_wang.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        # start
        logging.info("Search for kai_shi.png.")
        p = u.wait_until(os.path.join(img_dir, "kai_shi.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        # za dou zi
        logging.info("Start piu piu piu.")
        while (True):
            p = u.exists(os.path.join(img_dir, "feng_xiang.png"))
            if p != None:
                u.random_sleep(1, 0.2)
                p = u.position_relative(0.95, 0.55)
                u.random_click(p, 20)
                u.random_sleep(0.5, 0.2)
                break
            p = u.position_relative(0.8, 0.55)
            u.random_click(p, 20)
            u.random_sleep(0.5, 0.2)

        u.random_sleep(3, 0.3)
