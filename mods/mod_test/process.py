import logging
import onmyoji.onmyoji_funcs as o


def main_process(thresold=0.7, type=0):
    print(o.current_scene())
    o.goto_scene("ting_zhong")
    o.goto_scene("yu_hun")

    logging.info("Finished.")
