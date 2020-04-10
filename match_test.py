from window_funcs import *
import cv2
import time
import os
import json

resource_path = "1.png"
template_path = "2.png"


def main():
    # resource = get_screenshot(title)
    resource = cv2.imread(resource_path)
    template = cv2.imread(template_path)

    match(resource, template, show_result=True)
    # p = wait_until(template)
    # print(p.x)
    # print(p.y)


if __name__ == "__main__":
    main()
