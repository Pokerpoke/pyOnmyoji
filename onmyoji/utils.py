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
import math
import logging
from datetime import datetime
from PIL import Image
from win10toast import ToastNotifier
from threading import Thread


class OnmyojiThread(Thread):
    def __init__(self, target):
        Thread.__init__(self)
        self.ret_val = None
        self.thread_ = target

    def run(self):
        self.ret_val = self.thread_()

    def get_ret(self):
        return self.ret_val


def get_title():
    return os.environ.get("GAME_TITLE")


def get_background():
    return os.environ.get("GAME_BACKGROUND") == "True"


def get_cursor_window_handle():
    # Left button down = 0 or 1. Button up = -127 or -128
    state_left = win32api.GetKeyState(0x01)
    # Right button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)

    p = None
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                logging.debug("左键按下")
                (x, y) = win32api.GetCursorPos()
                p = Point(x, y)
                break
            else:
                logging.debug("左键释放")
        if b != state_right:  # Button state changed
            state_right = b
            if b < 0:
                logging.debug("右键按下")
            else:
                logging.debug("右键释放")
        time.sleep(0.001)
    handle = win32gui.WindowFromPoint((p.x, p.y))
    logging.info("当前窗口句柄："+str(handle))
    return handle


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

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


def move(p, continuous=False, interval=0.1):
    if continuous:
        pass
    else:
        win32api.SetCursorPos((int(p.x), int(p.y)))


def distance(x, y):
    return math.sqrt((y.y-x.y)*(y.y-x.y)+(y.x-x.x)*(y.x-x.x))


def slide(p_src, p_des, v=1, duration=None, interval=0.01, release=True):
    """
    滑动操作，从p_src滑动到p_des
    """
    if duration == None:
        duration = random.uniform(0.3, 0.5)

    x = p_src.x
    y = p_src.y
    d = distance(p_src, p_des)
    v = d/duration
    d_x = p_des.x - p_src.x
    d_y = p_des.y - p_src.y
    v_x = v * d_x / d
    v_y = v * d_y / d

    p_cur = Point(x, y)
    p_next = Point()

    if get_background():
        window_handle = find_window(get_title())

        pos_body = get_window_pos(window_handle)

        # 加上偏移，传进来的坐标有标题栏和边框
        # 手动测试的，不一定完全准确
        p_cur.x = p_cur.x - pos_body.x - 5
        p_cur.y = p_cur.y - pos_body.y - 30

        long_position = win32api.MAKELONG(p_cur.x, p_cur.y)  # 模拟鼠标指针 传送到指定坐标
        win32gui.SendMessage(
            window_handle, win32con.WM_MOUSEMOVE, 0, long_position)
        win32gui.PostMessage(
            window_handle, win32con.WM_LBUTTONDOWN, 0, long_position)  # 模拟鼠标按下

        t = int(duration / interval)
        for _ in range(t):
            p_next.x = p_cur.x + v_x*interval
            p_next.y = p_cur.y + v_y*interval
            long_position = win32api.MAKELONG(
                int(p_next.x), int(p_next.y))  # 模拟鼠标指针 传送到指定坐标
            win32gui.SendMessage(
                window_handle, win32con.WM_MOUSEMOVE, 0, long_position)
            p_cur = p_next
            time.sleep(interval)

        if release:
            long_position = win32api.MAKELONG(
                int(p_next.x), int(p_next.y))  # 模拟鼠标指针 传送到指定坐标
            win32gui.SendMessage(
                window_handle, win32con.WM_LBUTTONUP, 0, long_position)  # 模拟鼠标弹起
    else:
        move(p_cur)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        t = int(duration / interval)
        for _ in range(t):
            p_next.x = p_cur.x + v_x*interval
            p_next.y = p_cur.y + v_y*interval
            move(p_next)
            p_cur = p_next
            time.sleep(interval)
        if release:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def click(p, duration=0):
    """
    点击操作
    """
    if duration == 0:
        duration = random.randint(20, 80)/1000

    background = get_background()
    if p == None:
        return

    if background:
        window_handle = find_window(get_title())

        pos_body = get_window_pos(window_handle)

        x = p.x - pos_body.x - 5
        y = p.y - pos_body.y - 30

        # 模拟鼠标指针 传送到指定坐标
        long_position = win32api.MAKELONG(x, y)
        win32gui.SendMessage(
            window_handle, win32con.WM_MOUSEMOVE, 0, long_position)
        # 模拟鼠标按下
        win32gui.SendMessage(
            window_handle, win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(duration)
        # 模拟鼠标弹起
        win32gui.SendMessage(
            window_handle, win32con.WM_LBUTTONUP, 0, long_position)

        logging.debug("点击("+str(p.x)+", "+str(p.y)+")")
    else:
        x = p.x
        y = p.y

        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

        logging.debug("点击("+str(x)+", "+str(y)+")")


def find_window(title):
    """
    查找窗口，返回句柄
    """
    handle = win32gui.FindWindow(None, title)
    return handle


def get_window_pos(window_handle):
    """
    获取窗口位置，返回(x,y,width,heigth)
    """
    rect = win32gui.GetWindowRect(find_window(get_title()))
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    pos = Pos(x, y, w, h)

    return pos


def get_screenshot(title, filename=None):
    """
    截图
    """
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
                              (bmpinfo['bmWidth'],
                               bmpinfo['bmHeight']),
                              bmpstr, 'raw', 'BGRX')
    res = cv2.cvtColor(np.asarray(im_PIL), cv2.COLOR_RGB2BGR)

    saveDC.SelectObject(saveBitMap)
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.DeleteObject(saveBitMap.GetHandle())
    win32gui.ReleaseDC(handle, hwndDC)
    return res


