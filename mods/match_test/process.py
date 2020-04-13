def main_process(type=0):
    '''
    0 - screen shot
    1 - file
    '''
    import sys
    import cv2
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import os
    import logging

    # type = 1

    resource_path = os.path.join(os.environ.get(
        "YYS_MODS_PATH"), "match_test", "img", "resource.png")
    template_path = os.path.join(os.environ.get(
        "YYS_MODS_PATH"), "match_test", "img", "template.png")

    if type == 0:
        resource = u.get_screenshot(u.get_title())
    elif type == 1:
        resource = cv2.imread(resource_path)

    template = cv2.imread(template_path)

    logging.info("Match.")
    u.match(resource, template, show_result=True)
