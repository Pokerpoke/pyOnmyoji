import logging
import os
from datetime import datetime
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o


def main_process(times=1):
    img_dir = os.path.join(__file__, "..", "img")

    logging.info("Will run for "+str(times)+" times.")

    INVITED_MAX = False
    INVITED = False

    if o.current_scene() is not None:
        o.goto_scene("bai_gui_ye_xing")

    for i in range(times):
        if not INVITED:
            if not INVITED_MAX:
                INVITED_MAX = False

                logging.info("运行:" + str(i + 1) + "次.")
                # 邀请好友
                logging.info("Search for yao_qing_hao_you.png.")
                p = u.wait_until(os.path.join(img_dir, "yao_qing_hao_you.png"))
                u.random_sleep(1, 0.5)
                u.random_click(p, 10)
                u.random_sleep(1, 0.5)
            # 选择好友
            logging.info("Search for xuan_ze_hao_you.png.")
            p = u.wait_until(os.path.join(
                img_dir, "xuan_ze_hao_you.png"),
                thresold=0.5)
            u.random_sleep(1, 0.5)
            u.random_click(p, 5)
            try:
                logging.info("Search for yao_qing_ci_shu_shang_xian.png.")
                p = u.wait_until(os.path.join(
                    img_dir, "yao_qing_ci_shu_shang_xian.png"), timeout=1, interval=0.1, notify=False)
                if p != None:
                    p = u.exists(os.path.join(
                        img_dir, "guan_bi_xuan_ze_hao_you.png"))
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
            p = u.wait_until(os.path.join(img_dir, "jin_ru.png"))
            u.random_sleep(1, 0.5)
            u.random_click(p, 20)
            u.random_sleep(1, 0.5)
            # 选择鬼王，选择中间的
            logging.info("Search for xuan_ze_gui_wang.png.")
            try:
                p = u.wait_until(os.path.join(
                    img_dir, "xuan_ze_gui_wang.png"), timeout=10)
            except TimeoutError:
                i = i - 1
                INVITED = True
                continue
        else:
            # 邀请
            logging.info("Search for qu_xiao_xuan_ze_hao_you.png.")
            p = u.wait_until(os.path.join(
                img_dir, "qu_xiao_xuan_ze_hao_you.png"))
            u.random_sleep(1, 0.5)
            u.random_click(p, 20)
            u.random_sleep(1, 0.5)
            i = i - 1
            INVITED = False
            continue

        u.random_sleep(1, 0.5)
        p = u.offset_position(p, (0, 300))
        u.random_click(p, 20)
        u.random_sleep(2, 0.5)
        # 开始
        logging.info("Search for kai_shi.png.")
        p = u.wait_until(os.path.join(img_dir, "kai_shi.png"))
        u.random_sleep(1, 0.5)
        u.random_click(p, 20)
        u.random_sleep(3, 0.5)
        # 砸豆子
        logging.info("Start piu piu piu.")
        begin_time = datetime.now()
        while (True):
            # 判断是否完成，前面一直点一定概率直接跳过分享界面了
            p = u.exists(os.path.join(img_dir, "feng_xiang.png"))
            if p != None:
                u.random_sleep(1, 0.2)
                p = u.position_relative(0.95, 0.55)
                u.random_click(p, 20)
                u.random_sleep(0.5, 0.2)
                break
            p = u.position_relative(0.8, 0.55)
            u.random_click(p, 20)
            u.random_sleep(0.5, 0.2)
            # 超时退出
            if (datetime.now() - begin_time).seconds >= 80:
                break

        u.random_sleep(3, 0.3)

    logging.info("Finished.")
