def main_process(times=1, time_used=7):
    import sys
    import os
    import time
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import logging
    import win32api
    import win32con

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("Will run for "+str(times)+" times.")

    while True:
        logging.info("Search for ling_qu.png.")
        p = u.exists(os.path.join(img_dir, "ling_qu.png"))
        if p == None:
            logging.info("No awards to get.")
        else:
            u.random_sleep(1, 0.2)
            u.random_click(p, 5)
            u.random_sleep(1, 0.2)

        logging.info("Search for huo_de_jiang_li.png.")
        p = u.exists(os.path.join(img_dir, "huo_de_jiang_li.png"))
        if p != None:
            p = u.offset_position(p, (400, 0))
            u.random_sleep(1, 0.2)
            u.random_click(p, 20)
            u.random_sleep(1, 0.2)

        time.sleep(2)

    # for i in range(times):
    #     logging.info("Start for times: "+str(i + 1)+".")

    #     logging.info("Search for yi_jian_ling_qu.png.")
    #     p = u.exists(os.path.join(img_dir, "yi_jian_ling_qu.png"))
    #     if p == None:
    #         logging.info("No awards to get.")
    #     else:
    #         u.random_sleep(1, 0.2)
    #         u.random_click(p, 5)
    #         u.random_sleep(1, 0.2)

    #     logging.info("Search for huo_de_jiang_li.png.")
    #     p = u.wait_until(os.path.join(img_dir, "huo_de_jiang_li.png"))
    #     p = u.offset_position(p, (400, 0))
    #     u.random_sleep(1, 0.2)
    #     u.random_click(p, 20)
    #     u.random_sleep(1, 0.2)

    #     logging.info("Search for ling_qu.png.")
    #     p = u.exists(os.path.join(img_dir, "ling_qu.png"))
    #     if p == None:
    #         logging.info("No awards to get.")
    #     else:
    #         u.random_sleep(1, 0.2)
    #         u.random_click(p, 5)
    #         u.random_sleep(1, 0.2)

    #     logging.info("Search for huo_de_jiang_li.png.")
    #     p = u.wait_until(os.path.join(img_dir, "huo_de_jiang_li.png"))
    #     p = u.offset_position(p, (400, 0))
    #     u.random_sleep(1, 0.2)
    #     u.random_click(p, 20)
    #     u.random_sleep(1, 0.2)

        # logging.info("Search for tiao_zhan.png.")
        # p = u.wait_until(os.path.join(img_dir, "tiao_zhan.png"))
        # u.random_click(p, 20)
        # u.random_sleep(time_used+3, 0.3)

        # logging.info("Search for sheng_li.png.")
        # p = u.wait_until(os.path.join(img_dir, "sheng_li.png"))
        # u.random_sleep(1, 0.3)
        # u.random_click(p, 20)

        # logging.info("Search for jie_suan.png.")
        # p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        # u.random_sleep(1, 0.3)
        # u.random_click(p, 20)

        # u.random_sleep(3, 0.3)
