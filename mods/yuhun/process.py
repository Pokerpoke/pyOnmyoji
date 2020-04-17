def main_process(times=1, time_used=7):
    import sys
    import os
    import time
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("Will run for: "+str(times)+" times.")

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")

        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(os.path.join(img_dir, "tiao_zhan.png"))
        u.random_click(p, 20)
        u.random_sleep(time_used+3, 0.3)

        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(img_dir, "sheng_li.png"))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        u.random_sleep(3, 0.3)

    logging.info("Finished.")
