def main_process(times=1, time_used=35):
    import sys
    import os
    import time
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    for i in range(times):
        logging.info("Start for times: " + str(times + 1) + ".")

        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                         timeout=time_used+25)
        u.random_sleep(1, 0.3)
        p = u.offset_position(p, (300, 300))
        u.random_click(p, 20)

        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        u.random_sleep(1, 0.3)
        p = u.offset_position(p, (300, 0))
        u.random_click(p, 20)

        u.random_sleep(time_used+15, 0.3)
