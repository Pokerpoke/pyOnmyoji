#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import onmyoji.utils as u
import threading

window = tk.Tk()
window.title("UI")
window.geometry("300x100")

var = tk.StringVar()
var.set("窗口句柄：None")
window.wm_attributes("-topmost", 1)


def get_handle(str="窗口句柄："):
    global var

    t = u.OnmyojiThread(target=u.get_cursor_window_handle)
    t.start()
    t.join()
    res = t.get_ret()
    var.set("窗口句柄："+str(res))


def multi_get_handle():
    global var

    l = tk.Label(window, textvariable=var)
    l.grid(row=1, column=2)

    b_handle = tk.Button(window, text="获取句柄", command=get_handle)
    b_handle.grid(row=2, column=1)

    close = tk.Button(window, text="关闭", command=window.destroy)
    close.grid(row=2, column=2)

    window.mainloop()
