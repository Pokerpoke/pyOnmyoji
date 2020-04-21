class Game_Mod():
    import sys
    import os
    import time
    import importlib
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    from onmyoji import onmyoji_funcs
    import logging
    sys.path.append("../")

    mod_path = os.environ.get("GAME_MODS_PATH")
    sys.path.append(mod_path)
    import huan_gou_liang.process

    def __init__(self):
        pass

    def main_process(self):
        pass

    def finished(self):
        pass
