# -*- coding: UTF-8 -*-

# import mods.juexing.process as jx
import mods.match_test.process
import tkinter as tk
import tkinter.messagebox
import onmyoji
import os

window = tk.Tk()
window.title("Onmyoji Assert")

WORKSPACE_PATH = os.getcwd()
MODS_PATH = os.path.join(WORKSPACE_PATH, "mods")

os.environ["WORKSPACE_PATH"] = WORKSPACE_PATH
os.environ["MODS_PATH"] = MODS_PATH


def center_window(w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


center_window(500, 500)


def hello():
    onmyoji.base_process("baiguiyexing", 1)
    # tk.messagebox.showinfo(title="Hello")


button_baiguiyexing = tk.Button(window, text="百鬼夜行", command=hello)
button_baiguiyexing.pack()


def match_test():
    mods.match_test.process.main_process(1)


button_match_test = tk.Button(window, text="match", command=match_test)
button_match_test.pack()

# 进入消息循环
window.mainloop()
