#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import onmyoji.utils as u
import threading

from onmyoji import env

MULTI_CURRENT_HANDLE = None

MULTI_LEADER_HANDLE = None
MULTI_MEMBER_HANDLE = None


def get_current_handle():
    global MULTI_CURRENT_HANDLE

    t = u.OnmyojiThread(target=u.get_cursor_window_handle)
    t.start()
    t.join()
    res = t.get_ret()
    MULTI_CURRENT_HANDLE = res


def get_leader_handle():
    global MULTI_LEADER_HANDLE

    t = u.OnmyojiThread(target=u.get_cursor_window_handle)
    t.start()
    t.join()
    res = t.get_ret()
    env.set("game_leader_handle", res)
    MULTI_LEADER_HANDLE = res


def get_member_handle():
    global MULTI_MEMBER_HANDLE

    t = u.OnmyojiThread(target=u.get_cursor_window_handle)
    t.start()
    t.join()
    res = t.get_ret()
    env.set("game_member_handle", res)
    MULTI_MEMBER_HANDLE = res


def get_handles():
    global MULTI_CURRENT_HANDLE

    multi_windows = tk.Tk()
    multi_windows.title("获取窗口句柄")

    ws = multi_windows.winfo_screenwidth()
    hs = multi_windows.winfo_screenheight()

    w = 200
    h = 200

    x = (ws/2)-(w/2)
    y = (hs/2)-(h/2)

    multi_windows.geometry("%dx%d+%d+%d" % (w, h, x, y))

    multi_windows.wm_attributes("-topmost", 1)

    l = tk.Label(multi_windows, textvariable=MULTI_CURRENT_HANDLE)
    l.grid(row=1, column=2)

    b_handle_cur = tk.Button(multi_windows, text="获取句柄",
                             command=get_current_handle)
    b_handle_cur.grid(row=2, column=1)

    b_handle_leader = tk.Button(multi_windows, text="获取队长句柄",
                                command=get_leader_handle)
    b_handle_leader.grid(row=3, column=1)

    b_handle_member = tk.Button(multi_windows, text="获取队员句柄",
                                command=get_member_handle)
    b_handle_member.grid(row=4, column=1)

    close = tk.Button(multi_windows, text="关闭", command=multi_windows.destroy)
    close.grid(row=5, column=1)

    multi_windows.mainloop()
