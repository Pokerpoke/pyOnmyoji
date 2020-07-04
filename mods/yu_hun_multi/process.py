import logging
from onmyoji import env
import onmyoji.utils as u
from onmyoji.game_instance import GameInstance
import mods.yu_hun_leader.process as leader
import mods.yu_hun_member.process as member
import threading


def main_process(times=5, time_used=35):
    h = env.get("game_leader_handle")
    l = GameInstance(h, "mod_test")
    h = env.get("game_member_handle")
    m = GameInstance(h, "mod_test")

    th1 = threading.Thread(target=leader.main_process,
                           args=(times, time_used, l.get_handle(),))
    th1.setDaemon(True)
    th1.start()
    th2 = threading.Thread(target=member.main_process,
                           args=(times, time_used, m.get_handle(),))
    th2.setDaemon(True)
    th2.start()
