import logging
from onmyoji import env
import onmyoji.utils as u
from onmyoji.game_instance import GameInstance
import threading


def main_process(times=30, time_used=7):
    h = env.get("game_default_handle")
    g = GameInstance(h, "general")

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")

        logging.info("Search for tiao_zhan.png.")
        p = g.wait_until(g.img_path("tiao_zhan"), timeout=time_used)
        g.random_sleep(1)
        g.random_click(p, 10)

        p = g.wait_until(g.img_path("sheng_li"), timeout=time_used*5)
        p = u.offset_position(p, (300, 300))
        u.random_sleep(1, 0.3)
        u.random_click(p, 20)

        p = g.wait_until(g.img_path("jie_suan"), timeout=time_used)
        u.random_sleep(2, 0.3)
        u.random_click(p, 20)
