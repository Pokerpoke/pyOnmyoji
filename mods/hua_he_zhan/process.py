import logging
import onmyoji.onmyoji_funcs as o
import onmyoji.utils as u
import threading
import mods.tan_suo.process as tan_suo
import mods.yu_hun.process as yu_hun
import mods.bai_gui_ye_xing.process as bai_gui
import mods.jue_xing.process as jue_xing


def main_process():
    cur_thread = threading.Thread(target=bai_gui.main_process, args=(1,))
    cur_thread.start()
    cur_thread.join()
    cur_thread = threading.Thread(target=yu_hun.main_process, args=(17,))
    cur_thread.start()
    cur_thread.join()
    cur_thread = threading.Thread(target=jue_xing.main_process, args=(13,))
    cur_thread.start()
    cur_thread.join()
    cur_thread = threading.Thread(target=tan_suo.main_process, args=(7,))
    cur_thread.start()
    cur_thread.join()
