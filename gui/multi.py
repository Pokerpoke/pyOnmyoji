#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import onmyoji.utils as u
import threading

# window = tk.Tk()
# window.title("UI")
# window.geometry("300x100")

# top = tk.Toplevel()

# var = tk.StringVar()
# var.set("窗口句柄：None")
# top.wm_attributes("-topmost", 1)

MULTI_CURRENT_HANDLE = None


def get_handle_thread(str="窗口句柄："):
    global MULTI_CURRENT_HANDLE

    t = u.OnmyojiThread(target=u.get_cursor_window_handle)
    t.start()
    t.join()
    res = t.get_ret()
    MULTI_CURRENT_HANDLE = res


def get_handle():
    global MULTI_CURRENT_HANDLE

    top = tk.Tk()
    top.title("获取窗口句柄")
    top.geometry("300x100")

    top.wm_attributes("-topmost", 1)

    l = tk.Label(top, textvariable=MULTI_CURRENT_HANDLE)
    l.grid(row=1, column=2)

    b_handle = tk.Button(top, text="获取句柄", command=get_handle_thread)
    b_handle.grid(row=2, column=1)

    close = tk.Button(top, text="关闭", command=top.destroy)
    close.grid(row=2, column=2)

    top.mainloop()
