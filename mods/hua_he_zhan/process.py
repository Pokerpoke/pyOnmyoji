import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
import threading
import os
import mods.kun_28.process as kun_28
import mods.yu_hun.process as yu_hun
import mods.bai_gui_ye_xing.process as bai_gui
import mods.jue_xing.process as jue_xing


def main_process():
    img_dir = os.path.join(__file__, "..", "img")
    # 百鬼夜行
    # cur_thread = threading.Thread(target=bai_gui.main_process, args=(1,))
    # cur_thread.start()
    # cur_thread.join()
    # 御魂
    cur_thread = threading.Thread(target=yu_hun.main_process, args=(17,))
    cur_thread.start()
    cur_thread.join()
    # 觉醒
    cur_thread = threading.Thread(target=jue_xing.main_process, args=(13,))
    cur_thread.start()
    cur_thread.join()
    # 困28
    cur_thread = threading.Thread(target=kun_28.main_process, args=(7,))
    cur_thread.start()
    cur_thread.join()

    # 领取奖励
    o.goto_scene("hua_he_zhan")
    u.random_sleep(1)
    o.click_if_exists(os.path.join(img_dir, "quan_bu_ling_qu.png"))

    p = o.wait_until(os.path.join(img_dir, "huo_de_jiang_li.png"))
    if p is not None:
        u.random_sleep(1)
        p = u.offset_position(p, (300, 0))
        u.random_click(p, 20)

    # 返回庭院
    o.goto_scene("ting_yuan")

    logging.info("花合战完成")

    u.toast("花合战完成")
