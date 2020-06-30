#!/usr/bin/python3
# -*- coding:utf-8 -*-

from onmyoji import env
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
from PIL import ImageGrab
from win10toast import ToastNotifier
from threading import Thread


class OnmyojiThread(Thread):
    """
    封装后的线程
    @TODO 转移到Onmyoji相关文件中
    """

    def __init__(self, target):
        Thread.__init__(self)
        self.ret_val = None
        self.thread_ = target

    def run(self):
        self.ret_val = self.thread_()

    def get_ret(self):
        return self.ret_val


def get_title():
    """
    从全局变量中读取游戏名
    """
    return env.get("game_title")


def get_background():
    """
    从全局变量中读取后台运行标志
    """
    return env.get("game_background")


def get_window_handle(title):
    """
    通过标题获取窗口句柄
    """
    return find_window(title)


def get_cursor_window_handle():
    """
    获取鼠标点击处的窗口句柄
    """
    # Left button down = 0 or 1. Button up = -127 or -128
    state_left = win32api.GetKeyState(0x01)
    # Right button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)

    p = None
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:
            # Button state changed
            state_left = a
            if a < 0:
                logging.debug("左键按下")
                (x, y) = win32api.GetCursorPos()
                p = Point(x, y)
                break
            else:
                logging.debug("左键释放")
        if b != state_right:
            # Button state changed
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
    """
    窗口位置类
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class Point(object):
    """
    点
    """

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
        if other is None:
            return False
        elif self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


def move(p, continuous=False, interval=0.1):
    """
    移动鼠标
    """
    if continuous:
        pass
    else:
        win32api.SetCursorPos((int(p.x), int(p.y)))


def distance(x, y):
    """
    计算两点间的距离
    """
    return math.sqrt((y.y-x.y)*(y.y-x.y)+(y.x-x.x)*(y.x-x.x))


def check_handle(handle):
    """
    如果handle为None则获取默认句柄
    """
    if handle is None:
        return get_window_handle(get_title())
    else:
        return handle


def slide(p_src, p_des, handle=None, v=1,
          duration=None, interval=0.01, release=True):
    """
    滑动操作，从p_src滑动到p_des
    """
    handle = check_handle(handle)

    if duration == None:
        duration = random.uniform(0.3, 0.5)

    x = p_src.x
    y = p_src.y
    # 距离
    d = distance(p_src, p_des)
    # 速度
    v = d / duration
    # 偏移量
    d_x = p_des.x - p_src.x
    d_y = p_des.y - p_src.y
    # 速度分量
    v_x = v * d_x / d
    v_y = v * d_y / d
    # 临时变量用于迭代
    p_cur = Point(x, y)
    p_next = Point()
    # 后台运行
    if get_background():
        pos_body = get_window_pos(handle)
        # 加上偏移，传进来的坐标有标题栏和边框
        # 手动测试的，不一定完全准确
        p_cur.x = p_cur.x - pos_body.x - 5
        p_cur.y = p_cur.y - pos_body.y - 30
        # 模拟鼠标指针 传送到指定坐标
        long_position = win32api.MAKELONG(p_cur.x, p_cur.y)
        win32gui.SendMessage(
            handle, win32con.WM_MOUSEMOVE, 0, long_position)
        # 模拟鼠标按下
        win32gui.PostMessage(
            handle, win32con.WM_LBUTTONDOWN, 0, long_position)

        t = int(duration / interval)
        for _ in range(t):
            p_next.x = p_cur.x + v_x*interval
            p_next.y = p_cur.y + v_y * interval
            # 模拟鼠标指针 传送到指定坐标
            long_position = win32api.MAKELONG(
                int(p_next.x), int(p_next.y))
            win32gui.SendMessage(
                handle, win32con.WM_MOUSEMOVE, 0, long_position)
            p_cur = p_next
            time.sleep(interval)

        if release:
            # 模拟鼠标指针 传送到指定坐标
            long_position = win32api.MAKELONG(
                int(p_next.x), int(p_next.y))
            # 模拟鼠标弹起
            win32gui.SendMessage(
                handle, win32con.WM_LBUTTONUP, 0, long_position)
    # 前台运行
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


def click(p, handle=None, duration=0):
    """
    点击操作
    """
    handle = check_handle(handle)
    # 持续时间
    if duration == 0:
        duration = random.randint(20, 80)/1000

    background = get_background()
    if p is None:
        return
    # 后台运行
    if background:
        pos_body = get_window_pos(handle)

        x = p.x - pos_body.x - 5
        y = p.y - pos_body.y - 30

        # 模拟鼠标指针 传送到指定坐标
        long_position = win32api.MAKELONG(x, y)
        win32gui.SendMessage(
            handle, win32con.WM_MOUSEMOVE, 0, long_position)
        # 模拟鼠标按下
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(duration)
        # 模拟鼠标弹起
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONUP, 0, long_position)

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


def get_window_pos(handle=None):
    """
    获取窗口位置，返回(x,y,width,heigth)
    """

    handle = check_handle(handle)

    rect = win32gui.GetWindowRect(handle)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    pos = Pos(x, y, w, h)

    return pos


def get_screenshot(handle=None, filename=None, show=False):
    """
    截图
    """
################################################################################
#   以前可以用，不知道是不是处理过这种方法了
#   貌似阴阳师用win32截图出来，现在是全黑的，暂时弃用
#   PyQt5截图也不行了
#   后来又行了，可能是显卡驱动问题？增加了一个单选框进行切换
################################################################################
    handle = check_handle(handle)
    logging.info("current handle is: "+str(handle))
    if not env.get("game_image_grab"):
        hwndDC = win32gui.GetWindowDC(handle)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        pos = get_window_pos(handle)
        # 获取大小
        w = pos.width
        h = pos.height
        # 图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        # 是否保存为文件
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
        # 清理句柄
        # saveDC.SelectObject(saveBitMap)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(handle, hwndDC)

        return res

################################################################################
#   ImageGrab方式截图，要求不能被遮挡
################################################################################
    else:
        pos = get_window_pos(handle)
        bbox = (pos.x, pos.y, pos.x+pos.width, pos.y+pos.height)
        res = ImageGrab.grab(bbox)
        if show:
            res.show()
        if filename is not None:
            res.save(filename)

        res = cv2.cvtColor(np.asarray(res), cv2.COLOR_RGB2BGR)

        return res


def match(img_rgb, template_rgb,
          show_result=False, thresold=0.7, gray=True):
    """
    模板匹配
    接受RGB格式的图片作为输入，目前灰度处理后进行匹配，不包含颜色
    @TODO：增加对颜色的判断
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


