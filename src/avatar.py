from logger import log
from states import States
from layers_manager import LayersManager

class Avatar:
    def __init__(self, name: str, dir: str):
        self.name = name
        self.dir = dir
        self.states = States()
        self.layers_manager = LayersManager(dir)

    def get_obj(self):
        return  {
                    "name": self.name,
                    "dir": self.dir
                }