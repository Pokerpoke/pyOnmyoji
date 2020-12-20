from onmyoji.game_instance import GameInstance
from onmyoji import env
import cv2

import onmyoji.utils as u


def main_process(threshold=0.7):
    if env.get("game_multi"):
        leader_handle = env.get("game_leader_handle")
        member_handle = env.get("game_member_handle")

        l = GameInstance(leader_handle, "match_test")
        m = GameInstance(member_handle, "match_test")

        template = cv2.imread(l.img_path("template"))

        l.match(l.get_screenshot(), template, show_result=True)
        m.match(m.get_screenshot(), template, show_result=True)
    else:
        h = env.get("game_default_handle")
        g = GameInstance(h, "match_test")

        template = cv2.imread(g.img_path("template"))

        g.match(g.get_screenshot(), template,
                threshold=threshold, show_result=True)