def exists(template, handle=None, flag=0, thresold=0.7, random_pos=True):

    handle = check_handle(handle)

    if type(template) == str:
        template = cv2.imread(template)

    pos_body = get_window_pos(handle)
    resource = get_screenshot(handle)
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


def wait_until(template, timeout=10, handle=None,
               interval=1, flag=0,
               thresold=0.7, notify=True,
               raise_except=True):
    '''
    flag 0 -> center
    '''
    handle = check_handle(handle)
    if type(template) == str:
        template = cv2.imread(template)

    pos_body = get_window_pos(handle)

    begin_time = datetime.now()
    while True:
        resource = get_screenshot(handle)

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


def click_if_exists(template, handle=None,
                    thresold=0.7,
                    click_random=10,
                    click_offset=(0, 0),
                    interval=0.5):
    """
    Click if template exists.
    """
    handle = check_handle(handle)
    _p = exists(handle=handle, template=template, thresold=thresold)
    if _p is not None:
        _p = offset_position(_p, click_offset)
        random_sleep(interval, 0.2)
        random_click(_p, click_random)
        return True
    return False


def click_until():
    pass


def offset_position(p, offset=10):
    """
    偏移位置
    """
    if type(offset) == tuple:
        return p + Point(offset[0], offset[1])
    elif type(offset) == Point:
        return p + Point(offset.x, offset.y)


def random_position(p, offset=10):
    """
    随机位置
    """
    return p + Point(random.randint(-offset, offset),
                     random.randint(-offset, offset))


def random_time(t, offset=1):
    """
    随机时间
    """
    return t + random.uniform(-offset, offset)


def random_sleep(t, offset=0):
    """
    随机随眠
    """
    return time.sleep(random_time(t, offset))


def random_click(p, offset=10, handle=None):
    """
    随机点击
    """
    handle = check_handle(handle)
    return click(random_position(p, offset), handle=handle)


def position_relative(x, y, handle=None):
    """
    计算相对位置
    """
    handle = check_handle(handle)
    pos_window = get_window_pos(handle)
    p = Point(int(pos_window.x +
                  pos_window.width * x),
              int(pos_window.y +
                  pos_window.height * y))
    return p


def set_foreround_window(handle=None):
    """
    将窗口置前
    """
    handle = check_handle(handle)
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(handle)


def toast(message, duration=5):
    """
    win10通知
    """
    toaster = ToastNotifier()
    toaster.show_toast(message, duration=duration, threaded=True)
