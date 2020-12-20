#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import time
import importlib
import onmyoji.utils as u
import logging
import huan_gou_liang.process
import xie_zuo.process
import bonus.process
from onmyoji import onmyoji_funcs


def main_process(times=1, time_used=10):

    LOCKED = False
    BONUS_ACTIVE = False

    img_dir = os.path.join(__file__, "..", "img")

    logging.info("将要执行"+str(times)+"次")

    time_used_min = 5

    if onmyoji_funcs.current_scene() is not None:
        onmyoji_funcs.goto_scene("tan_suo")
        u.random_sleep(2, 0.3)

    p = u.exists(os.path.join(img_dir, "ping_an_qi_tan.png"))
    if p != None:
        p = u.offset_position(p, (150, -50))
        u.random_click(p, 10)
        u.random_sleep(5, 0.3)

    logging.info("Trig bonus.")
    if u.exists(os.path.join(img_dir, "bonus_deactive.png"),
                threshold=0.98):
        BONUS_ACTIVE = True
        bonus.process.main_process()

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")

        p = u.exists(os.path.join(
            img_dir, "chu_zhan_xiao_hao.png"))
        if p == None:
            logging.info("Search for tan_suo.png.")
            p = u.wait_until(os.path.join(img_dir, "tan_suo.png"))
            u.random_sleep(2, 0.5)
            u.random_click(p, 0)
            u.random_sleep(3, 0.5)

        j = 0
        BOSS_FOUND = False

        # check if locked
        logging.info("Search for zhen_rong_suo_ding.png.")
        p = u.exists(os.path.join(img_dir, "zhen_rong_suo_ding.png"))
        if p == None:
            LOCKED = False
        else:
            LOCKED = True

        # search for battle
        logging.info("Search for zhan_dou.png.")
        while True:
            # boss appears
            p = u.exists(os.path.join(img_dir, "boss.png"))
            if p != None:
                BOSS_FOUND = True
                u.random_sleep(1, 0.05)
                u.random_click(p, 10)

            if not BOSS_FOUND:
                try:
                    p = u.wait_until(os.path.join(img_dir, "zhan_dou.png"),
                                     timeout=2, notify=False)
                except TimeoutError:
                    p = u.exists(os.path.join(
                        img_dir, "chu_zhan_xiao_hao.png"))
                    p = u.offset_position(p, (-40, -50))
                    u.random_sleep(1, 0.05)
                    u.random_click(p, 10)
                    u.random_sleep(2, 0.5)
                    continue
                if p != None:
                    j = j+1
                    logging.info("Discover "+str(j)+"st monster.")
                    u.random_click(p, 2)

            if not LOCKED:
                logging.info("Search for zhun_bei.png.")
                p = u.wait_until(os.path.join(
                    img_dir, "zhun_bei.png"), interval=0.2)

                u.random_sleep(3, 0.05)

                logging.info("Check if needed to change dog food.")

                temp = u.exists(os.path.join(
                    img_dir, "man_2.png"), threshold=0.99)
                if temp == None:
                    temp = u.exists(os.path.join(
                        img_dir, "man_3.png"), threshold=0.99)
                if temp != None:
                    time.sleep(1)
                    huan_gou_liang.process.main_process()

                u.random_sleep(2, 0.5)
                u.random_click(p, 10)

            u.random_sleep(time_used_min, 0.5)

            # battle and win
            logging.info("Search for sheng_li.png.")
            p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                             timeout=time_used*2, interval=0.2)
            u.random_sleep(1, 0.2)
            p = u.offset_position(p, (300, 300))
            u.random_click(p, 20)
            u.random_sleep(2, 0.3)
            # get rewards
            logging.info("Search for jie_suan.png.")
            p = u.wait_until(os.path.join(
                img_dir, "jie_suan.png"), interval=0.2)
            u.random_sleep(2, 0.1)
            p = u.offset_position(p, (300, 0))
            u.random_click(p, 20)
            u.random_sleep(3, 0.3)

            if BOSS_FOUND:
                break

        u.random_sleep(5, 0.3)

        while True:
            p = u.exists(os.path.join(img_dir, "tan_suo.png"))
            if p != None:
                break
            p = u.exists(os.path.join(img_dir, "bao_xiang.png"), threshold=0.8)
            if p != None:
                logging.info("Discover treasure.")
                u.random_sleep(1, 0.1)
                u.random_click(p, 10)

                u.random_sleep(2, 0.5)

                logging.info("Search for huo_de_jiang_li.png.")
                p = u.wait_until(os.path.join(img_dir, "huo_de_jiang_li.png"),
                                 timeout=2)
                u.random_sleep(1, 0.1)
                p = u.offset_position(p, (500, 0))
                u.random_click(p, 10)
                u.random_sleep(3, 0.5)
            else:
                break

        u.random_sleep(5, 0.3)

        logging.info("Check if discover shi_ju(use ping_an_qi_tan).")
        p = u.exists(os.path.join(img_dir, "ping_an_qi_tan.png"))
        if p != None:
            p = u.offset_position(p, (150, -50))
            u.random_sleep(2, 0.5)
            u.random_click(p, 10)
            u.random_sleep(5, 0.3)

    logging.info("Trig bonus.")
    if BONUS_ACTIVE:
        bonus.process.main_process()

    u.toast("Explore finished.")
    logging.info("Finished.")
