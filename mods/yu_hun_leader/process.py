import sys
import os
import time
import logging
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o


def img_path(img_name):
    path = os.path.join(__file__, "..", "img", img_name+".png")
    return path


def main_process(times=1, time_used=35):
    time_used_min = 18
    DEFAULT_INVITED = False

    for i in range(times):
        logging.info("第" + str(i + 1) + "次")
        # 锁定阵容
        o.lock_lineup()
        # 点击挑战
        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(img_path("tiao_zhan"))
        u.random_click(p, 20)
        # sleep以减少消耗
        time.sleep(time_used_min)
        # 等待战斗结束
        logging.info("Search for sheng_li.png.")
        p = u.wait_until(img_path("sheng_li"),
                         timeout=time_used*2)
        # 胜利下方点击
        p = u.offset_position(p, (300, 300))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)
        # 等待跳蛋
        logging.info("Search for jie_suan.png.")
        p = u.wait_until(img_path("jie_suan"))
        u.random_sleep(2, 0.3)
        u.random_click(p, 20)
        # 默认邀请好友
        if not DEFAULT_INVITED:
            try:
                p = u.wait_until(img_path("mo_ren_yao_qing_hao_you"),
                                 timeout=1,
                                 interval=0.1, notify=False)
                if p is not None:
                    u.random_click(p, 10)
                    u.random_sleep(0.5)
                    p = u.exists(img_path("que_ren"))
                    u.random_click(p, 10)
                    u.random_sleep(0.5)
                DEFAULT_INVITED = True
            except TimeoutError:
                pass
        # sleep以等待，等待稍久保证队员进入
        u.random_sleep(4.5, 0.3)
