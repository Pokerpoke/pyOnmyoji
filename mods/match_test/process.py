def main_process(type):
    import sys
    import cv2
    sys.path.append("../../onmyoji")
    import onmyoji.utils as u
    import os

    resource_path = os.path.join(os.environ.get(
        "MODS_PATH"), "match_test", "img", "resource.png")
    template_path = os.path.join(os.environ.get(
        "MODS_PATH"), "match_test", "img", "template.png")

    if type == 0:
        resource = u.get_screenshot(title)
    elif type == 1:
        resource = cv2.imread(resource_path)

    template = cv2.imread(template_path)

    u.match(resource, template, show_result=True)
