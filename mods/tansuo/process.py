def main_process(times=1, time_used=35):
    import sys
    import os
    import time
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    from onmyoji import onmyoji_funcs
    import logging

    img_dir = os.path.join(__file__, "..", "img")

    onmyoji_funcs.goto_tan_suo()

    u.random_sleep(2, 0.3)
    p = u.exists(os.path.join(img_dir, "ping_an_qi_tan.png"))
    if p != None:
        p = u.offset_position(p, (150, -50))
        u.random_click(p, 10)
        u.random_sleep(5, 0.3)

    for i in range(times):
        logging.info("Start for times: " + str(i + 1) + ".")

        logging.info("Search for tan_suo.png.")
        p = u.wait_until(os.path.join(img_dir, "tan_suo.png"),
                         timeout=2)
        u.random_sleep(0.3, 0.05)
        u.random_click(p, 10)
        u.random_sleep(3, 0.5)

        j = 0
        BOSS_FOUND = False

        # search for battle
        logging.info("Search for zhan_dou.png.")
        while True:
            # boss appears
            p = u.exists(os.path.join(img_dir, "boss.png"))
            if p != None:
                BOSS_FOUND = True
                u.random_sleep(0.1, 0.05)
                u.random_click(p, 10)

            if not BOSS_FOUND:
                try:
                    p = u.wait_until(os.path.join(img_dir, "zhan_dou.png"),
                                     timeout=2)
                except TimeoutError:
                    p = u.exists(os.path.join(
                        img_dir, "chu_zhan_xiao_hao.png"))
                    p = u.offset_position(p, (-40, -50))
                    u.random_click(p, 10)
                    u.random_sleep(2, 0.5)
                    continue
                if p != None:
                    j = j+1
                    logging.info("Discover "+str(j)+"st monster.")
                    u.random_sleep(0.1, 0.05)
                    u.random_click(p, 10)

            logging.info("Search for zhun_bei.png.")
            p = u.wait_until(os.path.join(img_dir, "zhun_bei.png"),
                             timeout=2)
            u.random_sleep(0.3, 0.05)
            u.random_click(p, 10)
            u.random_sleep(3, 0.5)

            u.random_sleep(7+3, 0.5)

            # battle and win
            logging.info("Search for sheng_li.png.")
            p = u.wait_until(os.path.join(img_dir, "sheng_li.png"),
                             timeout=time_used+25)
            u.random_sleep(1, 0.3)
            p = u.offset_position(p, (300, 300))
            u.random_click(p, 20)
            # get rewards
            logging.info("Search for jie_suan.png.")
            p = u.wait_until(os.path.join(img_dir, "jie_suan.png"))
            u.random_sleep(1, 0.3)
            p = u.offset_position(p, (300, 0))
            u.random_click(p, 20)

            u.random_sleep(3, 0.3)

            if BOSS_FOUND:
                break

        u.random_sleep(5, 0.3)

        while True:
            p = u.exists(os.path.join(img_dir, "bao_xiang.png"))
            if p != None:
                logging.info("Discover treasure.")
                u.random_sleep(0.1, 0.05)
                u.random_click(p, 10)

                u.random_sleep(2, 0.5)

                logging.info("Search for huo_de_jiang_li.png.")
                p = u.wait_until(os.path.join(img_dir, "huo_de_jiang_li.png"),
                                 timeout=2)
                p = u.offset_position(p, (500, 0))
                u.random_click(p, 10)
            else:
                break

        u.random_sleep(5, 0.3)

        logging.info("Check if discover shi_ju(use ping_an_qi_tan).")
        p = u.exists(os.path.join(img_dir, "ping_an_qi_tan.png"))
        if p != None:
            p = u.offset_position(p, (150, -50))
            u.random_click(p, 10)
            u.random_sleep(5, 0.3)
