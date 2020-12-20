import logging
import os
from datetime import datetime
import onmyoji.utils as utils
from onmyoji.game_instance import GameInstance


def img_path(img_name):
    path = os.path.join(__file__, "..", "img", img_name+".png")
    return path


def main_process(times=1, handle=None):

    handle = utils.check_handle(handle)

    u = GameInstance(handle, "bai_gui_ye_xing")

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("将运行："+str(times)+"次")

    INVITED_MAX = False
    INVITED = False

    if u.current_scene() is not None:
        u.goto_scene("bai_gui_ye_xing")

    for i in range(times):
        if not INVITED:
            if not INVITED_MAX:
                INVITED_MAX = False

                logging.info("第" + str(i + 1) + "次")
                # 邀请好友
                logging.info("匹配 yao_qing_hao_you.png.")
                p = u.wait_until(img_path("yao_qing_hao_you"))
                u.random_sleep(1, 0.5)
                u.random_click(p, 10)
                u.random_sleep(1, 0.5)
            # 选择好友
            logging.info("匹配 xuan_ze_hao_you.png.")
            p = u.wait_until(os.path.join(
                img_dir, "xuan_ze_hao_you.png"),
                threshold=0.5)
            u.random_sleep(1, 0.5)
            u.random_click(p, 5)
            try:
                # 邀请次数上限
                logging.info("Search for yao_qing_ci_shu_shang_xian.png.")
                p = u.wait_until(img_path("yao_qing_ci_shu_shang_xian"),
                                 timeout=2, interval=0.1, notify=False)
                if p is not None:
                    p = u.exists(img_path("guan_bi_xuan_ze_hao_you"))
                    p = u.offset_position(p, (0, 200))
                    u.random_sleep(1, 0.5)
                    u.random_click(p, 5)
                    u.random_sleep(1, 0.5)
                    INVITED_MAX = True
                    i = i - 1
                    continue
            except TimeoutError:
                pass
            # 进入
            logging.info("Search for jin_ru.png.")
            p = u.wait_until(img_path("jin_ru"))
            u.random_sleep(1, 0.5)
            u.random_click(p, 20)
            try:
                # 邀请次数上限
                logging.info("Search for yao_qing_ci_shu_shang_xian.png.")
                p = u.wait_until(img_path("yao_qing_ci_shu_shang_xian"),
                                 timeout=2, interval=0.1, notify=False)
                if p is not None:
                    p = u.exists(img_path("guan_bi_xuan_ze_hao_you"))
                    p = u.offset_position(p, (0, 200))
                    u.random_sleep(1, 0.5)
                    u.random_click(p, 5)
                    u.random_sleep(1, 0.5)
                    INVITED_MAX = True
                    INVITED = True
                    i = i - 1
                    continue
            except TimeoutError:
                pass
            u.random_sleep(1, 0.5)
            # 选择鬼王，选择中间的
            logging.info("Search for xuan_ze_gui_wang.png.")
            try:
                p = u.wait_until(img_path("xuan_ze_gui_wang"), timeout=10)
            except TimeoutError:
                i = i - 1
                INVITED = True
                continue
            # 点击中间的鬼王
            u.random_sleep(1, 0.5)
            p = u.offset_position(p, (0, 300))
            u.random_click(p, 20)
            u.random_sleep(2, 0.5)
        else:
            # 邀请
            logging.info("Search for qu_xiao_xuan_ze_hao_you.png.")
            p = u.wait_until(img_path("qu_xiao_xuan_ze_hao_you"))
            u.random_sleep(1, 0.5)
            u.random_click(p, 20)
            u.random_sleep(1, 0.5)
            i = i - 1
            INVITED = False
            continue

        # 开始
        logging.info("Search for kai_shi.png.")
        p = u.wait_until(img_path("kai_shi"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        u.random_sleep(3, 0.5)
        # 砸豆子
        logging.info("开始砸豆子。")
        begin_time = datetime.now()
        while (True):
            # 判断是否完成，前面一直点一定概率直接跳过分享界面了
            p = u.exists(img_path("feng_xiang"))
            if p != None:
                u.random_sleep(1, 0.2)
                p = u.position_relative(0.95, 0.55)
                u.random_click(p, 20)
                u.random_sleep(0.5, 0.2)

                logging.info("砸完了")
                break
            # 存在豆子获取
            p = u.exists(img_path("dou_zi_huo_qu"))
            if p is not None:
                p = u.offset_position(p, (-30, -20))
                u.random_click(p, 5)
                u.random_sleep(0.5, 0.2)
            # 概率up
            p = u.exists(img_path("gai_lv_up"))
            if p is not None:
                p = u.offset_position(p, (-30, -20))
                u.random_click(p, 5)
                u.random_sleep(0.5, 0.2)
            # 好友概率up
            p = u.exists(img_path("hao_you_gai_lv_up"))
            if p is not None:
                p = u.offset_position(p, (-30, -20))
                u.random_click(p, 5)
                u.random_sleep(0.5, 0.2)
            # 优先砸带灯笼的
            p = u.exists(img_path("deng_long"))
            if p is not None:
                # 大概由于识别速度慢，要增加一定偏移才能砸到正下方
                p = u.offset_position(p, (-100, 100))
                u.random_click(p, 20)
                u.random_sleep(0.5, 0.2)
            else:
                p = u.position_relative(0.8, 0.55)
                u.random_click(p, 20)
                u.random_sleep(0.5, 0.2)
            # 分享界面出现以后一定概率直接跳过，检测到进入即视为当次完成
            if u.exists(img_path("jin_ru")):
                logging.info("砸完了")
                break
            # 超时退出
            if (datetime.now() - begin_time).seconds >= 100:
                logging.info("超时退出")
                break

        u.random_sleep(3, 0.3)

    logging.info("Finished.")
