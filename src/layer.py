from logger import log

class Layer:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.x_offset = 0
        self.y_offset = 0

    def set_offset(self, x: int, y: int):
        self.x_offset = x
        self.y_offset = y

    def get_obj(self):
        return  {
                    "name": self.name,
                    "path": self.path,
                    "x_offset": self.x_offset,
                    "y_offset": self.y_offset
                }