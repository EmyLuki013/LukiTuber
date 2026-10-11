from enum import Enum

class StatesEnum(Enum):
    Default = "default"
    Open = "open"
    OpenBig = "open_big"
    Closed = "closed"

class States:
    def __init__(self):
        self.layers = {
            "body": StatesEnum.Default,
            "eyes": StatesEnum.Open,
            "mouth": StatesEnum.Closed,
        }

        self.speaking = False
        self.blinking = False
        self.volume = 0.0