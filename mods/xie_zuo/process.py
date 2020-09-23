import os
import logging
from threading import Event
import onmyoji.utils as u
from onmyoji import env
from onmyoji.game_instance import GameInstance

STOP = Event()


def stop():
    global STOP

    if STOP.is_set():
        logging.info("协作已经停止。")
    else:
        logging.info("停止协作。")
        STOP.set()


def main_process(accept=True, times=1, time_used=7):
    global STOP

    STOP.clear()
    STOP.set()

    img_dir = os.path.join(__file__, "..", "img")

    accept_path = os.path.join(img_dir, "accept.png")
    reject_path = os.path.join(img_dir, "reject.png")

    while (True):
        if not env.get("game_multi"):
            if accept:
                u.click_if_exists(accept_path, thresold=0.9)
            else:
                u.click_if_exists(reject_path, thresold=0.9)
            u.random_sleep(1, 0.2)
        else:
            l = GameInstance(env.get("game_leader_handle"), "xie_zuo")
            m = GameInstance(env.get("game_member_handle"), "xie_zuo")
            if accept:
                l.click_if_exists(accept_path, thresold=0.9)
                m.click_if_exists(accept_path, thresold=0.9)
            else:
                l.click_if_exists(reject_path, thresold=0.9)
                m.click_if_exists(reject_path, thresold=0.9)
            u.random_sleep(1, 0.2)
        if STOP.is_set():
            break
