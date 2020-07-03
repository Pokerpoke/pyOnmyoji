import logging
from onmyoji import env
from onmyoji.game_instance import GameInstance
import mods.bai_gui_ye_xing.process as b
import threading


def main_process(times=3):
    h = env.get("game_leader_handle")
    l = GameInstance(h, "bai_gui_ye_xing_multi")
    h = env.get("game_member_handle")
    m = GameInstance(h, "bai_gui_ye_xing_multi")

    th1 = threading.Thread(target=b.main_process,
                           args=(times, l.get_handle(),))
    th1.setDaemon(True)
    th1.start()
    th2 = threading.Thread(target=b.main_process,
                           args=(times, m.get_handle(),))
    th2.setDaemon(True)
    th2.start()
