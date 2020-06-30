import logging
from onmyoji import env
import onmyoji.utils as u
from onmyoji.game_instance import GameInstance
import mods.bai_gui_ye_xing.process as b
import threading


def main_process(thresold=0.7, type=0):
    h = env.get("game_leader_handle")
    l = GameInstance(h, "mod_test")
    h = env.get("game_member_handle")
    m = GameInstance(h, "mod_test")

    l.get_screenshot(filename="leader.png")
    m.get_screenshot(filename="member.png")

    th1 = threading.Thread(target=b.main_process, args=(5, l.get_handle(),))
    th1.setDaemon(True)
    th1.start()
    m.random_sleep(1)
    th2 = threading.Thread(target=b.main_process, args=(3, m.get_handle(),))
    th2.setDaemon(True)
    th2.start()
