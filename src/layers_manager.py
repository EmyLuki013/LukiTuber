import json
import os

from logger import log
from layer import Layer

LAYERS_FILE = "layers.json"

class LayersManager:
    def __init__(self, basePath):
        self.layers = []
        self.basePath = basePath
        self.layer_file_path = os.path.join(self.basePath, LAYERS_FILE)

    def get_layer(self):
        pass

    def create_layer(self):
        pass

    def save_layers(self):
        layers_obj = [a.get_obj() for a in self.layers]

        with open(self.layer_file_path, "w", encoding="utf-8") as f:
            json.dump(layers_obj, f, indent=2, ensure_ascii=False)

        log.info(f"Arquivo '{LAYERS_FILE}' salvo ({len(layers_obj)} layers)")

    def load_layers(self):
        if not os.path.exists(self.layer_file_path):
            log.warning(f"Arquivo '{LAYERS_FILE}' não encontrado. Criando novo...")

            self.layers = []
            for layer in ("body", "eyes", "mouth"):
                layer_path = os.path.join(self.basePath, layer)
                os.makedirs(layer_path, exist_ok=True)
                new_layer = Layer(layer, layer_path.replace("\\", "/"))
                self.layers.append(new_layer)

            self.save_layers()
            return

        with open(self.layer_file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            log.warning(f"Arquivo '{LAYERS_FILE}' vazio. Recriando...")

            self.layers = []
            for layer in ("body", "eyes", "mouth"):
                layer_path = os.path.join(self.basePath, layer)
                os.makedirs(layer_path, exist_ok=True)
                new_layer = Layer(layer, layer_path.replace("\\", "/"))
                self.layers.append(new_layer)

            self.save_layers()
            return

        try:
            layers_json = json.loads(content)
        except json.JSONDecodeError as e:
            log.error(f"JSON inválido em '{LAYERS_FILE}': {e}")
            raise

        self.layers = []

        log.info("Carregando Layers...")
        for obj in layers_json:
            new_layer = Layer(obj["name"], obj["path"])
            new_layer.set_offset(obj["x_offset"], obj["y_offset"])
            self.layers.append(new_layer)