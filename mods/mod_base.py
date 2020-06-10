import sys
import os
import time
import importlib
import onmyoji.utils as u
import logging
import huan_gou_liang.process
from onmyoji import onmyoji_funcs
from threading import Thread
from onmyoji import env


class GameMod(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.finished_ = False
        self.name_ = name

    def img_path(self, img_name):
        path = os.path.join(env.get("game_mods_path"),
                            self.name_, "img", img_name+".png")
        return path

    def main_process(self):
        pass

    def finished(self):
        pass
