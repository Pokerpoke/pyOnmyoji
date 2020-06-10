import os
import json


class Conf:
    def __init__(self):
        self.env_ = {
            "game_workspace": os.path.join(os.path.dirname(__file__), "..")
        }
        self.j = None

    def read(self):
        with open(os.path.join(self.env_["game_workspace"],
                               "onmyoji",
                               "configure.json"),
                  encoding="utf-8") as f:
            self.j = json.load(f)
        for key in self.j:
            if isinstance(self.j[key], str):
                for var in self.env_:
                    self.j[key] = self.j[key].replace(
                        "${"+var+"}", self.env_[var])

    def get(self, key):
        return self.j[key]

    def push(self, key, value):
        self.j[key] = value


game_conf = Conf()
game_conf.read()


def get(key):
    global game_conf

    return game_conf.get(key)


def push(key, value):
    global game_conf

    return game_conf.push(kye, value)
