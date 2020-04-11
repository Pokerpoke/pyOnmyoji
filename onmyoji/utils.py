#!/usr/bin/python3
# -*- coding:utf-8 -*-

import win32api
import win32con
import win32gui
import win32ui
import cv2
import time
import random
import os
import numpy as np
import random
import logging
from PIL import Image


def get_title():
    return os.environ.get("YYS_TITLE")


def get_background():
    return os.environ.get("YYS_BACKGROUND")


class Pos(object):
    def __init__(self, x=0, y=0, w=0, h=0, i=0):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __radd__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __eq__(self, other):
        if other == None:
            return False
        elif self.x == other.x and self.y == other.y:
            return True
        else:
            return False


def move(p):
    win32api.SetCursorPos((p.x, p.y))


def click(p):
    background = get_background()
    if p == None:
        return

    if background == "True":
        window_handle = win32gui.FindWindow(None, get_title())

        pos_body = get_window_pos(window_handle)

        x = p.x - pos_body.x
        y = p.y - pos_body.y

        long_position = win32api.MAKELONG(x, y)  # 模拟鼠标指针 传送到指定坐标
        win32gui.SendMessage(
            window_handle, win32con.WM_MOUSEMOVE, 0, long_position)
        win32gui.PostMessage(
            window_handle, win32con.WM_LBUTTONDOWN, 0, long_position)  # 模拟鼠标按下
        time.sleep(random.randint(20, 80)/1000)
        win32gui.SendMessage(
            window_handle, win32con.WM_LBUTTONUP, 0, long_position)  # 模拟鼠标弹起
    else:
        x = p.x
        y = p.y

        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def find_window(title):
    handle = win32gui.FindWindow(None, title)
    return handle


def get_window_pos(window_handle):
    def get_window_rect(hwnd):
        import ctypes
        import ctypes.wintypes

        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(hwnd),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect))
            return rect.left, rect.top, rect.right, rect.bottom

    (x, y, w, h) = get_window_rect(window_handle)
    pos = Pos(x, y, w, h)

    return pos


def get_screenshot(title, filename=None):
    handle = find_window(get_title())
    hwndDC = win32gui.GetWindowDC(handle)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    pos = get_window_pos(handle)
    w = pos.width
    h = pos.height
    # 图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    if filename != None:
        saveBitMap.SaveBitmapFile(saveDC, filename)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im_PIL = Image.frombuffer('RGB',
                              (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                              bmpstr, 'raw', 'BGRX', 0, 1)
    res = cv2.cvtColor(np.asarray(im_PIL), cv2.COLOR_RGB2BGR)
    return res


def match(img_rgb, template_rgb, show_result=False):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    thresold = 0.7
    loc = np.where(res >= thresold)
    pos = []
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt,
                      (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        pos.append(Pos(pt[0], pt[1], w, h))
    if show_result:
        cv2.imshow('Match Result', img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return pos


def exists(template_path, timeout=10, interval=1, flag=0):
    if type(template) == str:
        template = cv2.imread(template)

    resource = get_screenshot(get_title())
    pos = match(resource, template)

    if len(pos) == 1:
        return pos
    elif len(pos) > 1:
        return pos[-1]
    else:
        return None


def wait_until(template, timeout=10, interval=1, flag=0):
    '''
    flag 0 -> center
    '''
    import time
    import random
    from datetime import datetime

    if type(template) == str:
        template = cv2.imread(template)

    pos_body = get_window_pos(find_window(get_title()))

    begin_time = datetime.now()
    while True:
        resource = get_screenshot(get_title())

        # print("Matching...")
        logging.info("Matching...")
        pos = match(resource, template)
        if len(pos) > 0:
            pos = pos[random.randint(0, len(pos) - 1)]

            # print("Matched")
            logging.info("Matched.")
            if flag == 0:
                p = Point(int(pos.x + 0.5 * pos.width),
                          int(pos.y + 0.5 * pos.height))
                p = Point(pos_body.x + p.x,
                          pos_body.y + p.y)
            return p

        end_time = datetime.now()
        time.sleep(interval)
        if (end_time - begin_time).seconds >= timeout:
            raise TimeoutError("Match process timeout.")

    return None


def offset_position(p, offset):
    if type(offset) == tuple:
        return p+Point(offset[0], offset[1])
    elif type(offset) == Point:
        return p+Point(offset.x, offset.y)


def random_position(p, offset):
    return p + Point(random.randint(-offset, offset),
                     random.randint(-offset, offset))


def random_time(t, offset):
    return t + random.uniform(-offset, offset)


def random_sleep(t, offset):
    return time.sleep(random_time(t, offset))


def random_click(p, offset):
    return click(random_position(p, offset))


def position_relative(x, y):
    pos_window = get_window_pos(find_window(get_title))
    p = Point(int(pos_window.x +
                  pos_window.width * x),
              int(pos_window.y +
                  pos_window.height * y))
    return p
