from onmyoji.game_instance import GameInstance
from onmyoji import env
import cv2

import onmyoji.utils as u


def main_process(threhold=0.7):

    leader_handle = env.get("game_leader_handle")
    member_handle = env.get("game_member_handle")

    l = GameInstance(leader_handle, "match_test")
    m = GameInstance(member_handle, "match_test")

    template = cv2.imread(l.img_path("template"))

    l.match(l.get_screenshot(), template, show_result=True)
    m.match(m.get_screenshot(), template, show_result=True)
