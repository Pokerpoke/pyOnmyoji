import logging
import sys
import os
import time
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o


def main_process(times=1, target="lei_qi_lin", time_used=7):

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("即将执行：" + str(times)+"次")

    if target in ["lei_qi_lin", "feng_qi_lin", "shui_qi_lin", "huo_qi_lin"]:
        o.goto_scene(target)
    else:
        logging.error("目标错误")

    for i in range(times):
        logging.info("第"+str(i + 1)+"次")

        # 阵容锁定
        LINEUP_LOCKED = o.lineup_locked()

        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(os.path.join(img_dir, "tiao_zhan.png"))
        u.random_click(p, 20)
        u.random_sleep(1, 0.3)

        if not LINEUP_LOCKED:
            o.click_mark("zhun_bei", interval=3)

        u.random_sleep(time_used, 0.3)
        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(
            img_dir, "sheng_li.png"), timeout=time_used)
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        u.random_sleep(3, 0.3)

    logging.info("完成")
