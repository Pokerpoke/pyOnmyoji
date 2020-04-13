# -*- coding:utf-8 -*-

import os
import logging
from .utils import *


cur_path = os.path.join(os.environ.get("YYS_WORKSPACE_PATH"), "onmyoji")


def current_scene():
    '''
    0 - 庭院
    1 - 町中
    2 - tan suo
    '''
    global cur_path

    if exists(os.path.join(cur_path, "img/tan_suo_deng_long.png")):
        logging.info("Current sence is ting_yuan.")
        return "ting_yuan"
    elif exists(os.path.join(cur_path, "img/ting_yuan.png")):
        logging.info("Current sence is ting_zhong.")
        return "ting_zhong"
    elif exists(os.path.join(cur_path, "img/yao.png")):
        # use yao to match
        logging.info("Current sence is tan_suo.")
        return "tan_suo"
    else:
        return


def click_mark(mark):
    global cur_path

    p = exists(os.path.join(cur_path, "img/"+mark+".png"))
    random_click(p, 10)


def goto_scence(p):
    pass


def goto_ting_yuan():
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
