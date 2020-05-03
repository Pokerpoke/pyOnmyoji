import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
import mods.tan_suo.process as tan_suo
import mods.yu_hun.process as yu_hun
import mods.bai_gui_ye_xing.process as bai_gui
import mods.jue_xing.process as jue_xing


def main_process():
    bai_gui.main_process(times=1)
    yu_hun.main_process(times=17)
    jue_xing.main_process(times=13)
    tan_suo.main_process(times=7)
