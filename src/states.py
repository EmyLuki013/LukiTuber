class States:
    LAYER_ORDER = [
        "body",
        "eye_open", "eye_closed",
        "mouth_closed", "mouth_open", "mouth_open_big",
    ]

    def __init__(self):
        self.active_layers = ["body", "eye_open", "mouth_closed"]

        self.speaking = False
        self.blinking = False
        self.volume = 0.0

    def set_active(self, *layer_names):
        self.active_layers = [l for l in self.LAYER_ORDER if l in layer_names]

    def set_eyes(self, state: str):
        layer = f"eye_{state}"
        self._replace_group("eye_", layer)

    def set_mouth(self, state: str):
        layer = f"mouth_{state}"
        self._replace_group("mouth_", layer)

    def _replace_group(self, prefix: str, new_layer: str):
        others = [l for l in self.active_layers if not l.startswith(prefix)]
        others.append(new_layer)
        self.active_layers = [l for l in self.LAYER_ORDER if l in others]