#!/usr/bin/python3
# -*- coding:utf-8 -*-

from onmyoji import env
import onmyoji.utils as u
import onmyoji.onmyoji_funcs as o
from functools import partial
import os


class GameInstance():
    def __init__(self, handle, mod_name=None):
        self.handle_ = handle
        self.mod_name_ = mod_name
        # 绑定参数
        # onmyoji.utils
        self.slide = partial(u.slide, handle=self.handle_)
        self.click = partial(u.click, handle=self.handle_)
        self.get_screenshot = partial(u.get_screenshot, handle=self.handle_)
        self.exists = partial(u.exists, handle=self.handle_)
        self.wait_until = partial(u.wait_until, handle=self.handle_)
        self.click_if_exists = partial(u.click_if_exists, handle=self.handle_)
        self.move = u.move
        self.random_click = partial(u.random_click, handle=self.handle_)
        self.position_relative = partial(
            u.position_relative, handle=self.handle_)
        self.set_foreround_window = partial(
            u.set_foreround_window, handle=self.handle_)
        self.random_sleep = u.random_sleep
        self.distance = u.distance
        self.offset_position = u.offset_position
        self.random_position = u.random_position
        self.random_time = u.random_time
        self.toast = u.toast
        self.match = u.match
        # onmyoji_funcs
        self.current_scene = partial(o.current_scene, handle=self.handle_)
        self.goto_scene = partial(o.goto_scene, handle=self.handle_)
        self.click_mark = partial(o.click_mark, handle=self.handle_)
        self.lineup_locked = partial(o.lineup_locked, handle=self.handle_)
        self.lock_lineup = partial(o.lock_lineup, handle=self.handle_)
        self.unlock_lineup = partial(o.unlock_lineup, handle=self.handle_)
        self.win = partial(o.win, handle=self.handle_)

    def get_handle(self):
        return self.handle_

    def img_path(self, img_name):
        if self.mod_name_ is None:
            return None
        mods_path = env.get("game_mods_path")
        return os.path.join(mods_path, self.mod_name_, "img", img_name+".png")