def match(img_rgb, template_rgb, show_result=False, thresold=0.7, gray=True):
    """
    模板匹配
    """
    img_gray = None
    template_gray = None
    w = 0
    h = 0
    if gray:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]
    else:
        img_gray = img_rgb
        template_gray = template_rgb
        h, w, _ = template_gray.shape

    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thresold)
    pos = []
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt,
                      (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        pos.append(Pos(pt[0], pt[1], w, h))
    if show_result:
        cv2.imshow("match result", img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return pos


def exists(template, flag=0, thresold=0.7, random_pos=True):
    if type(template) == str:
        template = cv2.imread(template)

    pos_body = get_window_pos(find_window(get_title()))
    resource = get_screenshot(get_title())
    pos = match(resource, template, thresold=thresold)
    if len(pos) > 0:
        logging.debug("目标模板存在")

        res = []
        if flag == 0:
            for p in pos:
                pt = Point(int(p.x + 0.5 * p.width),
                           int(p.y + 0.5 * p.height))
                pt = Point(pos_body.x + pt.x,
                           pos_body.y + pt.y)
                res.append(pt)
        if random_pos:
            res = res[random.randint(0, len(res) - 1)]
        return res
    else:
        logging.debug("目标模板不存在")
        return None


def wait_until(template, timeout=10,
               interval=1, flag=0,
               thresold=0.7, notify=True,
               raise_except=True):
    '''
    flag 0 -> center
    '''
    if type(template) == str:
        template = cv2.imread(template)

    pos_body = get_window_pos(find_window(get_title()))

    begin_time = datetime.now()
    while True:
        resource = get_screenshot(get_title())

        logging.debug("匹配中...")
        pos = match(resource, template, thresold=thresold)
        if len(pos) > 0:
            pos = pos[random.randint(0, len(pos) - 1)]

            logging.debug("匹配成功")
            if flag == 0:
                p = Point(int(pos.x + 0.5 * pos.width),
                          int(pos.y + 0.5 * pos.height))
                p = Point(pos_body.x + p.x,
                          pos_body.y + p.y)
            return p

        end_time = datetime.now()
        time.sleep(interval)
        if (end_time - begin_time).seconds >= timeout:
            if notify:
                toast("匹配过程超时，查看日志以获得更多信息")
            if raise_except:
                raise TimeoutError("Match process timeout.")
            else:
                break

    return None


def click_if_exists(template,
                    thresold=0.7,
                    click_random=10,
                    click_offset=(0, 0),
                    interval=0.5):
    """
    Click if template exists.
    """
    _p = exists(template=template, thresold=thresold)
    if _p is not None:
        _p = offset_position(_p, click_offset)
        random_sleep(interval, 0.2)
        random_click(_p, click_random)
        return True
    return False


def click_until():
    pass


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


def random_sleep(t, offset=0):
    return time.sleep(random_time(t, offset))


def random_click(p, offset):
    return click(random_position(p, offset))


def position_relative(x, y):
    pos_window = get_window_pos(find_window(get_title()))
    p = Point(int(pos_window.x +
                  pos_window.width * x),
              int(pos_window.y +
                  pos_window.height * y))
    return p


def set_foreround_window(title):
    GAME_TITLE = os.environ.get("GAME_TITLE")

    handle = find_window(GAME_TITLE)
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(handle)


def toast(message, duration=5):
    toaster = ToastNotifier()
    toaster.show_toast(message, duration=duration, threaded=True)
