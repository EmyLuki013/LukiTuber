class States:
    EXCLUSIVE_GROUPS = {
        "eye_":   "eye_open",
        "mouth_": "mouth_closed",
    }

    def __init__(self):
        self.active_layers = set()

        self.speaking = False
        self.blinking = False
        self.volume = 0.0

    def bootstrap_from_layers(self, layers):
        for default_layer in self.EXCLUSIVE_GROUPS.values():
            self.active_layers.add(default_layer)

        for layer in layers:
            if self._is_exclusive(layer.name):
                continue
            if layer.active:
                self.active_layers.add(layer.name)

    def _is_exclusive(self, name: str) -> bool:
        return any(name.startswith(p) for p in self.EXCLUSIVE_GROUPS)

    def set_eyes(self, state: str):
        self._set_group("eye_", f"eye_{state}")

    def set_mouth(self, state: str):
        self._set_group("mouth_", f"mouth_{state}")

    def _set_group(self, prefix: str, layer_name: str):
        for name in list(self.active_layers):
            if name.startswith(prefix):
                self.active_layers.discard(name)
        self.active_layers.add(layer_name)

    def is_active(self, name: str) -> bool:
        return name in self.active_layers