import cv2
import time
import os
import json
import getopt
import sys
from window_funcs import *

resource_path = "./mods/match_test/img/resource.png"
template_path = "./mods/match_test/img/template.png"


def main():
    opts, args = getopt.getopt(sys.argv[1:], "t:")

    if args[0] == "screenshot":
        resource = get_screenshot(title)
    elif args[0] == "file":
        resource = cv2.imread(resource_path)

    template = cv2.imread(template_path)

    match(resource, template, show_result=True)
    # p = wait_until(template)
    # print(p.x)
    # print(p.y)


if __name__ == "__main__":
    main()
