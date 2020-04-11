# -*- coding:utf-8 -*-

import os
from .utils import *

def current_sence():
    '''
    0 - 庭院
    1 - 町中
    2 - tan suo
    '''
    cur_path = os.path.join(os.environ.get("YYS_WORKSPACE_PATH"),"onmyoji")

    if exists(os.path.join(cur_path,"img/tan_suo_deng_long.png")):
        return 0
    elif exists(os.path.join(cur_path,"img/ting_yuan.png")):
        return 1
    elif exists(os.path.join(cur_path,"img/tan_suo_cun_zi.png")):
        return 2
    else:
        return -1