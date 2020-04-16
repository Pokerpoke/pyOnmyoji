def main_process(times=1, time_used=7):
    import sys
    import os
    import time
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    p = u.position_relative(0.4, 0.6)
    u.random_click(p, 20)
    u.random_sleep(1, 0.2)

    logging.info("Search for quan_bu.png")
    p = u.wait_until(os.path.join(img_dir, "quan_bu.png"))
    u.random_sleep(1, 0.2)
    u.random_click(p, 20)

    logging.info("Search for su_cai.png")
    p = u.wait_until(os.path.join(img_dir, "su_cai.png"), thresold=0.99)
    u.random_sleep(1, 0.2)
    u.random_click(p, 20)

    u.random_sleep(3, 0.3)

    for _ in range(4):
        logging.info("Search for man_2.png")
        des = u.exists(os.path.join(img_dir, "man_2.png"), thresold=0.99)

        if des == None:
            logging.info("Search for man_3.png")
            des = u.exists(os.path.join(img_dir, "man_3.png"), thresold=0.99)

        if des != None:
            des.y = des.y + 100
        else:
            time.sleep(1)
            continue

        logging.info("Search for gou_liang_bai_dan.png")
        src = u.wait_until(os.path.join(
            img_dir, "gou_liang_bai_dan.png"), thresold=0.99)

        if src != None:
            temp = u.Point(src.x, src.y-200)
            u.slide(src, temp, release=False)
            u.slide(temp, des)

        time.sleep(0.5)

    logging.info("Search for fan_hui.png")
    p = u.wait_until(os.path.join(img_dir, "fan_hui.png"))
    u.random_sleep(1, 0.2)
    u.random_click(p, 20)
    u.random_sleep(1, 0.2)

    logging.info("Finished.")
