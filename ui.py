#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import tkinter as tk
import os
import json
import importlib
import logging
import win32gui
import win32con
import threading
import inspect
import ctypes
from functools import partial
from onmyoji import utils as u
from gui import multi as m
from onmyoji import env


window = tk.Tk()
window.title("123")

CURRENT_MOD = None

var_background = tk.BooleanVar()
var_background.set(env.get("game_background") == True)

var_debug = tk.BooleanVar()
var_debug.set(True)


def set_debug():
    global var_debug
    global GAME_LOG_FILE

    if var_debug.get() == True:
        logging.basicConfig(
            format="[%(asctime)s]: %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(env.get("game_log_file_path")),
                logging.StreamHandler()
            ])
    else:
        logging.getLogger().setLevel(logging.INFO)


def init():
    set_debug()
    center_window(500, 700)

    # import paths
    mod_path = env.get("game_mods_path")
    sys.path.append(mod_path)
    mod_path = env.get("game_utils_path")
    sys.path.append(mod_path)


def center_window(w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def get_mods_list(path=env.get("game_mods_path")):
    def exclude_dir(dir_name):
        exclude_dirs = ["__pycache__", "mod_base.py"]
        if dir_name in exclude_dirs:
            return False
        else:
            return True

    return list(filter(exclude_dir, os.listdir(path)))


def generate_mods_button():
    mods = get_mods_list()

    row_idx = 0

    for mod_name in mods:
        mod_frame = tk.Frame(window)
        mod_frame.pack()

        info_path = os.path.join(
            env.get("game_mods_path"), mod_name, "package.json")

        mod = importlib.import_module("mods."+mod_name+".process")

        col_idx = 0
        with open(info_path, encoding='UTF-8') as f:
            mod_info = json.load(f)

        if "visible" in mod_info:
            if not mod_info["visible"]:
                continue

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
                                      entries, param_t, mod_name=mod_name
                                      )).grid(row=row_idx, column=col_idx)
        else:
            tk.Button(mod_frame, text="开始",
                      command=partial(mod.main_process)).grid(row=row_idx, column=col_idx)
        col_idx = col_idx + 1

        row_idx = row_idx + 1


def _async_raise(tid, exectype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exectype):
        exectype = type(exectype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exectype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def button_clicked(func, entries, param_t, mod_name):
    global CURRENT_MOD

    params = []
    for entry, t in zip(entries, param_t):
        if t == "int":
            params.append(int(entry.get()))
        elif t == "str":
            params.append(str(entry.get()))
        elif t == "float":
            params.append(float(entry.get()))

    CURRENT_MOD = threading.Thread(target=func, args=(*params,))
    CURRENT_MOD.setDaemon(True)
    CURRENT_MOD.start()


def set_background():
    global var_background

    if var_background.get():
        logging.info("Run in background.")
        env.push("game_background", True)
        # os.environ["GAME_BACKGROUND"] = "True"
    else:
        logging.info("Run in foreground.")
        env.push("game_background", False)
        # os.environ["GAME_BACKGROUND"] = "False"


def stop_current_mod():
    global CURRENT_MOD

    if CURRENT_MOD != None:
        stop_thread(thread=CURRENT_MOD)
        logging.info("Stopped.")
        CURRENT_MOD = None
    else:
        logging.info("No mod is running.")


def main():
    init()

    tk.Checkbutton(window, text="后台运行", variable=var_background,
                   command=set_background).pack()
    tk.Checkbutton(window, text="调试", variable=var_debug,
                   command=set_debug).pack()

    generate_mods_button()

    tk.Button(window, text="停止", command=stop_current_mod).pack()

    tk.Button(window, text="获取窗口句柄", command=m.get_handle).pack()


main()
# 进入消息循环
window.mainloop()
