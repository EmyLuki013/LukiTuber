import json
import os

from logger import log

class Avatar:
    def __init__(self, name: str, dir: str):
        self.name = name
        self.dir = dir

    def get_obj(self):
        return  {
                    "name": self.name,
                    "dir": self.dir
                }