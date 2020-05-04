import sys
import os
import time
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o
import logging
from datetime import datetime
import mods.bonus.process as bonus


def main_process(times=1, time_used=35):
    img_dir = os.path.join(__file__, "..", "img")

    logging.info("即将执行"+str(times)+"次")

    INVITE_LOCKED = False
    LINEUP_LOCKED = False

    logging.info("开启加成")
    bonus.main_process("yu_hun")

    for i in range(times):
        logging.info("第" + str(i + 1) + "次")

        if not INVITE_LOCKED:
            logging.info("等待接受邀请")
            start = datetime.now()
            while (True):

                if u.click_if_exists(os.path.join(img_dir,
                                                  "suo_ding_jie_shou_yao_qing.png"), interval=1):
                    logging.info("锁定接受邀请")
                    INVITE_LOCKED = True
                    time.sleep(0.2)
                    break

                if u.click_if_exists(os.path.join(img_dir,
                                                  "jie_shou_yao_qing.png"),
                                     interval=1):
                    logging.info("接受邀请")
                    INVITE_LOCKED = False
                    time.sleep(0.2)
                    break

                end = datetime.now()
                if (end - start).seconds > 300:
                    logging.error("等待接受邀请超时，请重新启动")
                    return

        time.sleep(1)

        o.lock_lineup()
        time.sleep(time_used)

        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                         timeout=time_used+25)
        u.random_sleep(1, 0.3)
        p = u.offset_position(p, (300, 300))
        u.random_click(p, 20)

        u.click_if_exists(os.path.join(img_dir, "dian_zan.png"))

        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        u.random_sleep(1, 0.3)
        p = u.offset_position(p, (300, 0))
        u.random_click(p, 20)

        u.random_sleep(3, 0.3)

    logging.info("关闭加成")
    bonus.main_process("yu_hun")

    logging.info(str(times)+"次御魂（队员）完成")
