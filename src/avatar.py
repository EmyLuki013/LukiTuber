from logger import log
from states import States

class Avatar:
    def __init__(self, name: str, dir: str):
        self.name = name
        self.dir = dir
        self.states = States()

    def get_obj(self):
        return  {
                    "name": self.name,
                    "dir": self.dir
                }