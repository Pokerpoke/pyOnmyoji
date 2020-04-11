# -*- coding: UTF-8 -*-

import tkinter as tk
import tkinter.messagebox
import onmyoji
import os
import json
import importlib
import logging
from functools import partial
from onmyoji import utils as u
import win32gui
import win32con

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

window = tk.Tk()
window.title("Onmyoji Assert")

YYS_TITLE = "阴阳师-网易游戏"
YYS_WORKSPACE_PATH = os.getcwd()
YYS_MODS_PATH = os.path.join(YYS_WORKSPACE_PATH, "mods")
YYS_BACKGROUND = "True"
# YYS_BACKGROUND = "False"

os.environ["YYS_WORKSPACE_PATH"] = YYS_WORKSPACE_PATH
os.environ["YYS_MODS_PATH"] = YYS_MODS_PATH
os.environ["YYS_TITLE"] = YYS_TITLE
os.environ["YYS_BACKGROUND"] = YYS_BACKGROUND


def init():
    if YYS_BACKGROUND == "False":
        handle = u.find_window(YYS_TITLE)
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(handle)
        pos_window = u.get_window_pos(handle)


def center_window(w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def get_mods_list(path=YYS_MODS_PATH):
    return os.listdir(path)


def generate_mods_button():
    mods = get_mods_list()

    row_idx = 0

    for mod_name in mods:
        mod_frame = tk.Frame(window)
        mod_frame.pack()

        info_path = os.path.join(YYS_MODS_PATH, mod_name, "package.json")

        mod = importlib.import_module("mods."+mod_name+".process")

        col_idx = 0
        with open(info_path, encoding='UTF-8') as f:
            mod_info = json.load(f)

        if "text" in mod_info:
            tk.Label(mod_frame, text=mod_info["text"]).grid(
                row=row_idx, column=col_idx)
        else:
            tk.Label(mod_frame, text=mod_name).grid(
                row=row_idx, column=col_idx)

        col_idx = col_idx+1

        if "params" in mod_info:
            entries = []
            param_t = []
            for param in mod_info["params"]:
                if "text" in param:
                    tk.Label(mod_frame, text=param["text"]).grid(
                        row=row_idx, column=col_idx)
                else:
                    tk.Label(mod_frame, text=param["param"]).grid(
                        row=row_idx, column=col_idx)
                col_idx = col_idx + 1

                entry = tk.Entry(mod_frame)
                entries.append(entry)
                entry.grid(row=row_idx, column=col_idx)

                if "default" in param:
                    entry.insert(0, str(param["default"]))
                col_idx = col_idx+1

                if "param_t" in param:
                    param_t.append(param["param_t"])

            tk.Button(mod_frame, text="开始",
                      command=partial(button_clicked, mod.main_process,
                                      entries, param_t
                                      )).grid(row=row_idx, column=col_idx)
        else:
            tk.Button(mod_frame, text="开始",
                      command=partial(mod.main_process)).grid(row=row_idx, column=col_idx)
        col_idx = col_idx + 1

        row_idx = row_idx + 1


def button_clicked(func, entries, param_t):
    params = []
    for entry, t in zip(entries, param_t):
        if t == "int":
            params.append(int(entry.get()))
        elif t == "str":
            params.append(str(entry.get()))
    func(*params)


def main():
    init()

    center_window(500, 500)

    generate_mods_button()


main()
# 进入消息循环
window.mainloop()
