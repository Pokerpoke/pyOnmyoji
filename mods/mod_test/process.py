import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
from onmyoji import env
from onmyoji.game_instance import GameInstance


def main_process(thresold=0.7, type=0):
    h = env.get("game_leader_handle")
    l = GameInstance(h, "mod_test")
    h = env.get("game_member_handle")
    m = GameInstance(h, "mod_test")

    l.click_if_exists(l.img_path("template"))

    m.click_if_exists(m.img_path("template"))
