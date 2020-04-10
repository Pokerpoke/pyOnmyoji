def main_process():
    sys.path.append("../../onmyoji")
    from onmyoji.utils import *

    p = wait_until("./img/tiao_zhan.png")
    click(p)
