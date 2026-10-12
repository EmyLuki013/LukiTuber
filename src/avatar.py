from logger import log
from states import States
from layers_manager import LayersManager

class Avatar:
    def __init__(self, name: str, dir: str):
        self.name = name
        self.dir = dir
        self.states = States()
        self.layers_manager = LayersManager(dir)

        self.bbox_size = (500, 500)
        self.position = (400, 300)
        self.scale = 1.0

    def apply_bbox_scale(self, reference_layer="body"):
        self.layers_manager.apply_scale_from_reference(
            self.bbox_size,
            reference_layer=reference_layer,
            user_scale=self.scale,
        )

    def draw(self, surface):
        cx, cy = self.position
        for name in self.states.active_layers:
            layer = self.layers_manager.get_layer(name)
            if layer is None:
                continue
            layer.draw(surface, cx, cy)

    def get_obj(self):
        return {
            "name": self.name,
            "dir": self.dir,
            "position": list(self.position),
            "scale": self.scale,
        }