import sys
import os
import time
import onmyoji.utils as utils
from onmyoji.game_instance import GameInstance
import logging
from datetime import datetime
import mods.bonus.process as bonus


def main_process(times=1, time_used=35, handle=None):
    handle = utils.check_handle(handle)
    u = GameInstance(handle, "yu_hun_member")

    # 最短时间，控制sleep以降低消耗
    time_used_min = 18

    logging.info("执行御魂（队员）"+str(times)+"次")

    INVITE_LOCKED = False

    # logging.info("开启加成")
    # bonus.main_process("yu_hun")

    for i in range(times):
        logging.info("第" + str(i + 1) + "次")

        # if not INVITE_LOCKED:
        #     if u.current_scene() != "xie_zhan_dui_wu":
        #         logging.info("等待接受邀请")
        #         start = datetime.now()
        #         while (True):
        #             logging.info("111")

        #             if u.click_if_exists(u.img_path("suo_ding_jie_shou_yao_qing"), interval=1):
        #                 logging.info("锁定接受邀请")
        #                 INVITE_LOCKED = True
        #                 time.sleep(0.2)
        #                 break

        #             if u.click_if_exists(u.img_path("jie_shou_yao_qing"),
        #                                  interval=1):
        #                 logging.info("接受邀请")
        #                 INVITE_LOCKED = False
        #                 time.sleep(0.2)
        #                 break

        #             end = datetime.now()
        #             if (end - start).seconds > 300:
        #                 logging.error("等待接受邀请超时，请重新启动")
        #                 return

        time.sleep(1)

        u.lock_lineup()
        time.sleep(time_used_min)

        logging.info("等待胜利")
        p = u.wait_until(u.img_path("sheng_li"),
                         timeout=time_used*2)
        u.random_sleep(1, 0.3)

        # 点赞
        u.click_if_exists(u.img_path("dian_zan"))
        # 胜利下方点击
        p = u.offset_position(p, (300, 300))
        u.random_click(p, 20)
        # 等待跳蛋
        logging.info("等待跳蛋")
        p = u.wait_until(u.img_path("jie_suan"))
        u.random_sleep(2, 0.3)
        p = u.offset_position(p, (300, 0))
        u.random_click(p, 20)

        u.random_sleep(3, 0.3)

        if not INVITE_LOCKED:
            logging.info("接受邀请")
            start = datetime.now()
            while (True):
                if u.click_if_exists(u.img_path("suo_ding_jie_shou_yao_qing"), interval=1):
                    logging.info("锁定接受邀请")
                    INVITE_LOCKED = True
                    time.sleep(0.2)
                    break

                if u.click_if_exists(u.img_path("jie_shou_yao_qing"),
                                     interval=1):
                    logging.info("接受邀请")
                    INVITE_LOCKED = False
                    time.sleep(0.2)
                    break

                end = datetime.now()
                if (end - start).seconds > 5:
                    logging.error("等待接受邀请超时，请重新启动")
                    return

    # logging.info("关闭加成")
    # bonus.main_process("yu_hun")

    logging.info(str(times)+"次御魂（队员）完成")
