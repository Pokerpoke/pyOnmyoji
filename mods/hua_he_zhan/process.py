import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
import mods.tan_suo as tan_suo
import mods.yu_hun as yu_hun
import mods.bai_gui_ye_xing as bai_gui


def main_process(thresold=0.7, type=0):
    bai_gui.process.main_process(times=1)
    yu_hun.process.main_process(times=17)
    tan_suo.process.main_process(times=7)
