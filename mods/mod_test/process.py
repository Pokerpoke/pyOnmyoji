import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
import mods.bonus.process as b
import mods.mod_base as mod_base


class mod_test(mod_base.GameMod):
    def main_process(self):
        print(self.img_path("kai_qi"))


def main_process(thresold=0.7, type=0):
    # o.goto_scene("kun_28")
    # u.random_sleep(1, 0.2)
    # o.goto_scene("ting_yuan")
    # u.random_sleep(1, 0.2)
    # o.goto_scene("lei_qi_lin")
    # print(b.main_process(
    #     bonus=["yu_hun", "jue_xing", "jing_yan_50", "jing_yan_100"]))
    # o.lock_lineup()
    # u.random_sleep(1, 0.2)
    # o.unlock_lineup()
    # o.goto_scene("lei_qi_lin")
    # u.get_cursor_window_handle()
    # print(o.lineup_locked())
    # o.goto_scene("jie_jie_ka_he_cheng")
    pass
