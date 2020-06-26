#!/usr/bin/python3
# -*- coding:utf-8 -*-

from onmyoji import env
import onmyoji.utils as u
from functools import partial
import os


class GameInstance():
    def __init__(self, handle, mod_name=None):
        self.handle_ = handle
        self.mod_name_ = mod_name
        # 绑定参数
        self.slide = partial(u.slide, handle=self.handle_)
        self.click = partial(u.click, handle=self.handle_)
        self.get_screenshot = partial(u.get_screenshot, handle=self.handle_)
        self.exists = partial(u.exists, handle=self.handle_)
        self.wait_until = partial(u.wait_until, handle=self.handle_)
        self.click_if_exists = partial(u.click_if_exists, handle=self.handle_)
        self.move = partial(u.move)
        self.match = u.match

    def get_handle(self):
        return self.handle_

    def img_path(self, img_name):
        if self.mod_name_ is None:
            return None
        mods_path = env.get("game_mods_path")
        return os.path.join(mods_path, self.mod_name_, "img", img_name+".png")
