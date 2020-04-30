# -*- coding:utf-8 -*-

import os
import logging
from onmyoji.utils import *


cur_path = os.path.join(os.environ.get("GAME_WORKSPACE_PATH"), "onmyoji")


def current_scene():
    """
    庭院
    町中
    探索
    百鬼夜行
    御魂
    御灵
    """
    global cur_path

    if exists(os.path.join(cur_path, "img/tan_suo_deng_long.png")):
        logging.info("Current sence is ting_yuan.")
        return "ting_yuan"
    elif exists(os.path.join(cur_path, "img/bai_gui_ye_xing.png")):
        logging.info("Current sence is bai_gui_ye_xing.")
        return "bai_gui_ye_xing"
    elif exists(os.path.join(cur_path, "img/ting_yuan.png")):
        logging.info("Current sence is ting_zhong.")
        return "ting_zhong"
    elif exists(os.path.join(cur_path, "img/yao.png")):
        # use yao to match
        logging.info("Current sence is tan_suo.")
        return "tan_suo"
    else:
        return None


def click_mark(mark):
    global cur_path

    p = wait_until(os.path.join(cur_path, "img/"+mark+".png"))
    random_sleep(1, 0.2)
    random_click(p, 10)


def goto_scene(s):
    # @TODO: 用map重构，减少if的使用
    cur_scene = current_scene()
    if s == "ting_yuan":
        # 庭院
        if cur_scene == "ting_yuan":
            pass
        elif cur_scene == "ting_zhong":
            click_mark("ting_yuan")
            random_sleep(1, 0.2)
        elif cur_scene == "tan_suo":
            click_mark("fan_hui")
            random_sleep(1, 0.2)
        elif cur_scene == "bai_gui_ye_xing":
            click_mark("bai_gui_ye_xing_cha")
            random_sleep(1, 0.2)
            click_mark("ting_yuan")
            random_sleep(1, 0.2)
    elif s == "ting_zhong":
        # 町中
        if cur_scene == "ting_zhong":
            pass
        elif cur_scene == "ting_yuan":
            click_mark("ting_zhong")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("ting_zhong")
    elif s == "tan_suo":
        # 探索
        if cur_scene == "tan_suo":
            pass
        elif cur_scene == "ting_yuan":
            click_mark("tan_suo_deng_long")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("tan_suo")
    elif s == "bai_gui_ye_xing":
        # 百鬼夜行
        if cur_scene == "bai_gui_ye_xing":
            pass
        elif cur_scene == "ting_yuan":
            goto_scene("ting_zhong")
            click_mark("bai_gui_ye_xing_deng_long")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("bai_gui_ye_xing")
    elif s == "yu_hun":
        # 御魂
        if cur_scene == "yu_hun":
            pass
        elif cur_scene == "ting_yuan":
            goto_scene("tan_suo")
            click_mark("yu_hun")
            random_sleep(1, 0.2)
            click_mark("yu_hun_ba_qi_da_she")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("yu_hun")
    elif s == "ye_yuan_huo":
        # 业原火
        if cur_scene == "yu_hun":
            pass
        elif cur_scene == "ting_yuan":
            goto_scene("tan_suo")
            click_mark("yu_hun")
            random_sleep(1, 0.2)
            click_mark("ye_yuan_huo")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("ye_yuan_huo")
    elif s == "ri_lun_zhi_yun":
        # 日轮之陨
        if cur_scene == "yu_hun":
            pass
        elif cur_scene == "ting_yuan":
            goto_scene("tan_suo")
            click_mark("yu_hun")
            random_sleep(1, 0.2)
            click_mark("ri_lun_zhi_yun")
            random_sleep(1, 0.2)
        else:
            goto_scene("ting_yuan")
            goto_scene("ri_lun_zhi_yun")

    else:
        logging.error("Wrong scene.")


def goto_ting_yuan():
    pass


def lineup_locked():
    pass


def goto_tan_suo():
    scene = current_scene()
    if scene == "ting_yuan":
        click_mark("tan_suo_deng_long")
    elif scene == "ting_zhong":
        click_mark("ting_yuan")
    elif scene == "tan_suo":
        pass
    else:
        return


def set_current_mod(mod):
    """
    Set current running mod.
    """
    if mod is None:
        os.environ["CURRENT_MOD"] = "None"
    else:
        os.environ["CURRENT_MOD"] = mod
