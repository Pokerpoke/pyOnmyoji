#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import logging
import json
from utils import *
import env


cur_path = os.path.join(env.get("game_workspace_path"), "onmyoji")


scene_conf = None
with open(os.path.join(cur_path, "scenes.json"), encoding="utf-8") as f:
    scene_conf = json.load(f)


def current_scene(handle=None):
    """
    获取当前场景，场景配置位于scenes.json。
    """
    global cur_path
    global scene_conf

    handle = check_handle(handle)

    for scene in scene_conf:
        if exists(os.path.join(cur_path, "img/" +
                               scene_conf[scene]["mark"] +
                               ".png"), handle=handle):
            if "chinese" in scene_conf[scene]:
                logging.info("当前场景：" +
                             scene_conf[scene]["chinese"])
            else:
                logging.info("当前场景："+scene)
            return scene
    return None
    # raise RuntimeError("Scene cannot be recognized.")


def goto_scene(s, handle=None):
    """
    进入场景，默认从当前场景返回庭院再次进入场景，场景配置位于scenes.json。
    """
    global cur_path
    global scene_conf

    handle = check_handle(handle)

    cur_scene = current_scene(handle=handle)
    if s == cur_scene:
        pass
    elif s == "ting_yuan":
        for next_scene in scene_conf[cur_scene]["to_ting_yuan"]:
            click_mark(next_scene, handle=handle)
            random_sleep(1.5, 0.2)
    elif cur_scene in scene_conf:
        goto_scene("ting_yuan", handle=handle)
        for next_scene in scene_conf[s]["route"]:
            if "0.98" in next_scene:
                click_mark(next_scene, threshold=0.98, handle=handle)
            else:
                click_mark(next_scene, handle=handle)
            random_sleep(1.5, 0.2)
    else:
        return None
        # raise RuntimeError("Scene cannot access.")


def click_mark(mark, handle=None, threshold=0.7, interval=1, timeout=10):
    """
    点击预设标志
    """
    global cur_path

    handle = check_handle(handle)

    p = wait_until(os.path.join(cur_path, "img/" +
                                mark + ".png"), threshold=threshold,
                   timeout=timeout, handle=handle)
    random_sleep(interval, 0.1)
    random_click(p, 10, handle=handle)


def lineup_locked(handle=None):
    """
    阵容锁定
    """
    global cur_path

    handle = check_handle(handle)

    if exists(os.path.join(cur_path, "img", "zhen_rong_suo_ding.png"), handle=handle):
        logging.debug("阵容已锁定")
        return True
    elif exists(os.path.join(cur_path, "img", "zhen_rong_wei_suo_ding.png"), handle=handle):
        logging.debug("阵容未锁定")
        return False
    else:
        logging.error("无法识别阵容锁定状态。")
        return None


def lock_lineup(handle=None):
    """
    锁定阵容
    """
    global cur_path

    handle = check_handle(handle)

    if not lineup_locked():
        click_if_exists(os.path.join(cur_path,
                                     "img", "zhen_rong_wei_suo_ding.png"), handle=handle)


def unlock_lineup(handle=None):
    """
    解锁阵容
    """
    global cur_path

    handle = check_handle(handle)

    if lineup_locked():
        click_if_exists(os.path.join(cur_path,
                                     "img", "zhen_rong_suo_ding.png"), handle=handle)


def set_current_mod(mod):
    """
    Set current running mod.
    """
    if mod is None:
        os.environ["CURRENT_MOD"] = "None"
    else:
        os.environ["CURRENT_MOD"] = mod


def win(timeout=10, handle=None, interval=1, threshold=0.7):
    global cur_path

    handle = check_handle(handle)

    return wait_until(os.path.join(cur_path, "img", "sheng_li"),
                      timeout=timeout, interval=interval,
                      notify=False, threshold=threshold, handle=handle)
