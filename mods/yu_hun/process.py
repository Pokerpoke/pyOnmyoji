import sys
import os
import time
import logging
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o
import mods.bonus.process as bonus


def main_process(times=1, time_used=35, floor=11):

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("即将运行"+str(times)+"次")

    # 进入御魂界面
    o.goto_scene("yu_hun_"+str(floor))

    # 切换加成状态
    bonus.main_process("yu_hun")

    for i in range(times):
        logging.info("第" + str(i + 1) + "次")
        # 阵容锁定
        LINEUP_LOCKED = o.lineup_locked()
        # 点击挑战按钮
        logging.info("Search for tiao_zhan.png.")
        p = u.wait_until(os.path.join(img_dir, "tiao_zhan.png"))
        u.random_click(p, 20)
        u.random_sleep(1, 0.3)
        # 阵容未锁定，点击准备
        if not LINEUP_LOCKED:
            o.click_mark("zhun_bei", interval=3)
        u.random_sleep(time_used+3, 0.3)
        # 等待打完，判断胜利
        logging.info("Search for sheng_li.png.")
        p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                         timeout=time_used)
        u.random_sleep(1, 0.1)
        u.random_click(p, 20)
        # 点击红蛋
        logging.info("Search for jie_suan.png.")
        p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
        u.random_sleep(1, 0.1)
        u.random_click(p, 20)
        # 等待加载
        u.random_sleep(3, 0.3)

    # 切换加成状态
    bonus.main_process("yu_hun")

    logging.info(str(times)+"次御魂（单人）完成")
