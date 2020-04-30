import os
import logging
from threading import Event
import onmyoji.utils as u

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

    img_dir = os.path.join(__file__, "..", "img")

    accept_path = os.path.join(img_dir, "accept.png")
    reject_path = os.path.join(img_dir, "reject.png")

    while (True):
        if accept:
            u.click_if_exists(accept_path)
        else:
            u.click_if_exists(reject_path)
        u.random_sleep(1, 0.2)
        if STOP.is_set():
            break
