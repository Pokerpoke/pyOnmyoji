from onmyoji.game_instance import GameInstance
from onmyoji import env
import cv2

import onmyoji.utils as u


def main_process(threhold=0.7):

    leader_handle = env.get("game_leader_handle")
    print(leader_handle)
    u.get_screenshot(leader_handle, show=True)
    print(1)

    l = GameInstance(leader_handle, "match_test")
    res = l.get_screenshot(show=True)
    print(1)

    print(l.img_path("template"))
    template = cv2.imread(l.img_path("template"))
    l.match(res, template, show_result=True)
