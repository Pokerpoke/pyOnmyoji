import sys
import os
import time
import logging
import onmyoji.utils as utils
from onmyoji.game_instance import GameInstance


def img_path(img_name):
    path = os.path.join(__file__, "..", "img", img_name+".png")
    return path


def main_process(times=1, time_used=35, handle=None):
    time_used_min = 18
    DEFAULT_INVITED = False

    handle = utils.check_handle(handle)
    u = GameInstance(handle, "yu_hun_leader")

    logging.info("执行御魂（队长）"+str(times)+"次")

    for i in range(times):
        logging.info("第" + str(i + 1) + "次")
        # 锁定阵容
        u.lock_lineup()
        # 点击挑战
        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(img_path("tiao_zhan"))
        u.random_click(p, 20)
        # sleep以减少消耗
        time.sleep(time_used_min)
        # 等待战斗结束
        logging.info("等待胜利")
        p = u.wait_until(img_path("sheng_li"),
                         timeout=time_used*2)
        # 胜利下方点击
        p = u.offset_position(p, (300, 300))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)
        # 点赞
        u.click_if_exists(u.img_path("dian_zan"))
        # 胜利下方点击
        p = u.offset_position(p, (300, 300))
        # 等待跳蛋
        u.random_click(p, 20)
        logging.info("等待跳蛋")
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
        u.random_sleep(1)
        try:
            p = u.wait_until(u.img_path("jia_ru_dui_wu"),
                             timeout=20,
                             interval=0.1, notify=False)
            if p is not None:
                logging.info("队员接受邀请")
                u.random_sleep(1)
        except TimeoutError:
            raise TimeoutError("未接受邀请")
